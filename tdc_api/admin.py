from django.contrib import admin

from tdc_api.models import  Appointment, AssignPatientToDoctor, Patient, Product, ProductStore, ServiceType, Services

# Register your models here.

admin.site.register(Appointment)
admin.site.register(Patient)
admin.site.register(Product)
admin.site.register(ProductStore)
admin.site.register(AssignPatientToDoctor)
admin.site.register(Services)
admin.site.register(ServiceType)
