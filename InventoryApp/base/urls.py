from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('inventory/', views.InventoryView.as_view(), name='inventory'),
    path('checkouts/', views.CheckoutsView.as_view(), name='checkouts'),
    path('checkout/<int:pk>/', views.CheckoutItemView.as_view(), name='checkout'),
    path('checkin/<int:pk>/', views.CheckinItemView.as_view(), name='checkin'),
    path('maintenance/', views.MaintenanceView.as_view(), name='maintenance'),
    path('reorder/', views.ReorderView.as_view(), name='reorder'),
    path('add_item/', views.AddInventoryItemView.as_view(), name='add_item'),
    path('update_item/<int:pk>/', views.UpdateInventoryItemView.as_view(), name='update_item'),
    path('delete_item/<int:pk>/', views.DeleteInventoryItemView.as_view(), name='delete_item'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='base:home'), name='logout'),
]

