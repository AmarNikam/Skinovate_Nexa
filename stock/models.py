from django.db import models
from django.contrib.auth.models import User


class Branch(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, help_text="City or area e.g. Nerul, Thane, Panvel")
    address = models.TextField(blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(blank=True, default='', help_text="Branch email for payout notifications")
    mobile = models.CharField(max_length=15, blank=True, default='', help_text="Branch mobile for SMS alerts")
    # Bank details for payout
    bank_name = models.CharField(max_length=100, blank=True, default='')
    account_holder = models.CharField(max_length=200, blank=True, default='')
    account_number = models.CharField(max_length=30, blank=True, default='')
    ifsc_code = models.CharField(max_length=20, blank=True, default='')
    upi_id = models.CharField(max_length=100, blank=True, default='', help_text="UPI ID for direct transfer")
    # Online payment options
    payment_link = models.URLField(blank=True, default='', help_text="PayTM/Razorpay/Google Pay payment link")
    gpay_mobile = models.CharField(max_length=15, blank=True, default='', help_text="Google Pay mobile number")
    paytm_mobile = models.CharField(max_length=15, blank=True, default='', help_text="PayTM mobile number")
    phonepe_mobile = models.CharField(max_length=15, blank=True, default='', help_text="PhonePe mobile number")
    # Tracking
    bank_details_updated_at = models.DateTimeField(null=True, blank=True)
    bank_details_updated_by = models.ForeignKey(
        'auth.User', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='bank_updates'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def has_bank_details(self):
        return bool(self.account_number or self.upi_id)

    def has_online_payment(self):
        return bool(self.upi_id or self.gpay_mobile or self.paytm_mobile
                    or self.phonepe_mobile or self.payment_link)

    def __str__(self):
        return f"{self.name} - {self.location}"

    class Meta:
        ordering = ['location', 'name']
        verbose_name_plural = 'Branches'


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('manager', 'Branch Manager'),
        ('staff', 'Staff'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='users', help_text="Leave blank for Owner (owner sees all branches)")

    def is_owner(self):
        return self.role == 'owner'

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    current_stock = models.IntegerField(default=0)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        help_text="Fixed MRP (Maximum Retail Price)")
    dp = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        help_text="Distributor Price - editable anytime")

    def stock_status(self):
        if self.current_stock <= 0:
            return 'OUT'
        elif self.current_stock <= 5:
            return 'LOW'
        return 'OK'

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class StockIn(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='stock_ins', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_ins')
    date = models.DateField()
    quantity_in = models.PositiveIntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    supplier = models.CharField(max_length=200, default='Dr. Susshil')

    @property
    def total_purchase_value(self):
        return self.quantity_in * self.purchase_price

    def __str__(self):
        return f"{self.product.name} - {self.date} - {self.branch}"

    class Meta:
        ordering = ['-date']


SALE_TYPE_CHOICES = [
    ('MRP', 'MRP'),
    ('Sample', 'Sample'),
    ('50%', '50% Discount'),
    ('Other', 'Other'),
]

DISCOUNT_BASE_CHOICES = [
    ('MRP', 'Discount on MRP'),
    ('DP', 'Discount on DP (Distributor Price)'),
    ('NONE', 'No Discount (Full Price)'),
]


class Sale(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='sales', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    date = models.DateField()
    customer_name = models.CharField(max_length=200)
    quantity_sold = models.PositiveIntegerField(default=1)
    sale_type = models.CharField(max_length=20, choices=SALE_TYPE_CHOICES, default='MRP')
    discount_base = models.CharField(max_length=10, choices=DISCOUNT_BASE_CHOICES, default='NONE')
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, default='')

    def calculate_selling_price(self):
        from decimal import Decimal
        discount_percent = Decimal(str(self.discount_percent))
        base = self.product.mrp if self.discount_base in ('MRP', 'NONE') else self.product.dp
        return base - (base * discount_percent / Decimal('100'))

    @property
    def total_sale_value(self):
        return self.quantity_sold * self.selling_price

    def __str__(self):
        return f"{self.customer_name} - {self.product.name} - {self.date}"

    class Meta:
        ordering = ['-date']


# ─── Commission System ────────────────────────────────────────────────────────

COMMISSION_TYPE_CHOICES = [
    ('percentage', 'Percentage of Sales (%)'),
    ('fixed',      'Fixed Amount per Month (₹)'),
]

BRANCH_TYPE_CHOICES = [
    ('branch',     'Company Branch'),
    ('franchise',  'Franchise'),
]


class CommissionSetting(models.Model):
    """Owner sets commission rate for each branch/franchise."""
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, related_name='commission_setting')
    branch_type = models.CharField(max_length=20, choices=BRANCH_TYPE_CHOICES, default='branch')
    commission_type = models.CharField(max_length=20, choices=COMMISSION_TYPE_CHOICES, default='percentage')
    commission_value = models.DecimalField(max_digits=10, decimal_places=2, default=0,
        help_text="Enter % value (e.g. 10 for 10%) or fixed ₹ amount per month")
    tds_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0,
        help_text="TDS percentage deducted from commission (e.g. 10 for 10% TDS)")
    service_charge_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0,
        help_text="Service charge % added to commission (e.g. 5 for 5%)")
    effective_from = models.DateField(default=None, null=True, blank=True)
    notes = models.TextField(blank=True, default='')

    def calculate_commission(self, total_sales):
        from decimal import Decimal
        if self.commission_type == 'percentage':
            base = Decimal(str(total_sales)) * self.commission_value / Decimal('100')
        else:
            base = self.commission_value
        service = base * self.service_charge_percent / Decimal('100')
        gross   = base + service
        tds     = gross * self.tds_percent / Decimal('100')
        net     = gross - tds
        return {
            'base_commission':   base,
            'service_charge':    service,
            'gross_commission':  gross,
            'tds_amount':        tds,
            'net_commission':    net,
        }

    def __str__(self):
        return f"{self.branch.name} — {self.commission_type} @ {self.commission_value}"


