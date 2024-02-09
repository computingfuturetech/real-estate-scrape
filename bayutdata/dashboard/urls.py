from django.urls import path
from .views import ValidatedInformationView

urlpatterns = [
    path('csvdata/', ValidatedInformationView.as_view(), name='csvdata'),
]
