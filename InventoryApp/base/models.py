from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class InventoryItem(models.Model):
    ITEM_STATUS = (
        ('AVAILABLE', 'Available'),
        ('IN_USE', 'In Use'),
        ('MAINTENANCE', 'Maintenance'),
        ('DAMAGED', 'Damaged'),
        ('DISPOSED', 'Disposed'),
    )

    name = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ITEM_STATUS)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    reorder = models.BooleanField(default=False)
    location = models.CharField(max_length=200)
    last_maintained = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.name} - {self.model}"

class Checkout(models.Model):
    CHECKOUT_STATUS = (
        ('ACTIVE', 'Active'),
        ('OVERDUE', 'Overdue'),
        ('RETURNED', 'Returned'),
        ('LOST', 'Lost'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    condition_on_checkout = models.TextField()
    condition_on_return = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=CHECKOUT_STATUS)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.item.name} - {self.user.username}"

class MaintenanceRecord(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    performed_by = models.CharField(max_length=200)
    next_maintenance_date = models.DateTimeField()

    def __str__(self):
        return f"{self.item.name} - {self.date}"

class DisposalRecord(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    disposal_method = models.CharField(max_length=200)
    authorized_by = models.ForeignKey(User, on_delete=models.CASCADE)
    replacement_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item.name} - {self.date}"

class ReorderRequest(models.Model):
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    )
    
    REQUEST_STATUS = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('ORDERED', 'Ordered'),
        ('RECEIVED', 'Received'),
    )

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=REQUEST_STATUS)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.item.name} - {self.date}"
