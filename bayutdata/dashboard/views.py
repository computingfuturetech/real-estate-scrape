from django.shortcuts import render
from django.core.cache import cache
from rest_framework import generics,status
from .models import BuildingInformation,ProjectInformation,ApartmentDetail,ValidatedInformation,PropertyDetail
from .serializers import BuildingInformationSerializer,ProjectInformationSerializer,PricesAgainstProjectCompletionSerializer,ApartmentDetailSerializer,PropertyDetailSerializer
from .serializers import PricesAgainstNumberOfRoomsSerializer,PricesAgainstAreaOfApartmentsSerializer,ValidatedInformationSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min, Max, Avg
from rest_framework.pagination import PageNumberPagination
from math import ceil
from rest_framework.pagination import PageNumberPagination
import pandas as pd
import os
from django.conf import settings


def test_redis(request):
    cache.set('my_key', 'my_value')
    cached_value = cache.get('my_key')
    request.session['my_data'] = 'my_value'
    session_data = request.session.get('my_data')
    return render(request, 'test_redis.html', {
        'cached_value': cached_value,
        'session_data': session_data
    })

class BuildingInformationViewSet(generics.RetrieveAPIView):
    queryset = BuildingInformation.objects.all()
    serializer_class = BuildingInformationSerializer

    def get(self, request, *args, **kwargs):
        try:
            building_ids = request.GET.get('building_id')
            if building_ids:
                cache_key = f'building_info_{building_ids}' 
                building_information = cache.get(cache_key)
                if building_information is None:
                    building_information = get_object_or_404(BuildingInformation, building_id=building_ids)
                    cache.set(cache_key, building_information, timeout=60 * 15)
                    print('Data retrieved from database')
                else:
                    print('Data retrieved from cache')
                serializer = self.get_serializer(building_information)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                building_information=BuildingInformation.objects.all()
                all_building_ids = set(BuildingInformation.objects.values_list('building_id', flat=True))
                all_building_ids_cached = all(cache.get(f'building_info_{id}') for id in all_building_ids)
                if all_building_ids_cached:
                    building_information = []
                    for id in all_building_ids:
                        cache_key = f'building_info_{id}'
                        building_info = cache.get(cache_key)
                        if building_info is None:
                            raise ObjectDoesNotExist("Data not found in cache")
                        building_information.append(building_info)
                    print('All data retrieved from cache')
                else:
                    building_information = BuildingInformation.objects.all()
                    for building_info in building_information:
                        cache_key = f'building_info_{building_info.building_id}'
                        cache.set(cache_key, building_info, timeout=60 * 15)
                    print('Data retrieved from database')
                serializer = self.get_serializer(building_information,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BuildingInformationUpdateViewSet(generics.UpdateAPIView):
    queryset = BuildingInformation.objects.all()
    serializer_class = BuildingInformationSerializer
    def patch(self, request, *args, **kwargs):
        try:
            building_ids = kwargs.get('building_id')
            cache_key = f'building_info_{building_ids}'
            building_information = cache.get(cache_key)
            if building_information:
                cache.delete(cache_key)
            building_information = get_object_or_404(BuildingInformation, building_id=building_ids)
            serializer = BuildingInformationSerializer(building_information, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                cache.set(cache_key, building_information, timeout=60 * 15)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ProjectInformationViewSet(generics.RetrieveAPIView):
    queryset = ProjectInformation.objects.all()
    serializer_class = ProjectInformationSerializer

    def get(self, request, *args, **kwargs):
        try:
            project_ids = request.GET.get('project_id')
            if project_ids:
                cache_key = f'project_info_{project_ids}' 
                project_information = cache.get(cache_key)
                if project_information is None:
                    project_information = get_object_or_404(ProjectInformation, project_id=project_ids)
                    cache.set(cache_key, project_information, timeout=60 * 15)
                    print('Data retrieved from database')
                else:
                    print('Data retrieved from cache')
                serializer = self.get_serializer(project_information)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                project_information=ProjectInformation.objects.all()
                all_project_ids = set(ProjectInformation.objects.values_list('project_id', flat=True))
                all_project_ids_cached = all(cache.get(f'project_info_{id}') for id in all_project_ids)
                if all_project_ids_cached:
                    project_information = []
                    for id in all_project_ids:
                        cache_key = f'project_info_{id}'
                        project_info = cache.get(cache_key)
                        if project_info is None:
                            raise ObjectDoesNotExist("Data not found in cache")
                        project_information.append(project_info)
                    print('All data retrieved from cache')
                else:
                    project_information = ProjectInformation.objects.all()
                    for project_info in project_information:
                        cache_key = f'project_info_{project_info.project_id}'
                        cache.set(cache_key, project_info, timeout=60 * 15)
                    print('Data retrieved from database')
                serializer = self.get_serializer(project_information,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PricesAgainstProjectCompletionViewSet(generics.RetrieveAPIView):
    queryset = ProjectInformation.objects.all()
    serializer_class = PricesAgainstProjectCompletionSerializer

    def get(self, request, *args, **kwargs):
        try:
            projects = self.get_queryset()
            response_data = []
            for project in projects:
                project_id = project.project_id
                apartment_details = ApartmentDetail.objects.filter(apartment_id=project_id)
                if not apartment_details.exists():
                    continue                
                prices = [detail.price for detail in apartment_details if detail.price is not None]
                if not prices:
                    continue    
                serializer = self.get_serializer(project)
                project_data = serializer.data
                project_data['prices'] = prices
                response_data.append(project_data)
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def data_convert_into_interval_for_rooms(apartment_details):
    min_room = apartment_details.aggregate(min_room=Min('rooms'))['min_room']
    max_room = apartment_details.aggregate(max_room=Max('rooms'))['max_room']  
    num_midpoints = 7
    interval = (max_room - min_room) / (num_midpoints + 1)
    midpoints = [min_room]
    for i in range(1, num_midpoints + 1):
        midpoint = min_room + interval * i
        midpoints.append(midpoint)
    midpoints.append(max_room)
    interval_info = []
    for i in range(len(midpoints) - 1):
        start_point = round(midpoints[i], 1)
        end_point = round(midpoints[i + 1], 1)
        prices_within_interval = apartment_details.filter(rooms__gte=start_point, rooms__lte=end_point)
        average_price_result = prices_within_interval.aggregate(avg_price=Avg('price'))
        average_price = round(average_price_result['avg_price'], 1) if average_price_result['avg_price'] is not None else None
        min_price = prices_within_interval.aggregate(min_price=Min('price'))['min_price']
        max_price = prices_within_interval.aggregate(max_price=Max('price'))['max_price']
        if average_price is not None and min_price is not None and max_price is not None:
            interval_dict = {
                'start_point': start_point,
                'end_point': end_point,
                'average_price': average_price,
                'min_price': min_price,
                'max_price': max_price
            }
            interval_info.append(interval_dict)
    return interval_info      


class PricesAgainstNumberOfRoomsViewSet(generics.RetrieveAPIView):
    queryset = ApartmentDetail.objects.all()
    serializer_class = PricesAgainstNumberOfRoomsSerializer

    def get(self, request, *args, **kwargs):
        try:
            to_rent = request.GET.get('to_rent')
            apartment_details = ApartmentDetail.objects.all()
            if to_rent:
                property_details = PropertyDetail.objects.filter(rent_frequency=to_rent)
                if property_details:
                    property_ids = property_details.values_list('property_id', flat=True)
                    apartment_details = apartment_details.filter(apartment_id__in=property_ids)
                    interval_info=data_convert_into_interval_for_rooms(apartment_details)
                else:
                    response_data = {
                        'status': 'Not Found'
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                list_of_filters = ['Yearly', 'Monthly', 'Daily', 'Weekly']
                rental_ids = set()
                for rent_type in list_of_filters:
                    property_details = PropertyDetail.objects.filter(for_rent=rent_type)
                    rental_ids.update(property_details.values_list('property_id', flat=True))
                    if rental_ids: 
                        apartment_details = self.queryset.exclude(apartment_id__in=rental_ids)
                        interval_info = data_convert_into_interval_for_rooms(apartment_details)
                    else:
                        response_data = {
                            'status': 'Rental ids not found'
                        }
                        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            return Response(interval_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def data_convert_into_interval(apartment_details):
    min_area = apartment_details.aggregate(min_area=Min('area'))['min_area']
    max_area = apartment_details.aggregate(max_area=Max('area'))['max_area']
    num_midpoints = 7
    interval = (max_area - min_area) / (num_midpoints + 1)
    midpoints = [min_area]
    for i in range(1, num_midpoints + 1):
        midpoint = min_area + interval * i
        midpoints.append(midpoint)
    midpoints.append(max_area)
    print(midpoints)
    interval_info = []
    for i in range(len(midpoints) - 1):
        start_point = round(midpoints[i], 1)
        end_point = round(midpoints[i + 1], 1)
        prices_within_interval = apartment_details.filter(area__gte=start_point, area__lte=end_point)
        average_price_result = prices_within_interval.aggregate(avg_price=Avg('price'))
        average_price = round(average_price_result['avg_price'], 1) if average_price_result['avg_price'] is not None else None
        min_price = prices_within_interval.aggregate(min_price=Min('price'))['min_price']
        max_price = prices_within_interval.aggregate(max_price=Max('price'))['max_price']
        if average_price is not None and min_price is not None and max_price is not None:
            interval_dict = {
                'start_point': start_point,
                'end_point': end_point,
                'average_price': average_price,
                'min_price': min_price,
                'max_price': max_price
            }
            interval_info.append(interval_dict)
    return interval_info       


class PricesAgainstAreaOfApartmentsViewSet(generics.RetrieveAPIView):
    queryset = ApartmentDetail.objects.all()
    serializer_class = PricesAgainstAreaOfApartmentsSerializer
    def get(self, request, *args, **kwargs):
        try:
            to_rent = request.GET.get('to_rent')
            if to_rent:
                property_details = PropertyDetail.objects.filter(rent_frequency=to_rent)
                if property_details:
                    property_ids = property_details.values_list('property_id', flat=True)
                    apartment_details = self.queryset.filter(apartment_id__in=property_ids)
                    interval_info=data_convert_into_interval(apartment_details)
                else:
                    response_data = {
                        'status': 'Not Found'
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                list_of_filters = ['Yearly', 'Monthly', 'Daily', 'Weekly']
                rental_ids = set()
                for rent_type in list_of_filters:
                    property_details = PropertyDetail.objects.filter(for_rent=rent_type)
                    rental_ids.update(property_details.values_list('property_id', flat=True))
                if rental_ids: 
                    apartment_details = self.queryset.exclude(apartment_id__in=rental_ids)
                    interval_info = data_convert_into_interval(apartment_details)
                else:
                    response_data = {
                        'status': 'Rental ids not found'
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 
            return Response(interval_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20

class PropertyDetailViewSet(generics.ListAPIView):
    pagination_class = MyPagination

    def get_queryset(self):
        return ApartmentDetail.objects.all().order_by('id')
    
    def get(self, request, *args, **kwargs):
        apartment_details = self.get_queryset()
        total_apartments = apartment_details.count()
        page = self.paginate_queryset(apartment_details)
        serialized_data = [self.get_apartment_response_data(apartment_detail) for apartment_detail in page]
        total_pages = ceil(total_apartments / self.pagination_class.page_size)
        response_data = {
            'total_pages': total_pages,
            'apartments': serialized_data
        }

        return Response(response_data, status=status.HTTP_200_OK)
   
    def get_apartment_response_data(self, apartment_detail):
        apartment_id = apartment_detail.apartment_id

        building_information = BuildingInformation.objects.filter(building_id=apartment_id).first()
        validated_information = ValidatedInformation.objects.filter(validated_id=apartment_id).first()
        project_information = ProjectInformation.objects.filter(project_id=apartment_id).first()
        property_detail = PropertyDetail.objects.filter(property_id=apartment_id).first()

        building_data = self.get_building_response_data(building_information, apartment_id)
        validated_data = self.get_validated_response_data(validated_information, apartment_id)
        project_data = self.get_project_response_data(project_information, apartment_id)
        property_data = self.get_property_response_data(property_detail, apartment_id)

        response_item = {
            'apartment_detail': ApartmentDetailSerializer(apartment_detail).data,
            'building_information': building_data,
            'validated_information': validated_data,
            'project_information': project_data,
            'property_detail': property_data
        }
        return response_item

    def get_building_response_data(self, building_information, apartment_id):
        if building_information:
            return BuildingInformationSerializer(building_information).data
        else:
            return {
                'building_id': apartment_id,
                'building_name': "nan",
                'year_of_completion': "nan",
                'total_floors': "nan",
                'swimming_pools': "nan",
                'total_parking_spaces': "nan",
                'elevators': "nan"
            }

    def get_validated_response_data(self, validated_information, apartment_id):
        if validated_information:
            return ValidatedInformationSerializer(validated_information).data
        else:
            return {
                'validated_id': apartment_id,
                'developer': "nan",
                'ownership': "nan",
                'usage': "nan",
            }

    def get_project_response_data(self, project_information, apartment_id):
        if project_information:
            return ProjectInformationSerializer(project_information).data
        else:
            return {
                'project_id': apartment_id,
                'project_name': "nan",
                'completion': "nan",
                'handover': "nan",
            }

    def get_property_response_data(self, property_detail, apartment_id):
        if property_detail:
            return PropertyDetailSerializer(property_detail).data
        else:
            return {
                'property_id': apartment_id,
                'purpose': "nan",
                'completion':'nan',
                'added_on':'nan',
                'rent_frequency':'nan',
                'state':'Dubai',
                'sub_state':'Dubai Marina',
            }






    