from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework import viewsets, mixins

from tdc_api.authentication import CustomJWTAuthentication
from tdc_api.models import  Appointment, AssignPatientToDoctor, Billing, Patient, Prescription, Product, ProductStore, ServiceType, Services
from tdc_api.serializers import  AppointmentCreateUpdateSerializer, AppointmentSerializer, AssignPatientToDoctorCreateUpdateSerializer, AssignPatientToDoctorSerializer, BillingCreateUpdateSerializer, BillingSerializer, CreateUserSerializer, PatientSerializer, PrescriptionCreateUpdateSerializer, PrescriptionSerializer, ProductSerializer, ProductStoreSerializer, ServiceSerializer, ServiceTypeSerializer, UserLoginSerializer, UserSerializer

# Create your views here.
@api_view(['GET'])
def index(request):
    return Response({"success":"Success Api create", 
                     "login":"http://192.168.0.102:8000/api/auth/login", 
                     "refresh-token":"http://192.168.0.102:8000/api/auth/auth/refresh", 

                     "To Get User":"http://192.168.0.102:8000/api/users/get-users",
                     "To Get User by id(id sent by form data)":"http://192.168.0.102:8000/api/users/get-user",
                     "To Create User":"http://192.168.0.102:8000/api/users/create-user",

                     "To Get Service Type List":"http://192.168.0.102:8000/api/service-type",
                     "To Get Service Type By ID":"http://192.168.0.102:8000/api/service-type/id",
                     "To Create Service Type":"http://192.168.0.102:8000/api/service-type/",
                     "To delete service type" : "192.168.0.102:8000/api/service-type/id/",

                     "To Get Services List":"http://192.168.0.102:8000/api/service",
                     "To Get Services By ID":"http://192.168.0.102:8000/api/service/id",
                     "To Create Service":"http://192.168.0.102:8000/api/service/",

                     "To Get store-item List":"http://192.168.0.102:8000/api/store-item",
                     "To Get store-item By ID":"http://192.168.0.102:8000/api/store-item/id",
                     "To Create store-item":"http://192.168.0.102:8000/api/store-item/",
                     "To Soft Delete store-item. archiveReason, deletedBy, updatedBy value send from form" :"http://192.168.0.102:8000/api/store-item/id/",
                     
                     "To Get product List":"http://192.168.0.102:8000/api/product",
                     "To Get product By ID":"http://192.168.0.102:8000/api/product/id",
                     "To Create product":"http://192.168.0.102:8000/api/product/",
                     
                     "To Get Patient List":"http://192.168.0.102:8000/api/patient",
                     "To Get Patient By ID":"http://192.168.0.102:8000/api/patient/id",
                     "To Create Patient":"http://192.168.0.102:8000/api/patient/",
                     "To update Patient":"http://192.168.0.102:8000/api/patient/id/",
                    #  "To Soft Delete Patient. archiveReason, deletedBy, updatedBy value send from form" :"http://192.168.0.102:8000/api/patient/id/"
  
                     "To Get Patients Assigned to Doctor List":"http://192.168.0.102:8000/api/assign/patient-to-doctor",
                     "To Get Patients Assigned to Doctor By ID":"http://192.168.0.102:8000/api/assign/patient-to-doctor/id",
                     "To Assigned Patients to Doctor":"http://192.168.0.102:8000/api/assign/patient-to-doctor/",
                     "To update Patient":"http://192.168.0.102:8000/api/assign/patient-to-doctor/id/",

                     
                     "To Get prescription List":"http://192.168.0.102:8000/api/prescription",
                     "To Get prescription By ID":"http://192.168.0.102:8000/api/prescription/id",
                     "To Create prescription":"http://192.168.0.102:8000/api/prescription/",
                     "To update prescription":"http://192.168.0.102:8000/api/prescription/id/",

                     "To Get appointment List":"http://192.168.0.102:8000/api/appointment",
                     "To Get appointment By ID":"http://192.168.0.102:8000/api/appointment/id",
                     "To Create appointment":"http://192.168.0.102:8000/api/appointment/",
                     "To update appointment":"http://192.168.0.102:8000/api/appointment/id/",

                     
                     "To Get billing List":"http://192.168.0.102:8000/api/billing",
                     "To Get billing By ID":"http://192.168.0.102:8000/api/billing/id",
                     "To Create billing":"http://192.168.0.102:8000/api/billing/",
                     "To update billing":"http://192.168.0.102:8000/api/billing/id/",
                     })


