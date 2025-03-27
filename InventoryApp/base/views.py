from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InventoryItem, Checkout
from django.views import View
from .forms import InventoryItemForm, UserManagementForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

class HomeView(TemplateView):
    template_name = 'home.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('base:login')
        else:
            return redirect('base:inventory')
        
class InventoryView(LoginRequiredMixin, FormView):
    template_name = 'inventory.html'
    model = InventoryItem
    form_class = InventoryItemForm
    login_url = 'base:login'
    success_url = reverse_lazy('base:inventory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_items'] = self.model.objects.all()
        return context
    
    def post(self, request):
        if 'update_item' in request.POST:
            item_id = request.POST.get('itemId')
            item = get_object_or_404(InventoryItem, pk=item_id)
            form = InventoryItemForm(request.POST, instance=item)
    
            if form.is_valid():
                form.save()
                return redirect('base:inventory')
    
        elif 'add_item' in request.POST:
            form = InventoryItemForm(request.POST)
    
            if form.is_valid():
                item = form.save(commit=False)
                item.last_maintained = timezone.now()
                item.save()
                return redirect('base:inventory')

class DeleteInventoryItemView(LoginRequiredMixin, View):
    template_name = 'confirm_delete.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = InventoryItem.objects.get(pk=self.kwargs['pk']).name
        return context

    def get(self, request, pk):
        item = get_object_or_404(InventoryItem, pk=pk)
        return render(request, self.template_name, {'item': item})

    def post(self, request, pk):
        item = get_object_or_404(InventoryItem, pk=pk)
        item.delete()
        return redirect(reverse_lazy('base:inventory'))

class CheckoutsView(LoginRequiredMixin, TemplateView):
    template_name = 'checkouts.html'
    login_url = 'base:login'
    model = Checkout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checkouts = Checkout.objects.filter(return_date__isnull=True)

        checkout_history = Checkout.objects.filter(return_date__isnull=False)
        context['checkouts'] = checkouts
        context['checkout_history'] = checkout_history

        return context

class CheckinItemView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        last_checkout = Checkout.objects.get(id=self.kwargs['pk'])
        if last_checkout:
            print("here")
            last_checkout.return_date = timezone.now()
            last_checkout.due_date = timezone.now() + timedelta(days=7)
            last_checkout.save()


        InventoryItem.objects.filter(pk=last_checkout.item.id).update(status='Availible')
        
        return redirect(reverse_lazy('base:checkouts'))

class CheckoutItemView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        Checkout.objects.create(
            user=request.user,
            item=InventoryItem.objects.get(pk=self.kwargs['pk']),
            checkout_date=timezone.now(),
            due_date=timezone.now() + timedelta(days=7),
        )
        InventoryItem.objects.filter(pk=self.kwargs['pk']).update(status='CHECKED OUT')
        
        return redirect(reverse_lazy('base:inventory'))

class MaintenanceView(LoginRequiredMixin, TemplateView):
    template_name = 'maintenance.html'
    login_url = 'base:login'

class ReorderView(LoginRequiredMixin, TemplateView):
    template_name = 'reorder.html'
    login_url = 'base:login'

class UserManagementView(LoginRequiredMixin, FormView):
    template_name = 'user_management.html'
    login_url = 'base:login'
    form_class = UserManagementForm
    success_url = reverse_lazy('base:user_management')

    def form_valid(self, form):
        action = form.cleaned_data.get('action')
        print('Action:', action)  # Debug log
        
        if action == 'create':
            print('Create')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
        elif action == 'edit':
            print('Edit')
            user_id = form.cleaned_data.get('user_id')
            user = get_object_or_404(User, id=user_id)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            if password:
                user.set_password(password)
            user.save()
        elif action == 'delete':
            print('Delete')
            user_id = form.cleaned_data.get('user_id')
            user = get_object_or_404(User, id=user_id)
            print("Deleting user:", user)
            user.delete()
        elif action == 'deactivate':
            print('Deactivate')
            user_id = form.cleaned_data.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.is_active = False
            user.save()
            print("User deactivated:", user)
        else:
            print('No valid action provided')
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context
