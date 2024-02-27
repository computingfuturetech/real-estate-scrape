from django.urls import path
from .views import test_redis,BuildingInformationViewSet,BuildingInformationUpdateViewSet,ProjectInformationViewSet

urlpatterns = [
    path('test-redis/', test_redis, name='test_redis'),
    path('buildinginfo/',BuildingInformationViewSet.as_view(),name='building-info'),
    path('projectinfo/',ProjectInformationViewSet.as_view(),name='project_info'),
    path('updateinfo/<int:building_id>/',BuildingInformationUpdateViewSet.as_view(),name='update-info'),
]
