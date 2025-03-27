from django import forms
from .models import InventoryItem, Checkout, MaintenanceRecord, DisposalRecord, ReorderRequest

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_category': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'reorder': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'last_maintained': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class UserManagementForm(forms.Form):
    action = forms.CharField(widget=forms.HiddenInput())
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    user_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    email = forms.EmailField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        if action in ['create', 'edit']:
            username = cleaned_data.get('username')
            if not username:
                self.add_error('username', 'Username is required.')
            if action == 'create':
                password = cleaned_data.get('password')
                if not password:
                    self.add_error('password', 'Password is required for creating a user.')
            first_name = cleaned_data.get('first_name')
            if not first_name:
                self.add_error('first_name', 'First name is required.')
            last_name = cleaned_data.get('last_name')
            if not last_name:
                self.add_error('last_name', 'Last name is required.')
            email = cleaned_data.get('email')
            if not email:
                self.add_error('email', 'Email is required.')
        elif action in ['delete', 'deactivate']:
            if not cleaned_data.get('user_id'):
                self.add_error('user_id', 'User ID is required for this action.')
        return cleaned_data