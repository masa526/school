from django.urls import path
from invoice import views

app_name = 'invoice'
urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
]