class MonthlyCommission(models.Model):
    """Auto-generated monthly commission record per branch."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid',    'Paid'),
        ('partial', 'Partial'),
    ]
    branch           = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='commissions')
    month            = models.IntegerField()
    year             = models.IntegerField()
    total_sales      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commission_type  = models.CharField(max_length=20, default='percentage')
    commission_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Breakdown stored at generation time
    base_commission         = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    service_charge_percent  = models.DecimalField(max_digits=5,  decimal_places=2, default=0)
    service_charge_amount   = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gross_commission        = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tds_percent             = models.DecimalField(max_digits=5,  decimal_places=2, default=0)
    tds_amount              = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commission_amount       = models.DecimalField(max_digits=12, decimal_places=2, default=0,
        help_text="Net payable commission after TDS and service charge")
    amount_paid      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_date     = models.DateField(null=True, blank=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes            = models.TextField(blank=True, default='')
    generated_on     = models.DateTimeField(auto_now_add=True)

    @property
    def amount_pending(self):
        return self.commission_amount - self.amount_paid

    @property
    def month_name(self):
        import calendar
        return calendar.month_name[self.month]

    def __str__(self):
        return f"{self.branch.name} — {self.month_name} {self.year}"

    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['branch', 'month', 'year']


class PayoutLog(models.Model):
    """Records every payout notification sent to a branch."""
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms',   'SMS'),
        ('both',  'Email + SMS'),
    ]
    monthly_commission = models.ForeignKey(MonthlyCommission, on_delete=models.CASCADE,
        related_name='payout_logs')
    sent_at   = models.DateTimeField(auto_now_add=True)
    channel   = models.CharField(max_length=10, choices=CHANNEL_CHOICES, default='both')
    sent_to_email  = models.EmailField(blank=True, default='')
    sent_to_mobile = models.CharField(max_length=15, blank=True, default='')
    email_status   = models.CharField(max_length=20, default='pending')  # sent/failed/skipped
    sms_status     = models.CharField(max_length=20, default='pending')
    message_preview = models.TextField(blank=True, default='')
    sent_by   = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    notes     = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Payout to {self.monthly_commission.branch.name} — {self.sent_at.date()}"

    class Meta:
        ordering = ['-sent_at']
