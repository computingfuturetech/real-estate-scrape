from rest_framework import serializers
from .models import BuildingInformation,ProjectInformation,ApartmentDetail,ValidatedInformation,PropertyDetail



class BuildingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=BuildingInformation
        fields=['building_id','building_name','year_of_completion','total_floors','swimming_pools','total_parking_spaces','elevators']

class ProjectInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectInformation
        fields=['project_id','project_name','completion','handover']

class ValidatedInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=ValidatedInformation
        fields=['validated_id','developer','ownership','usage']

class ApartmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApartmentDetail
        fields=['apartment_id','price','rooms','baths','area','furnishing_status','title']

class PropertyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=PropertyDetail
        fields=['property_id','purpose','completion','added_on','state','sub_state','rent_frequency']

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