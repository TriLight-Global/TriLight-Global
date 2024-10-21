from django.db import models
from django.contrib.auth.models import User

# Analytics App

class PropertyAnalytics(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='analytics')
    average_occupancy_rate = models.DecimalField(max_digits=5, decimal_places=2)
    average_rent = models.DecimalField(max_digits=10, decimal_places=2)
    maintenance_cost_ytd = models.DecimalField(max_digits=10, decimal_places=2)
    roi = models.DecimalField(max_digits=5, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

class MarketTrend(models.Model):
    area = models.CharField(max_length=100)
    property_type = models.CharField(max_length=50)
    average_price = models.DecimalField(max_digits=12, decimal_places=2)
    price_change_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()

class FinancialReport(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='financial_reports')
    report_type = models.CharField(max_length=50, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    ])
    start_date = models.DateField()
    end_date = models.DateField()
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    net_income = models.DecimalField(max_digits=12, decimal_places=2)

class Forecast(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='forecasts')
    forecast_type = models.CharField(max_length=50, choices=[
        ('rent', 'Rent'),
        ('occupancy', 'Occupancy'),
        ('maintenance_cost', 'Maintenance Cost'),
        ('property_value', 'Property Value'),
    ])
    start_date = models.DateField()
    end_date = models.DateField()
    forecasted_value = models.DecimalField(max_digits=12, decimal_places=2)
    confidence_level = models.DecimalField(max_digits=5, decimal_places=2)

class PerformanceMetric(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='performance_metrics')
    metric_name = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

