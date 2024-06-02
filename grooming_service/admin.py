from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *


# Register the Service model with the admin interface
@admin.register(Service)
class ServiceAdmin(SummernoteModelAdmin):
    # Enable Summernote editor for 'description' and 'short_description' fields
    summernote_fields = ('description', 'short_description')
    list_display = ['name', 'vary_price1', 'vary_price2']


# Define an admin class for Appointment model
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'pet', 'status', 'start_date_time']


# Register the Appointment model with the custom AppointmentAdmin class
admin.site.register(Appointment, AppointmentAdmin)


# Define an admin class for Pet model
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'age', 'user', 'medical_notes']


# Register the Appointment model with the custom AppointmentAdmin class
admin.site.register(Pet, PetAdmin)


# Register the User model with the admin interface
admin.site.register(User)
