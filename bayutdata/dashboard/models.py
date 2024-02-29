from django.db import models

class ApartmentDetail(models.Model):
    apartment_id = models.IntegerField(unique=True)
    price = models.IntegerField()
    rooms = models.IntegerField()
    baths = models.IntegerField()
    area = models.FloatField()
    title= models.CharField(max_length=500,blank=True,null=True)
    furnishing_status = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return str(self.apartment_id)
    
class BuildingInformation(models.Model):
    building_id = models.IntegerField(unique=True)
    building_name = models.CharField(max_length=500)
    year_of_completion=models.CharField(max_length=6)
    total_floors=models.CharField(max_length=5)
    swimming_pools=models.CharField(max_length=10)
    total_parking_spaces=models.CharField(max_length=10)
    elevators=models.CharField(max_length=5)

    def __str__(self):
        return str(self.building_id)

class ProjectInformation(models.Model):
    project_id= models.IntegerField(unique=True)
    project_name = models.CharField(max_length=500)
    last_inspected=models.CharField(max_length=500)
    completion=models.CharField(max_length=50)
    handover=models.CharField(max_length=500)


class ValidatedInformation(models.Model):
    validated_id= models.IntegerField(unique=True)
    developer = models.CharField(max_length=500)
    ownership=models.CharField(max_length=500)
    built_up_area=models.CharField(max_length=50)
    usage=models.CharField(max_length=500)
    balcony_size=models.CharField(max_length=500)
    total_building_area=models.CharField(max_length=500)
    parking_availability=models.CharField(max_length=500)


class PropertyDetail(models.Model):
    property_id= models.IntegerField(unique=True)
    type=models.CharField(max_length=50)
    purpose=models.CharField(max_length=50)
    completion=models.CharField(max_length=50,default='Ready')
    added_on=models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='Dubai')
    sub_state=models.CharField(max_length=100,default='Dubai Marina')
    rent_frequency=models.CharField(max_length=10,default='nan')


