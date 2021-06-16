from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='booking-login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='booking-login'),
    path('list/', AppointmentListView.as_view(), name='booking-list'),
    path('create/', AppointmentFormView.as_view(), name='booking-create'),
    path('details/<int:pk>/', AppointmentDetailView.as_view(), name='booking-detail'),
    path('details/<int:pk>/update/', AppointmentUpdateView.as_view(), name='booking-update'),
    path('details/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='booking-delete'),
    path('search/', AppointmentSearchView, name='booking-search'),
    path('logs/', AppointmentLogsView, name='booking-logs')
]