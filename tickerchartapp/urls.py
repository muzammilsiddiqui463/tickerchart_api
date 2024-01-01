# tickerchartapp/urls.py

from django.urls import path
from .views import DataListCreateView, DataRetrieveUpdateDestroyView,start_,stop_,scraper
import threading


urlpatterns = [
    path('data/', DataListCreateView.as_view(), name='data-list-create'),
    path('data/<int:pk>/', DataRetrieveUpdateDestroyView.as_view(), name='data-retrieve-update-destroy'),
    path('start/', start_, name='start'),
    path('stop/', stop_, name='stop'),
]
print("started")
s = threading.Thread(target=scraper.run_process)
s.start()
