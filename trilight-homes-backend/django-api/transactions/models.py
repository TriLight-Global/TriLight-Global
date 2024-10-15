# from django.db import models

# # Create your models here.

# class PropertyTransaction(models.Model):
#     property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='transactions')
#     transaction_type = models.CharField(_("Transaction Type"), max_length=20)  # e.g., 'sale', 'rent', 'lease'
#     price = models.DecimalField(_("Price"), max_digits=15, decimal_places=2)
#     date = models.DateField(_("Date"))
#     agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')

#     def __str__(self):
#         return f"{self.transaction_type.capitalize()} of {self.property.title} on {self.date}"

# class RentPayment(models.Model):
#     tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
#     property = models.ForeignKey(Property, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateField()
#     status = models.CharField(max_length=20)
