from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from grooming_service.forms import *
from .models import Service


# Register view
def register(request):
    # Handle POST request
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data["password"])
            user.first_name = form.cleaned_data["first_name"].title()
            user.last_name = form.cleaned_data["last_name"].title()
            user.save()
            login(request, user)
            messages.success(request, "Your account has been created! Logging you in...", extra_tags="register_form")
        else:
            __handle_form_errors(request, form, extra_tags="register_form")
    else:
        form = RegistrationForm()
    return render(request, "grooming_service/register.html", {"form": form})


# User login view
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "Login successful. Please wait...",
                                 extra_tags="login_form")
            else:
                messages.error(request, "Invalid email or password", extra_tags="login_form")
    else:
        form = LoginForm()
    return render(request, "grooming_service/login.html", {"form": form})


# User logout view
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def not_found(request):
    return render(request, "404.html")


# Home view
def home(request):
    home_services = Service.objects.exclude(short_description__exact='').order_by('-id')
    return render(request, "grooming_service/home.html", {'home_services': home_services})


# About view
def about(request):
    return render(request, "grooming_service/about.html")


# Get services view
def get_services(request):
    services = Service.objects.all()
    return render(request, "grooming_service/services.html", {'services': services})


# Book appointment view
@login_required(login_url='login')
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            start_date_time = form.cleaned_data["start_date_time"]
            description = form.cleaned_data["description"]
            pet = form.cleaned_data["pet"]
            service = form.cleaned_data["service"]
            try:
                check_appointment = Appointment.objects.get(start_date_time=start_date_time, status=1)
                messages.error(request, "The selected appointment is already booked.",
                               extra_tags="book_appointment_form")
            except Appointment.DoesNotExist:
                appointment = Appointment(user=request.user,
                                          pet=pet,
                                          status=1,
                                          service=service,
                                          start_date_time=start_date_time,
                                          description=description)
                appointment.save()
                messages.success(request,
                                 "Your appointment has been successfully created! Redirecting you to profile page...",
                                 extra_tags="book_appointment_form")
        else:
            messages.error(request, "There was an error booking this appointment.", extra_tags="book_appointment_form")
    else:
        form = AppointmentForm(user=request.user)
    return render(request, "grooming_service/appointment.html", {"form": form})


@login_required(login_url='login')
def edit_profile(request):
    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data["password"])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request,
                             "Your profile has been successfully saved with the new changes. Redirecting you to profile page...",
                             extra_tags="edit_profile_form")
        else:
            __handle_form_errors(request, form, extra_tags="edit_profile_form")

    else:
        form = EditUserForm(instance=request.user)
    return render(request, 'grooming_service/edit_profile.html', {'form': form})


# Manage profile view
@login_required(login_url='login')
def manage_profile(request):
    appointmentForm = AppointmentForm(request.POST or None, user=request.user)
    petForm = PetForm(request.POST or None, request.FILES)
    editPetForm = EditPetForm(request.POST or None, request.FILES)

    if request.method == "POST":
        form_type = request.POST.get('form_type')
        __handle_form_case(request, appointmentForm, petForm, editPetForm, form_type)

    appointments = Appointment.objects.filter(user=request.user).order_by('start_date_time')
    pets = Pet.objects.filter(user=request.user).order_by('name')
    return render(request, "grooming_service/profile.html", {
        'appointmentForm': appointmentForm,
        'appointments': appointments,
        'pets': pets,
        'petForm': petForm,
        'editPetForm': editPetForm
    })


def __handle_form_case(request, appointmentForm, petForm, editPetForm, form_type):
    match form_type:
        case 'edit_appointment_form':
            if appointmentForm.is_valid():
                __handle_edit_appointment_form(request, appointmentForm)
            else:
                __handle_form_errors(request, appointmentForm, 'edit_appointment_form')
        case 'pet_form':
            if petForm.is_valid():
                __handle_pet_add_form(request, petForm)
            else:
                __handle_form_errors(request, petForm, 'add_pet_form')
        case 'edit_pet_form':
            if editPetForm.is_valid():
                __handle_pet_edit_form(request, editPetForm)
            else:
                __handle_form_errors(request, editPetForm, 'edit_pet_form')


def __handle_form_errors(request, form, extra_tags):
    if '__all__' in form.errors:
        for error in form.errors['__all__']:
            messages.error(request, error, extra_tags=extra_tags)


def __handle_edit_appointment_form(request, appointmentForm):
    appointment_id = request.POST.get("appointment_id")
    start_date_time = request.POST.get("start_date_time")
    description = appointmentForm.cleaned_data["description"]
    pet = appointmentForm.cleaned_data["pet"]
    service = appointmentForm.cleaned_data["service"]
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        request_date_time_obj = datetime.strptime(start_date_time, '%Y-%m-%d %H:%M')
        formatted_date_time = request_date_time_obj.strftime('%Y-%m-%d %H:%M')
        if appointment.start_date_time.strftime('%Y-%m-%d %H:%M') != formatted_date_time:
            if Appointment.objects.filter(start_date_time=formatted_date_time, status=1).exists():
                messages.error(request, "The selected appointment slot is no longer available", extra_tags='edit_appointment_form')
            else:
                appointment.start_date_time = request_date_time_obj
                appointment.pet = pet
                appointment.service = service
                appointment.description = description
                appointment.save()
                messages.success(request, "Your appointment has been successfully updated. Redirecting you to profile page...",
                                 extra_tags='edit_appointment_form')
    except Appointment.DoesNotExist:
        messages.error(request, "The requested appointment does not exist")
        return redirect('not_found')


