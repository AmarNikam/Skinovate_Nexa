"""
Payout notification service for Skinovate.
Sends email + SMS to branch owner when commission is paid out.
Demo: all notifications also go to owner's email/mobile as fallback.
"""
import logging
import urllib.request
import urllib.parse
import json
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

logger = logging.getLogger(__name__)

OWNER_EMAIL  = getattr(settings, 'OWNER_EMAIL',  'amarnik88@gmail.com')
OWNER_MOBILE = getattr(settings, 'OWNER_MOBILE', '7021444055')


def send_payout_email(mc, to_email, sent_by_user):
    """Send a payout notification email for a MonthlyCommission record."""
    branch = mc.branch
    subject = f"Skinovate — Commission Payout: {branch.name} | {mc.month_name} {mc.year}"

    # Plain text body
    body = f"""
Dear {branch.account_holder or branch.name},

Your commission for {mc.month_name} {mc.year} has been processed by Skinovate.

─────────────────────────────────────────
  COMMISSION BREAKDOWN — {branch.name}
─────────────────────────────────────────
  Period          : {mc.month_name} {mc.year}
  Total Sales     : ₹{mc.total_sales:,.2f}
  Base Commission : ₹{mc.base_commission:,.2f}  ({mc.commission_value}%)
  Service Charge  : ₹{mc.service_charge_amount:,.2f}  ({mc.service_charge_percent}%)
  Gross Commission: ₹{mc.gross_commission:,.2f}
  TDS Deducted    : ₹{mc.tds_amount:,.2f}  ({mc.tds_percent}%)
  ─────────────────────────────────────
  NET PAYABLE     : ₹{mc.commission_amount:,.2f}
  Amount Paid     : ₹{mc.amount_paid:,.2f}
  Pending         : ₹{mc.amount_pending:,.2f}
  Status          : {mc.get_status_display().upper()}
─────────────────────────────────────────

Payment sent to:
  Bank     : {branch.bank_name or '—'}
  A/C Name : {branch.account_holder or '—'}
  A/C No.  : {mask_account(branch.account_number)}
  IFSC     : {branch.ifsc_code or '—'}
  UPI ID   : {branch.upi_id or '—'}

For any queries, contact Skinovate owner.
This is an automated notification. Please do not reply.

— Skinovate Management
  {OWNER_EMAIL} | {OWNER_MOBILE}
"""

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )
        return 'sent'
    except Exception as e:
        logger.error(f"Email failed for {branch.name}: {e}")
        return f'failed: {str(e)[:80]}'


def send_payout_sms(mc, to_mobile):
    """Send a payout notification SMS using Fast2SMS API."""
    branch = mc.branch
    message = (
        f"Skinovate Payout: {branch.name} | {mc.month_name} {mc.year} | "
        f"Net Commission: Rs{mc.commission_amount:,.0f} | "
        f"Paid: Rs{mc.amount_paid:,.0f} | "
        f"Status: {mc.get_status_display()} | "
        f"Skinovate Mgmt {OWNER_MOBILE}"
    )
    # Truncate to 160 chars for SMS
    message = message[:160]

    api_key = getattr(settings, 'FAST2SMS_API_KEY', '')
    if not api_key:
        # No API key — log and return demo mode
        logger.info(f"SMS (DEMO — no API key): To {to_mobile}: {message}")
        return 'demo_mode'

    try:
        url = "https://www.fast2sms.com/dev/bulkV2"
        payload = {
            'authorization': api_key,
            'message': message,
            'language': 'english',
            'route': 'q',
            'numbers': to_mobile.replace('+91', '').replace(' ', ''),
        }
        data = urllib.parse.urlencode(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            if result.get('return'):
                return 'sent'
            return f"failed: {result.get('message','unknown')}"
    except Exception as e:
        logger.error(f"SMS failed for {branch.name}: {e}")
        return f'failed: {str(e)[:80]}'


def send_payout_notification(mc, sent_by_user):
    """
    Master function: send email + SMS for one MonthlyCommission.
    Uses branch email/mobile if set, otherwise falls back to owner's.
    Returns a PayoutLog instance.
    """
    from .models import PayoutLog

    branch = mc.branch

    # Determine recipients — branch details or owner fallback
    to_email  = branch.email  if branch.email  else OWNER_EMAIL
    to_mobile = branch.mobile if branch.mobile else OWNER_MOBILE

    fallback_note = ''
    if not branch.email:
        fallback_note += f'[Email sent to owner {OWNER_EMAIL} — branch email not set] '
    if not branch.mobile:
        fallback_note += f'[SMS sent to owner {OWNER_MOBILE} — branch mobile not set] '

    email_status = send_payout_email(mc, to_email, sent_by_user)
    sms_status   = send_payout_sms(mc, to_mobile)

    preview = (
        f"To: {to_email} / {to_mobile} | "
        f"Net: ₹{mc.commission_amount:,.2f} | "
        f"Month: {mc.month_name} {mc.year}"
    )

    log = PayoutLog.objects.create(
        monthly_commission=mc,
        channel='both',
        sent_to_email=to_email,
        sent_to_mobile=to_mobile,
        email_status=email_status,
        sms_status=sms_status,
        message_preview=preview,
        sent_by=sent_by_user,
        notes=fallback_note,
    )

    # Mark commission as paid if not already
    if mc.status == 'pending':
        mc.status = 'partial'
        mc.save(update_fields=['status'])

    return log


def mask_account(acc_no):
    """Mask account number for security: show last 4 digits only."""
    if not acc_no:
        return '—'
    if len(acc_no) <= 4:
        return acc_no
    return 'X' * (len(acc_no) - 4) + acc_no[-4:]
