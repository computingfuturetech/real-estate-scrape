from django.urls import path
from .views import CSVDataView

urlpatterns = [
    path('csvdata/', CSVDataView.as_view(), name='csvdata'),
]
