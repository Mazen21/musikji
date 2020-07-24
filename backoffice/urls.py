from django.urls import path, include
from backoffice import views as backoffice_views

app_name = "backoffice"

urlpatterns = [
    path('', backoffice_views.home, name="home"),
    path('tickets/', backoffice_views.tickets, name="tickets"),
    path('tickets/<int:ticket_id>', backoffice_views.ticket_detail, name="ticket_detail")
]