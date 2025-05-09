from django.urls import include, path

from rest_framework_simplejwt.views import TokenRefreshView
from tdc_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'service-type', views.ServiceTypeViewSet, basename='sertype')
router.register(r'service', views.ServiceViewSet, basename='service')
router.register(r'store-item', views.ProductStoreViewSet, basename='store-item')
router.register(r'product', views.ProductViewSet, basename='product')
# router.register(r'materials', views.MaterialViewSet, basename='material')
router.register(r'patient', views.PatientViewSet, basename='patient')
router.register(r'appointment', views.AppointmentViewSet, basename='appointment')
router.register(r'prescription', views.PrescriptionViewSet, basename='prescription')
router.register(r'billing', views.BillingViewSet, basename='billing')
router.register(r'assign/patient-to-doctor', views.AssignPatientToDoctorViewSet, basename='patient_to_doctor')

urlpatterns = [
    path('', views.index),
    path('users/get-users', views.GetUserView.as_view(), name='getUser'),
    path('users/get-user', views.GetUserByIdView.as_view(), name='getUserById'),
    path('users/create-user', views.RegisterUserView.as_view(), name='registerEmployee'),
    path('auth/login', views.UserLoginView.as_view(), name='userLogin'),
    path('auth/refresh', TokenRefreshView.as_view(), name='refreshToken'),
]

urlpatterns += router.urls