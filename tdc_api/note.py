# Appointment: Represents a scheduled appointment.
# Treatment: Represents the treatment performed during an appointment.
# Prescription: Represents any medication prescribed during a treatment.
# Billing: Represents billing details associated with a treatment or appointment.


# +----------------+           +----------------+           +----------------+
# |  Appointment   |           |   Treatment    |           |  Prescription  |
# +----------------+           +----------------+           +----------------+
# | id             |           | id             |           | id             |
# | patient        |<--1-to-1--| appointment    |--1-to-1--> | treatment      |
# | dentist        |           | treatment_date |           | medication_name|
# | appointment_date|           | treatment_type |           | dosage         |
# | reason_for_visit|           | description    |           | frequency      |
# +----------------+           | cost           |           | start_date     |
#                              | notes          |           | end_date       |
#                              +----------------+           | instructions   |
#                                       |                  +----------------+
#                                       |
#                                       | 1-to-1
#                                       |
#                              +----------------+
#                              |    Billing     |
#                              +----------------+
#                              | id             |
#                              | treatment      |
#                              | amount         |
#                              | payment_date   |
#                              | payment_method |
#                              | status         |
#                              +----------------+




# myapp/models.py
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Dentist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, related_name='appointments', on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, related_name='appointments', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason_for_visit = models.CharField(max_length=255)

    def __str__(self):
        return f"Appointment for {self.patient} with {self.dentist} on {self.appointment_date}"

class Treatment(models.Model):
    appointment = models.OneToOneField(Appointment, related_name='treatment', on_delete=models.CASCADE)
    treatment_date = models.DateField()
    treatment_type = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Treatment for {self.appointment.patient} on {self.treatment_date}"

class Prescription(models.Model):
    treatment = models.OneToOneField(Treatment, related_name='prescription', on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.treatment}"

class Billing(models.Model):
    treatment = models.OneToOneField(Treatment, related_name='billing', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])

    def __str__(self):
        return f"Billing for {self.treatment} - {self.amount}"