def __handle_pet_edit_form(request, editPetForm):
    pet_id = request.POST.get("pet_id")
    name = editPetForm.cleaned_data["name"]
    breed = editPetForm.cleaned_data["breed"]
    age = editPetForm.cleaned_data["age"]
    image = editPetForm.cleaned_data["image"]
    medical_notes = editPetForm.cleaned_data["medical_notes"]
    try:
        pet = Pet.objects.get(id=pet_id)
        pet.name = name.title()
        pet.breed = breed.title()
        pet.age = age
        if image != 'media/images/tey9seavfcldmybatmmt':
            pet.image = image
        pet.medical_notes = medical_notes
        pet.save()
        messages.success(request, f"{pet.name} has been successfully updated. Redirecting you to profile page...",
                         extra_tags='edit_pet_form')
    except Pet.DoesNotExist:
        messages.error(request, "The requested pet does not exist",
                         extra_tags='edit_pet_form')
        return redirect('not_found')


def __handle_pet_add_form(request, petForm):
    name = petForm.cleaned_data["name"]
    breed = petForm.cleaned_data["breed"]
    age = petForm.cleaned_data["age"]
    image = petForm.cleaned_data["image"]
    medical_notes = petForm.cleaned_data["medical_notes"]
    pet = Pet()
    pet.name = name.title()
    pet.breed = breed.title()
    pet.age = age
    pet.medical_notes = medical_notes
    pet.user = request.user
    pet.image = image
    pet.save()
    messages.success(request, f"{pet.name} has been successfully created. Redirecting you to profile page...",
                     extra_tags='add_pet_form')


# Cancel appointment view
@login_required(login_url='login')
def cancel_appointment(request, cancel_appointment_id):
    try:
        appointment = get_object_or_404(Appointment, id=cancel_appointment_id)
        if appointment.user == request.user:
            appointment.delete()
            appointment_time = appointment.start_date_time.strftime('%Y-%m-%d %H:%M')
            messages.success(request,
                             f"Your appointment on the {appointment_time} has been cancelled. Redirecting you to profile page...",
                             extra_tags="cancel_appointment_form")
        else:
            messages.error(request, "You do not have permission to cancel this appointment.",
                           extra_tags="cancel_appointment_form")
    except Appointment.DoesNotExist:
        messages.error(request, "The requested appointment does not exist.")
        return redirect('not_found')
    return redirect("profile")


@login_required(login_url='login')
def delete_pet(request, delete_pet_id):
    try:
        pet = get_object_or_404(Pet, id=delete_pet_id)
        if pet.user == request.user:
            pet.delete()
            messages.success(request,
                             f"{pet.name} has been successfully deleted. Redirecting you to profile page...",
                             extra_tags="delete_pet_form")
        else:
            messages.error(request, "You do not have permission to delete this pet.", extra_tags="delete_pet_form")
    except Pet.DoesNotExist:
        messages.error(request, "The requested pet does not exist.")
        return redirect('not_found')
    return redirect("profile")


@login_required(login_url='login')
def delete_user(request, delete_user_id):
    try:
        user = get_object_or_404(User, id=delete_user_id)
        if user == request.user:
            user.delete()
            messages.success(request,
                             "Your account has been successfully deleted")
        else:
            messages.error(request, "You do not have permission to delete this user.")
    except User.DoesNotExist:
        messages.error(request, "The requested user does not exist.")
        return redirect('not_found')
    return redirect("home")


# Get appointment by ID view
@login_required(login_url='login')
def get_appointment_by_id(request, appointment_id):
    if appointment_id:
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment_data = {
                "id": appointment.id,
                "start_date_time": appointment.start_date_time.strftime('%d-%m-%Y %H:%M'),
                "description": appointment.description,
                "pet": {
                    "name": appointment.pet.name,
                    "id": appointment.pet.id
                },
                "service": {
                    "name": appointment.service.name,
                    "id": appointment.service.id
                }
            }
            return JsonResponse({"appointment": appointment_data})
        except Appointment.DoesNotExist:
            return JsonResponse({"message": "Appointment not found"}, status=404)
    return JsonResponse({"message": "Invalid request"}, status=400)


@login_required(login_url='login')
def get_pet_by_id(request, pet_id):
    if pet_id:
        try:
            pet = Pet.objects.get(id=pet_id)
            pet_data = {
                "id": pet.id,
                "name": pet.name,
                "breed": pet.breed,
                "age": pet.age,
                "medical_notes": pet.medical_notes
            }
            return JsonResponse({"pet": pet_data})
        except Pet.DoesNotExist:
            return JsonResponse({"message": "Pet not found"}, status=404)
    return JsonResponse({"message": "Invalid request"}, status=400)


@login_required(login_url='login')
def get_service_price(request, service_id):
    if service_id:
        try:
            service = Service.objects.get(id=service_id)
            price_range = {
                "vary_price1": service.vary_price1,
                "vary_price2": service.vary_price2
            }
            return JsonResponse({"price_range": price_range})
        except Service.DoesNotExist:
            return JsonResponse({"message": "Service not found"}, status=404)
    return JsonResponse({"message": "Invalid request"}, status=400)
