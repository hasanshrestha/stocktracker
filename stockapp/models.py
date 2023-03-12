from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Broker(models.Model):
    broker_number = models.CharField(max_length=100, primary_key=True) # 2,9,12,15,23,24,27,30,31
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "broker"

    def __str__(self):
        return self.broker_number


class Stock(models.Model):
    symbol = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=100)
    market_price = models.CharField(max_length=255)
    listed_shares = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "stock"
    
    def __str__(self):
        return self.symbol


class Holdings(models.Model):
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    total_shares = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "holdings"


class HoldingsPerMonth(models.Model):
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    total_shares = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "holdingspermonth"


class DailyTransaction(models.Model):
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    total_shares = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "dailytransaction"


class YesterdayTransaction(models.Model):
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    total_shares = models.CharField(max_length=255)
    percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "yesterdaytransaction"