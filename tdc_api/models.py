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
        return f"{self.first_name} {self.middle_name}. ID:- {self.pID}"

class AssignPatientToDoctor(models.Model):
    VISITSTATUS_TYPE = [
        ('Visited', 'Visited'),
        ('Reject', 'Reject'),
        ('Pending', 'Pending'),
    ]
    # visit
    # more than one service
    service = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='assign_service')
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE, related_name='patient_assign' )
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_assign')
    detail_description =  models.TextField(max_length=100, null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_assigner')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assign_update', null=True)
    archive_reason = models.CharField(max_length=255, null=True)
    assigned_at=models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Visited', 'Visited'),
            ('Reject', 'Reject'),
            ('Pending', 'Pending'),
        ],
        default='Pending'
    )
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
        return f"{self.product_name}:- from {self.manufacturer}"

class Product(models.Model):
    product_name = models.ForeignKey(ProductStore, on_delete=models.CASCADE, related_name='products_title')
    entry_quantity = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creater')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.entry_quantity
    
class Appointment(models.Model):
    APPOINTMENT_TYPE = [
        ('Checkup', 'Checkup'),
        ('Follow-Up', 'Follow-Up'),
        ('Treatment', 'Treatment'),
        ('Other', 'Other'),
    ]
    # appointed_by
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointed_patient')
    dentist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointer_dentist')
    appointment_date = models.DateTimeField()
    appointment_type = models.CharField(max_length=30, choices=APPOINTMENT_TYPE)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Scheduled', 'Scheduled'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Scheduled'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_updated', null=True)

    def __str__(self):
        return f'Appointment of {self.patient.first_name} with {self.dentist.first_name} on {self.appointment_date}'    

class Prescription(models.Model):
    PRESCRIPTION_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    ]
    dentist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriper_dentist')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriped_patient')
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='prescriped_service')
    product = models.ForeignKey(ProductStore, on_delete=models.CASCADE, related_name='prescriped_product')
    product_quantity = models.IntegerField()
    date_issued = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=30, choices=PRESCRIPTION_STATUS)

    def __str__(self):
        return f"Prescription of {self.patient}"
    
class Billing(models.Model):
    STATUS_TYPE = [
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('cancel', 'cancel'),
    ]
    bill_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  
    casher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='casher_name')  
    prescription = models.OneToOneField(Prescription, on_delete=models.CASCADE, related_name='prescription_bill')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remain_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_TYPE)

    def __str__(self):
        return self.bill_number