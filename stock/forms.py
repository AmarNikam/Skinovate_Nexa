from django import forms
from .models import StockIn, Sale, Product, Branch, UserProfile
from django.contrib.auth.models import User
from django.utils import timezone

WIDGET_ATTRS = {'class': 'form-input'}
SELECT_ATTRS = {'class': 'form-select'}


class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = ['branch', 'product', 'date', 'quantity_in', 'purchase_price', 'supplier']
        widgets = {
            'branch':         forms.Select(attrs=SELECT_ATTRS),
            'product':        forms.Select(attrs=SELECT_ATTRS),
            'date':           forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'quantity_in':    forms.NumberInput(attrs={'min': '0', **WIDGET_ATTRS}),
            'purchase_price': forms.NumberInput(attrs={'min': '0', 'step': '0.01', **WIDGET_ATTRS}),
            'supplier':       forms.TextInput(attrs=WIDGET_ATTRS),
        }

    def __init__(self, *args, user_branch=None, is_owner=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not is_owner:
            # Staff: hide branch field, it'll be set in the view
            self.fields.pop('branch', None)
        else:
            self.fields['branch'].queryset = Branch.objects.filter(is_active=True)
        if not self.initial.get('date'):
            self.fields['date'].initial = timezone.localdate()


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['branch', 'product', 'date', 'customer_name', 'quantity_sold',
                  'sale_type', 'discount_base', 'discount_percent',
                  'payment_received', 'payment_pending', 'description']
        widgets = {
            'branch':           forms.Select(attrs=SELECT_ATTRS),
            'product':          forms.Select(attrs={**SELECT_ATTRS, 'id': 'id_product'}),
            'date':             forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'customer_name':    forms.TextInput(attrs=WIDGET_ATTRS),
            'quantity_sold':    forms.NumberInput(attrs={'min': '1', 'id': 'id_quantity_sold', **WIDGET_ATTRS}),
            'sale_type':        forms.Select(attrs=SELECT_ATTRS),
            'discount_base':    forms.Select(attrs={**SELECT_ATTRS, 'id': 'id_discount_base'}),
            'discount_percent': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01',
                                'id': 'id_discount_percent', 'placeholder': '00.00', **WIDGET_ATTRS}),
            'payment_received': forms.NumberInput(attrs={'min': '0', 'step': '0.01', **WIDGET_ATTRS}),
            'payment_pending':  forms.NumberInput(attrs={'min': '0', 'step': '0.01', **WIDGET_ATTRS}),
            'description':      forms.Textarea(attrs={'rows': 2, 'class': 'form-textarea'}),
        }

    def __init__(self, *args, user_branch=None, is_owner=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not is_owner:
            self.fields.pop('branch', None)
        else:
            self.fields['branch'].queryset = Branch.objects.filter(is_active=True)
        if not self.initial.get('date'):
            self.fields['date'].initial = timezone.localdate()

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        qty = cleaned_data.get('quantity_sold', 0)
        if product and qty:
            existing_qty = self.instance.quantity_sold if (self.instance and self.instance.pk) else 0
            net_change = qty - existing_qty
            if product.current_stock < net_change:
                self.add_error('quantity_sold',
                    f'Not enough stock! Current stock: {product.current_stock}, Requested: {net_change}')
        discount_base = cleaned_data.get('discount_base')
        discount_percent = cleaned_data.get('discount_percent')
        if discount_base in ('MRP', 'DP'):
            if discount_percent is None:
                self.add_error('discount_percent', 'Enter a discount % when MRP or DP discount is selected.')
            elif discount_percent < 0 or discount_percent > 100:
                self.add_error('discount_percent', 'Discount must be between 0.00 and 100.00')
            else:
                from decimal import Decimal, ROUND_HALF_UP
                cleaned_data['discount_percent'] = Decimal(str(discount_percent)).quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP)
        elif discount_base == 'NONE':
            cleaned_data['discount_percent'] = 0
        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'mrp', 'dp', 'current_stock']
        widgets = {
            'name':          forms.TextInput(attrs=WIDGET_ATTRS),
            'mrp':           forms.NumberInput(attrs={'min': '0', 'step': '0.01', **WIDGET_ATTRS}),
            'dp':            forms.NumberInput(attrs={'min': '0', 'step': '0.01', **WIDGET_ATTRS}),
            'current_stock': forms.NumberInput(attrs=WIDGET_ATTRS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['mrp'].disabled = True
            self.fields['mrp'].widget.attrs['style'] = 'background:#f3f4f6;cursor:not-allowed;'
            self.fields['mrp'].help_text = 'MRP is fixed and cannot be changed after creation'


class BranchForm(forms.ModelForm):
    """Full branch form for owner — all fields."""
    class Meta:
        model = Branch
        fields = ['name', 'location', 'address', 'phone', 'email', 'mobile',
                  'bank_name', 'account_holder', 'account_number', 'ifsc_code',
                  'upi_id', 'gpay_mobile', 'paytm_mobile', 'phonepe_mobile',
                  'payment_link', 'is_active']
        widgets = {
            'name':            forms.TextInput(attrs=WIDGET_ATTRS),
            'location':        forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. Nerul, Thane, Panvel'}),
            'address':         forms.Textarea(attrs={'rows': 2, 'class': 'form-textarea'}),
            'phone':           forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '9876543210'}),
            'email':           forms.EmailInput(attrs={**WIDGET_ATTRS, 'placeholder': 'branch@email.com'}),
            'mobile':          forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '9876543210'}),
            'bank_name':       forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. HDFC Bank'}),
            'account_holder':  forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Account holder full name'}),
            'account_number':  forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Bank account number'}),
            'ifsc_code':       forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. HDFC0001234'}),
            'upi_id':          forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. name@upi'}),
            'gpay_mobile':     forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Google Pay mobile'}),
            'paytm_mobile':    forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'PayTM mobile'}),
            'phonepe_mobile':  forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'PhonePe mobile'}),
            'payment_link':    forms.URLInput(attrs={**WIDGET_ATTRS, 'placeholder': 'https://razorpay.me/...'}),
            'is_active':       forms.CheckboxInput(),
        }


