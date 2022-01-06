from django.urls import path

from APIs.models import Profile
from . import views

urlpatterns = [
    path('communities/', views.community_list, name='community_list'),
    path('communities/<int:id>/', views.community_details, name='community_list'),
    path('card-transfers/', views.card_transfers, name='card_transfers'),
    path('bank-transfers/', views.bank_transfers, name='bank_transfers'),
    path('exchange/', views.exchange_rates, name='exchange_rates'),

    # path('profile/', views.Profile, name='profile')

]

