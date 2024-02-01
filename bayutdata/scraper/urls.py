from django.urls import path
from .views import CSVDataView,HelloWorldView

urlpatterns = [
    path('csvdata/', CSVDataView.as_view(), name='csvdata'),
    path('hello/',HelloWorldView.as_view(), name='hello_world'),
]
