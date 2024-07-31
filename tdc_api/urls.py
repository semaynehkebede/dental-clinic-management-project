from django.urls import include, path

from rest_framework_simplejwt.views import TokenRefreshView
from tdc_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'service-type', views.ServiceTypeViewSet, basename='sertype')
router.register(r'service', views.ServiceViewSet, basename='service')
router.register(r'materials', views.MaterialViewSet, basename='material')
router.register(r'patient', views.patientViewSet, basename='patient')

urlpatterns = [
    path('', views.index),
    path('users/get-users', views.GetUserView.as_view(), name='getUser'),
    path('users/get-user', views.GetUserByIdView.as_view(), name='getUserById'),
    path('users/create-user', views.RegisterUserView.as_view(), name='registerEmployee'),
    path('auth/login', views.UserLoginView.as_view(), name='userLogin'),
    path('auth/refresh', TokenRefreshView.as_view(), name='refreshToken'),
]

urlpatterns += router.urls