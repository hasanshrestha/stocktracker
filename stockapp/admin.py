from django.contrib import admin
from .models import Broker, Stock, Holdings

# Register your models here.
# admin.site.register(Broker)
@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ["broker_number", "name", "address"]
    list_editable = ["name", "address"]

#admin.site.register(Stock)
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["name", "symbol", "sector"]


admin.site.register(Holdings)
