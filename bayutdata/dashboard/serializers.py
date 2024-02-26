from rest_framework import serializers
from .models import BuildingInformation,ProjectInformation



class BuildingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=BuildingInformation
        fields=['building_id','building_name','year_of_completion','total_floors','swimming_pools','total_parking_spaces','elevators']

class ProjectInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectInformation
        fields=['project_id','project_name','last_inspected','completion','handover']