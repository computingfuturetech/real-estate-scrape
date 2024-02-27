from django.shortcuts import render
from django.core.cache import cache
from rest_framework import generics,status
from .models import BuildingInformation,ProjectInformation,ApartmentDetail,PropertyDetail
from .serializers import BuildingInformationSerializer,ProjectInformationSerializer,PricesAgainstProjectCompletionSerializer,PricesAgainstNumberOfRoomsSerializer,PricesAgainstAreaOfApartmentsSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


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


class PricesAgainstNumberOfRoomsViewSet(generics.RetrieveAPIView):
    queryset = ApartmentDetail.objects.all()
    serializer_class = PricesAgainstNumberOfRoomsSerializer

    def get(self, request, *args, **kwargs):
        try:
            to_rent = request.GET.get('to_rent')
            apartment_details = ApartmentDetail.objects.all()
            if to_rent:
                property_details = PropertyDetail.objects.filter(for_rent=to_rent)
                if property_details:
                    property_ids = property_details.values_list('property_id', flat=True)
                    apartment_details = apartment_details.filter(apartment_id__in=property_ids)
                else:
                    response_data={
                        'status':'Not Found'
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                list_of_filters = ['Yearly', 'Monthly', 'Daily', 'Weekly']
                rental_ids = set()
                for rent_type in list_of_filters:
                    property_details = PropertyDetail.objects.filter(for_rent=rent_type)
                    rental_ids.update(property_details.values_list('property_id', flat=True))
                    apartment_details = ApartmentDetail.objects.exclude(apartment_id__in=rental_ids)
            serializer = self.get_serializer(apartment_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PricesAgainstAreaOfApartmentsViewSet(generics.RetrieveAPIView):
    queryset = ApartmentDetail.objects.all()
    serializer_class = PricesAgainstAreaOfApartmentsSerializer

    def get(self, request, *args, **kwargs):
        try:
            to_rent = request.GET.get('to_rent')
            apartment_details = ApartmentDetail.objects.all()
            if to_rent:
                property_details = PropertyDetail.objects.filter(for_rent=to_rent)
                if property_details:
                    property_ids = property_details.values_list('property_id', flat=True)
                    apartment_details = apartment_details.filter(apartment_id__in=property_ids)
                else:
                    response_data={
                        'status':'Not Found'
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                list_of_filters = ['Yearly', 'Monthly', 'Daily', 'Weekly']
                rental_ids = set()
                for rent_type in list_of_filters:
                    property_details = PropertyDetail.objects.filter(for_rent=rent_type)
                    rental_ids.update(property_details.values_list('property_id', flat=True))
                    apartment_details = ApartmentDetail.objects.exclude(apartment_id__in=rental_ids)
            serializer = self.get_serializer(apartment_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)