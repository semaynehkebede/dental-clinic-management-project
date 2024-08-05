from django.db import models
import uuid
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

class Patient(models.Model):
    GENDER_TYPE = [
        ('female', 'female'),
        ('male', 'male'),
    ]
    pID = models.CharField(max_length=30)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    dob = models.DateField()
    gender = models.CharField(max_length=50, choices=GENDER_TYPE)
    preferred_language = models.CharField(max_length=70)
    occupation = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30)
    email = models.CharField(max_length=40, null=True)
    previous_medical_condition = models.CharField(max_length=255, null=True)
    emergency_contact = models.CharField(max_length=40, null=True)
    sergical_history = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='patient_creater')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_updater', null=True)
    archive_reason = models.CharField(max_length=255, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='patient_delete')
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.firstName} {self.middleName}. ID:- {self.appointment_date}"

class AssignPatientToDoctor(models.Model):
    service = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='assign_service')
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE, related_name='patient_assign' )
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_assign')
    detail_description =  models.TextField(max_length=100, null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_assigner')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assign_update', null=True)
    archive_reason = models.CharField(max_length=255, null=True)
    assigned_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='assign_delete')
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
      return f"Assign {self.patient} to {self.doctor}"
    
class ProductStore(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    material_type = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_onstore_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_onstore_updated', null=True)
    archive_reason = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='product_onstore_deleted')
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name}:- from {self.manufacturer}"

class Product(models.Model):
    product_name = models.ForeignKey(ProductStore, on_delete=models.CASCADE, related_name='products_title')
    entry_quantity = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creater')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.entry_quantity
