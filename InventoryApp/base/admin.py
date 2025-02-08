from django.contrib import admin
from .models import (
    UserProfile, 
    InventoryItem, 
    Checkout, 
    MaintenanceRecord, 
    DisposalRecord, 
    ReorderRequest
)

admin.site.register(UserProfile)
admin.site.register(InventoryItem)
admin.site.register(Checkout)
admin.site.register(MaintenanceRecord)
admin.site.register(DisposalRecord)
admin.site.register(ReorderRequest)
