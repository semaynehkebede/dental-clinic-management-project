from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.core.validators import MinValueValidator

from tdc_api.models import  Appointment, AssignPatientToDoctor, Billing, Patient, Prescription, Product, ProductStore, ServiceType, Services

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'first_name', 'last_name']
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
   password = serializers.CharField(write_only=True)
   
   class Meta:
    model = User
    fields = ['username', 'password', 'email']
    
    def create(self, validated_data):
      user = User.objects.create_user(
         username=validated_data['username'],
         password=validated_data['password'],
         email=validated_data.get('email', '')
         )
      return user


class UserLoginSerializer(serializers.ModelSerializer):
  username = serializers.CharField(max_length=10)
  class Meta:
    model = User
    fields = ['username', 'password']

class ServiceSerializer(serializers.ModelSerializer):
  #  serviceType = ServiceTypeSerializer()
   class Meta:
    model = Services
    fields = '__all__'

class ServiceTypeSerializer(serializers.ModelSerializer):
   services = ServiceSerializer(many=True, read_only=True)  # Reverse nested serialization
   class Meta:
    model = ServiceType
    # fields = '__all__'
    fields = ['id', 'typeCode', 'typeName', 'services']
# class MaterialSerializer(serializers.ModelSerializer):
#     isActive = serializers.BooleanField(default=True)
#     quantity = serializers.IntegerField()
#     avilableQuantity = serializers.IntegerField()
#     class Meta:
#         model = Material
#         fields = '__all__'

#     def validate_avilableQuantity(self, value):
#         quantity = self.initial_data.get('quantity')
#         if quantity is not None:
#             quantity = int(quantity)  # Convert to int if needed
#             if value > quantity:
#               raise serializers.ValidationError("Avilable Quantity must be Less than or equal to the Quantity.")
#         return value
    
class PatientSerializer(serializers.ModelSerializer):
   pID = serializers.CharField(required=False, allow_blank=True, allow_null=True)
   occupation = serializers.CharField(required=False, allow_blank=True, allow_null=True)
   email = serializers.CharField(required=False, allow_blank=True, allow_null=True)
   previous_medical_condition = serializers.CharField(required=False, allow_blank=True, allow_null=True)
   sergical_history = serializers.CharField(required=False, allow_blank=True, allow_null=True)


   class Meta:
      model = Patient
      fields = '__all__'
      
class AssignPatientToDoctorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
      model = AssignPatientToDoctor
      fields = '__all__'

class AssignPatientToDoctorSerializer(serializers.ModelSerializer):
   patient = PatientSerializer(read_only=True)
   service = ServiceTypeSerializer(read_only=True)
   doctor = UserSerializer(read_only=True)
   assigned_by = UserSerializer(read_only=True)
   class Meta:
      model = AssignPatientToDoctor
      fields = '__all__'

class ProductStoreSerializer(serializers.ModelSerializer):
   quantity = serializers.IntegerField(default = 0, validators=[MinValueValidator(0)])
   is_active = serializers.BooleanField(default = True)
   class Meta:
      model = ProductStore
      fields = '__all__'   

class ProductSerializer(serializers.ModelSerializer):
   class Meta:
      model = Product
      fields = '__all__'     
      
class AppointmentSerializer(serializers.ModelSerializer):
   status = serializers.CharField(default = 'Scheduled')
   patient = PatientSerializer(read_only = True)
   dentist = UserSerializer(read_only = True)
   class Meta:
      model = Appointment
      fields = '__all__'   

class AppointmentCreateUpdateSerializer(serializers.ModelSerializer):
   status = serializers.CharField(default = 'Scheduled')
   class Meta:
      model = Appointment
      fields = '__all__'  

class PrescriptionSerializer(serializers.ModelSerializer):
   patient = PatientSerializer(read_only = True)
   dentist = UserSerializer(read_only = True)
   service = ServiceSerializer(read_only =True)
   product = ProductStoreSerializer(read_only = True)
   class Meta:
      model = Prescription
      fields = '__all__'

class PrescriptionCreateUpdateSerializer(serializers.ModelSerializer):
   status = serializers.CharField(default = 'Pending')
   class Meta:
      model = Prescription
      fields = '__all__'      

class BillingSerializer(serializers.ModelSerializer):
   remain_amount = serializers.DecimalField(decimal_places=2, max_digits=10, default = 0.00)
   status = serializers.CharField(default = 'pending')
   casher = UserSerializer(read_only = True)
   prescription = PrescriptionSerializer(read_only = True)
   class Meta:
      model = Billing
      fields = '__all__'

class BillingCreateUpdateSerializer(serializers.ModelSerializer):
   class Meta:
      model = Billing
      fields = '__all__'      