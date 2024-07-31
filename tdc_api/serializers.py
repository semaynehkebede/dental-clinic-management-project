from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from tdc_api.models import Material, Patient, ServiceType, Services

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



# class ServiceSerializer(serializers.ModelSerializer):
#    serviceType = ServiceTypeSerializer()
#    class Meta:
#     model = Services
#     fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    isActive = serializers.BooleanField(default=True)
    quantity = serializers.IntegerField()
    avilableQuantity = serializers.IntegerField()
    class Meta:
        model = Material
        fields = '__all__'

    def validate_avilableQuantity(self, value):
        quantity = self.initial_data.get('quantity')
        if quantity is not None:
            quantity = int(quantity)  # Convert to int if needed
            if value > quantity:
              raise serializers.ValidationError("Avilable Quantity must be Less than or equal to the Quantity.")
        return value
    
class PatientSerializer(serializers.ModelSerializer):
   class Meta:
      model = Patient
      fields = '__all__'


class CreateServiceTypeSerializer(serializers.ModelSerializer):
  #  services = ServicesSerializer()
   class Meta:
    model = ServiceType
    fields = ['typeName', 'typeCode']


class GetServicesSerializer(serializers.ModelSerializer):
  #  serviceType = GetServiceTypeSerializer(many=True, read_only=True)
   class Meta:
    model = Services
    fields = '__all__'

class GetServiceTypeSerializer(serializers.ModelSerializer):
   serviceLists = GetServicesSerializer(many=True, read_only=True)
   class Meta:
    model = ServiceType
    fields =  ['id', 'typeName', 'typeCode', 'serviceLists']


class CreateServicesSerializer(serializers.ModelSerializer):
  #  serviceType = ServiceTypeSerializer()
   class Meta:
    model = Services
    fields = ['serviceType', 'serviceName', 'price']