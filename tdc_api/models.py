from django.db import models

from tana_dental_clinic import settings
from django.contrib.auth.models import User

# Create your models here.
class ServiceType(models.Model):
    typeName = models.CharField(max_length=30)
    typeCode = models.CharField(max_length=5)
class Services(models.Model):
    serviceType = models.ForeignKey(ServiceType, related_name='services', on_delete=models.CASCADE)
    serviceName = models.CharField(max_length= 255)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    # discountPrice = models.DecimalField(decimal_places=2, max_digits=10)


class Material(models.Model):
    MATERIAL_TYPE = [
        ('consumable', 'Consumable'),
        ('equipment', 'Equipment'),
        ('furnishing', 'Furnishing'),
        ('other', 'other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    avilableQuantity = models.PositiveIntegerField()
    material_type = models.CharField(max_length=50, choices=MATERIAL_TYPE)
    supplier = models.CharField(max_length=255)
    expiration_date = models.DateField(blank=True, null=True)
    isActive = models.BooleanField(default=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='materialCreatedBy')
    updatedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='materialUpdatedBy', null=True)
    archiveReason = models.CharField(max_length=255, null=True)
  # auto_now_add=True(meanse the value not changed when we update the data)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
  # auto_now=True(meanse the value updated when we update the data)
    deletedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='materialDeletedBy')
    deletedAt = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name
    

class Patient(models.Model):
    GENDER_TYPE = [
        ('female', 'female'),
        ('male', 'male'),
    ]
    pID = models.CharField(max_length=30)
    firstName = models.CharField(max_length=20)
    middleName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    dob = models.DateField()
    gender = models.CharField(max_length=50, choices=GENDER_TYPE)
    preferredLanguage = models.CharField(max_length=70)
    occupation = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=30)
    email = models.CharField(max_length=40, null=True)
    previousMedicalCondition = models.CharField(max_length=255, null=True)
    emergencyContact = models.CharField(max_length=40, null=True)
    sergicalHistory = models.CharField(max_length=255, null=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE,related_name='patientCreatedBy')
    updatedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patientUpdatedBy', null=True)
    archiveReason = models.CharField(max_length=255, null=True)
  # auto_now_add=True(meanse the value not changed when we update the data)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
  # auto_now=True(meanse the value updated when we update the data)
    deletedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='patientDeletedBy')
    deletedAt = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return self.pID