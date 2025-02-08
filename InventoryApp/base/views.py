from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InventoryItem
from django.views import View
from .forms import InventoryItemForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse

class HomeView(TemplateView):
    template_name = 'home.html'

class InventoryView(LoginRequiredMixin, View):
    template_name = 'inventory.html'
    
    def get(self, request):
        form = InventoryItemForm()
        inventory_items = InventoryItem.objects.all()
        return render(request, self.template_name, {
            'add_item_form': form,
            'inventory_items': inventory_items
        })

class AddInventoryItemView(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    success_url = reverse_lazy('base:inventory')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        return redirect('base:inventory')
    
class UpdateInventoryItemView(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    success_url = reverse_lazy('base:inventory')
    template_name = 'inventory.html'

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        return redirect('base:inventory')

class DeleteInventoryItemView(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    success_url = reverse_lazy('base:inventory')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('base:inventory')
    
class CheckoutsView(LoginRequiredMixin, TemplateView):
    template_name = 'checkouts.html'

    login_url = 'base:login'


class MaintenanceView(LoginRequiredMixin, TemplateView):
    template_name = 'maintenance.html'
    login_url = 'base:login'


class ReorderView(LoginRequiredMixin, TemplateView):
    template_name = 'reorder.html'
    login_url = 'base:login'




