# Transactions

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('SALE', 'Property Sale'),
        ('PURCHASE', 'Property Purchase'),
        ('RENT', 'Rent Payment'),
        ('DEPOSIT', 'Security Deposit'),
        ('MAINTENANCE', 'Maintenance Fee'),
        ('PROPERTY_TAX', 'Property Tax'),
        ('INSURANCE', 'Insurance Payment'),
        ('UTILITY', 'Utility Payment'),
        ('COMMISSION', 'Agent Commission'),
        ('OTHER', 'Other'),
    ]

    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CHECK', 'Check'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('PAYPAL', 'PayPal'),
        ('CRYPTOCURRENCY', 'Cryptocurrency'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]

    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    payee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_received')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reference_number = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TransactionDetail(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='details')
    invoice_number = models.CharField(max_length=100, blank=True)
    purchase_order_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    additional_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Refund(models.Model):
    REFUND_REASONS = [
        ('OVERPAYMENT', 'Overpayment'),
        ('CANCELLATION', 'Service Cancellation'),
        ('DISSATISFACTION', 'Customer Dissatisfaction'),
        ('ERROR', 'Billing Error'),
        ('OTHER', 'Other'),
    ]

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.CharField(max_length=20, choices=REFUND_REASONS)
    description = models.TextField(blank=True)
    refund_date = models.DateTimeField()
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_refunds')
    status = models.CharField(max_length=20, choices=Transaction.STATUS_CHOICES, default='PENDING')

class PaymentPlan(models.Model):
    FREQUENCY_CHOICES = [
        ('WEEKLY', 'Weekly'),
        ('BI_WEEKLY', 'Bi-weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('ANNUALLY', 'Annually'),
    ]

    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='payment_plans')
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, related_name='payment_plans')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PaymentPlanInstallment(models.Model):
    payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name='installments')
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Transaction.STATUS_CHOICES, default='PENDING')
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True)

class Invoice(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='invoices')
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ])
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

class TransactionFee(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=50, choices=[
        ('PROCESSING', 'Processing Fee'),
        ('SERVICE', 'Service Fee'),
        ('LATE', 'Late Payment Fee'),
        ('CONVENIENCE', 'Convenience Fee'),
        ('OTHER', 'Other Fee'),
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    method_type = models.CharField(max_length=50, choices=[
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('BANK_ACCOUNT', 'Bank Account'),
        ('PAYPAL', 'PayPal'),
        ('OTHER', 'Other'),
    ])
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    # Sensitive information should be stored securely, possibly using encryption
    # These fields are placeholders and should be handled with proper security measures
    card_last_four = models.CharField(max_length=4, blank=True)
    card_expiry = models.CharField(max_length=5, blank=True)
    bank_account_last_four = models.CharField(max_length=4, blank=True)

class TransactionDispute(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='disputes')
    disputed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disputed_transactions')
    reason = models.CharField(max_length=50, choices=[
        ('UNAUTHORIZED', 'Unauthorized Transaction'),
        ('DUPLICATE', 'Duplicate Charge'),
        ('PRODUCT_NOT_RECEIVED', 'Product/Service Not Received'),
        ('INCORRECT_AMOUNT', 'Incorrect Amount'),
        ('QUALITY', 'Quality or Service Issue'),
        ('OTHER', 'Other'),
    ])
    description = models.TextField()
    submitted_date = models.DateTimeField(auto_now_add=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('OPEN', 'Open'),
        ('UNDER_REVIEW', 'Under Review'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ], default='OPEN')
    resolution = models.TextField(blank=True)

class TransactionReceipt(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=50, unique=True)
    generated_date = models.DateTimeField(auto_now_add=True)
    sent_to_email = models.EmailField(blank=True)
    pdf_file = models.FileField(upload_to='transaction_receipts/', null=True, blank=True)

class RecurringPayment(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_payments')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='recurring_payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=[
        ('WEEKLY', 'Weekly'),
        ('BIWEEKLY', 'Bi-weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('ANNUALLY', 'Annually'),
    ])
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    next_payment_date = models.DateField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

class TransactionTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

class TransactionTagAssignment(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(TransactionTag, on_delete=models.CASCADE)

class TransactionNote(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TransactionAttachment(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='transaction_attachments/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class TransactionSummary(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='transaction_summaries')
    period_start = models.DateField()
    period_end = models.DateField()
    total_income = models.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    net_income = models.DecimalField(max_digits=12, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

class PaymentReminder(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='reminders')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_reminders')
    send_date = models.DateTimeField()
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)

class TransactionExport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_exports')
    start_date = models.DateField()
    end_date = models.DateField()
    export_format = models.CharField(max_length=10, choices=[
        ('CSV', 'CSV'),
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
    ])
    generated_file = models.FileField(upload_to='transaction_exports/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ], default='PENDING')

class TransactionCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

class TransactionCategoryAssignment(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