class BranchStaffBankForm(forms.ModelForm):
    """
    Restricted form for branch staff — they can update their own
    contact and payment details, but cannot change branch name/location/status.
    """
    class Meta:
        model = Branch
        fields = ['email', 'mobile', 'phone',
                  'bank_name', 'account_holder', 'account_number',
                  'ifsc_code', 'upi_id',
                  'gpay_mobile', 'paytm_mobile', 'phonepe_mobile', 'payment_link']
        widgets = {
            'phone':           forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '9876543210'}),
            'email':           forms.EmailInput(attrs={**WIDGET_ATTRS, 'placeholder': 'branch@email.com'}),
            'mobile':          forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '9876543210'}),
            'bank_name':       forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. HDFC Bank'}),
            'account_holder':  forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Account holder full name'}),
            'account_number':  forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Bank account number'}),
            'ifsc_code':       forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. HDFC0001234'}),
            'upi_id':          forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. name@upi'}),
            'gpay_mobile':     forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Google Pay mobile'}),
            'paytm_mobile':    forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'PayTM mobile'}),
            'phonepe_mobile':  forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'PhonePe mobile'}),
            'payment_link':    forms.URLInput(attrs={**WIDGET_ATTRS, 'placeholder': 'https://razorpay.me/...'}),
        }


class UserBranchForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs=SELECT_ATTRS),
        help_text='Select a user to assign to this branch'
    )
    role = forms.ChoiceField(
        choices=[('staff', 'Staff'), ('manager', 'Branch Manager')],
        widget=forms.Select(attrs=SELECT_ATTRS)
    )

    def __init__(self, *args, branch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if branch:
            # Show all users not already assigned to this branch
            assigned = UserProfile.objects.filter(branch=branch).values_list('user_id', flat=True)
            self.fields['user'].queryset = User.objects.exclude(pk__in=assigned)


class CommissionSettingForm(forms.ModelForm):
    class Meta:
        model = __import__('stock.models', fromlist=['CommissionSetting']).CommissionSetting
        fields = ['branch_type', 'commission_type', 'commission_value',
                  'tds_percent', 'service_charge_percent', 'effective_from', 'notes']
        widgets = {
            'branch_type':             forms.Select(attrs=SELECT_ATTRS),
            'commission_type':         forms.Select(attrs=SELECT_ATTRS),
            'commission_value':        forms.NumberInput(attrs={'min': '0', 'step': '0.01',
                                           'placeholder': 'e.g. 10 for 10% or 5000 for ₹5000', **WIDGET_ATTRS}),
            'tds_percent':             forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01',
                                           'placeholder': 'e.g. 10 for 10% TDS', **WIDGET_ATTRS}),
            'service_charge_percent':  forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01',
                                           'placeholder': 'e.g. 5 for 5% service charge', **WIDGET_ATTRS}),
            'effective_from':          forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'notes':                   forms.Textarea(attrs={'rows': 2, 'class': 'form-textarea'}),
        }


class CommissionPaymentForm(forms.ModelForm):
    class Meta:
        model = __import__('stock.models', fromlist=['MonthlyCommission']).MonthlyCommission
        fields = ['amount_paid', 'payment_date', 'status', 'notes']
        widgets = {
            'amount_paid':   forms.NumberInput(attrs={'min': '0', 'step': '0.01', **WIDGET_ATTRS}),
            'payment_date':  forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'status':        forms.Select(attrs=SELECT_ATTRS),
            'notes':         forms.Textarea(attrs={'rows': 2, 'class': 'form-textarea'}),
        }
