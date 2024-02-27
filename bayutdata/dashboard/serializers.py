from rest_framework import serializers
from .models import BuildingInformation,ProjectInformation,ApartmentDetail



class BuildingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=BuildingInformation
        fields=['building_id','building_name','year_of_completion','total_floors','swimming_pools','total_parking_spaces','elevators']

class ProjectInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectInformation
        fields=['project_id','project_name','last_inspected','completion','handover']
    
class PricesAgainstProjectCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectInformation
        fields=['completion']

class PricesAgainstNumberOfRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApartmentDetail
        fields=['price','rooms']    

class PricesAgainstAreaOfApartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApartmentDetail
        fields=['price','area']   