class GetUserView(APIView):
  # authentication_classes = [CustomJWTAuthentication]
#   permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    user=User.objects.all()
    serializer = UserSerializer(user, many=True)
    if(serializer.data):
      return Response({'data' : serializer.data, 'count' : len(serializer.data)}, status=201)
    return Response({'status':200, 'payload':"Empty Data"})
  

class GetUserByIdView(APIView):
  def get(self, request, format = None):
    # employeeId sent by form data from end point as request
    userId = request.data.get('id')
    try:
      user = User.objects.get(id=userId)
      serializer=UserSerializer(user)
      return Response(serializer.data)
    except User.DoesNotExist:
      return Response({"Error": "User does not exist"}, status=404)
    except Exception as e:
      return Response({"success": False, "error": str(e)}, status=500)
    
class RegisterUserView(APIView):
  # authentication_classes = [CustomJWTAuthentication]
  def post(self, request, format=None):
    serializer=CreateUserSerializer(data=request.data, many=True)
    if serializer.is_valid():
       serializer.save()
       return Response({'user':serializer.data, 'message':'Registration Successful'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
def get_tokens(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }
class UserLoginView(APIView):
  def post(self, request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    password = serializer.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
      token = get_tokens(user)
      return Response({'message':'Login Success','userId':user.id, 'userName':user.username, 'token':token}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':'Email or Password is not Valid'}, status=status.HTTP_404_NOT_FOUND)

class ServiceViewSet(viewsets.ViewSet):

  # authentication_classes = [CustomJWTAuthentication]
  def list(self, request):
    queryset = Services.objects.all()
    serializer = ServiceSerializer(queryset, many=True)
    if(serializer.data):
      return Response({'data':serializer.data, 'count':len(serializer.data)}, status=200)
    return Response(status=status.HTTP_204_NO_CONTENT)
  
  # authentication_classes = [CustomJWTAuthentication]
  def create(self, request):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  # authentication_classes = [CustomJWTAuthentication]
  def retrieve(self, request, pk=None):
    queryset = Services.objects.all()
    serviceData = get_object_or_404(queryset, pk=pk)
    serializer = ServiceSerializer(serviceData)
    return Response(serializer.data)
  
  # authentication_classes = [CustomJWTAuthentication]
  def update(self, request, pk=None):
        try:
            serviceData = Services.objects.get(pk=pk)
        except Services.DoesNotExist:
            return Response({"errors" : "No service by this id"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ServiceSerializer(serviceData, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # authentication_classes = [CustomJWTAuthentication]
  def destroy(self, request, pk=None):
    try:
      serviceTypeData = Services.objects.get(pk=pk)
    except Services.DoesNotExist:
      return Response({'errors':'No Data by this parameter'}, status=status.HTTP_404_NOT_FOUND)
    
    serviceTypeData.delete()
    return Response({'success':'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)

class ServiceTypeViewSet(viewsets.ViewSet):
  def list(self, request):
    queryset = ServiceType.objects.all()
    serializer = ServiceTypeSerializer(queryset, many=True)
    if(serializer.data):
      return Response({'data':serializer.data, 'count':len(serializer.data)}, status=200)
    return Response(status=status.HTTP_204_NO_CONTENT)
  
  def create(self, request):
    serializer = ServiceTypeSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def retrieve(self, request, pk=None):
    queryset = ServiceType.objects.all()
    serviceTypeData = get_object_or_404(queryset, pk=pk)
    serializer = ServiceTypeSerializer(serviceTypeData)
    return Response(serializer.data)
  
  # authentication_classes = [CustomJWTAuthentication]
  def update(self, request, pk=None):
        try:
            serviceTypeData = ServiceType.objects.get(pk=pk)
        except ServiceType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ServiceTypeSerializer(serviceTypeData, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # authentication_classes = [CustomJWTAuthentication]
  def destroy(self, request, pk=None):
    try:
      serviceTypeData = ServiceType.objects.get(pk=pk)
    except ServiceType.DoesNotExist:
      return Response({'errors':'No Data by this parameter'}, status=status.HTTP_404_NOT_FOUND)
    
    serviceTypeData.delete()
    return Response({'success':'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
  
class PatientViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin
                     ):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Prepare the custom response
        # response_data = {
        #     "count": len(serializer.data),
        #     "data": serializer.data
        # }
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        # Partially update an existing object.
        partial = kwargs.pop('partial', False)  # Check if this is a partial update
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AssignPatientToDoctorViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):
    queryset = AssignPatientToDoctor.objects.all()
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AssignPatientToDoctorSerializer
        return AssignPatientToDoctorCreateUpdateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Prepare the custom response
        # response_data = {
        #     "count": len(serializer.data),
        #     "data": serializer.data
        # }
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        # Partially update an existing object.
        partial = kwargs.pop('partial', False)  # Check if this is a partial update
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
class ProductStoreViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):
   
   queryset = ProductStore.objects.all()
   serializer_class = ProductStoreSerializer

  #  def perform_create(self, serializer):
  #       serializer.save(created_by=self.request.user)

   def perform_create(self, serializer):
        # Set the quantity to 0 for new instances
        serializer.save(quantity=0)

  
   def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Prepare the custom response
        response_data = {
            "count": len(serializer.data),
            "data": serializer.data
        }
        return Response(response_data)

class ProductViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin) :
   
   queryset = Product.objects.all()
   serializer_class = ProductSerializer

   def perform_create(self, serializer):
        # Save the new Product instance
        instance = serializer.save()

        # Now update the related ProductStore quantity
        ProductStore = instance.product_name

        # Add new registered quantity to old quantity on the store
        ProductStore.quantity =  ProductStore.quantity + instance.entry_quantity  
        ProductStore.save()

        # you can return the instance
        return instance
   
class AppointmentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, 
                         mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                           mixins.CreateModelMixin):
   
   queryset = Appointment.objects.all()
   def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AppointmentSerializer
        return AppointmentCreateUpdateSerializer

   def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Prepare the custom response
        response_data = {
            "count": len(serializer.data),
            "data": serializer.data
        }
        return Response(response_data)
   
class PrescriptionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin):
   
   queryset = Prescription.objects.all()

   def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PrescriptionSerializer
        return PrescriptionCreateUpdateSerializer

   def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Prepare the custom response
        response_data = {
            "count": len(serializer.data),
            "data": serializer.data
        }
        return Response(response_data)
   
   def perform_create(self, serializer):
        # Save the new Prescription instance
        instance = serializer.save()

        # Now update the related ProductStore quantity
        ProductStore = instance.product

        # substract new Prescriped quantity from old quantity on the store
        ProductStore.quantity =  ProductStore.quantity - instance.product_quantity  
        ProductStore.save()

        # you can return the instance
        return instance
   
class BillingViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin):
   
   queryset = Billing.objects.all()
   def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BillingSerializer
        return BillingCreateUpdateSerializer
  #  serializer_class = BillingSerializer
   
   def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Prepare the custom response
        response_data = {
            "count": len(serializer.data),
            "data": serializer.data
        }
        return Response(response_data)
   
   def perform_create(self, serializer):
        # Save the new Billing instance
        instance = serializer.save()

        # Now update the related PrescriptionStatus
        Prescription = instance.prescription

        # update prescription to approved
        if instance.status == 'completed':
           Prescription.status =  'Approved'  
        Prescription.save()

        # you can return the instance
        return instance