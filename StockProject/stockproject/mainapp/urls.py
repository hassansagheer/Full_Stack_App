from django.urls import path
from . import views

urlpatterns = [
    path('', views.stockPicker, name='stockepicker'),
    path('stocktracker', views.stockTracker, name='stocketracker'),
]
