from django.db import models




class ApartmentDetail(models.Model):
    apartment_id = models.IntegerField(unique=True)
    price = models.IntegerField()
    rooms = models.IntegerField()
    baths = models.IntegerField()
    area = models.FloatField()
    furnishing_status = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return str(self.apartment_id)
    
class BuildingInformation(models.Model):
    building_id = models.IntegerField(unique=True)
    building_name = models.CharField(max_length=500)
    year_of_completion=models.CharField(max_length=5)
    total_floors=models.CharField(max_length=5)
    swimming_pools=models.CharField(max_length=10)
    total_parking_spaces=models.CharField(max_length=10)
    elevators=models.CharField(max_length=5)

    def __str__(self):
        return str(self.building_id)
