from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.get_services, name='services'),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='logout'),
    path('appointment/', views.book_appointment, name='appointment'),
    path('not_found/', views.not_found, name='not_found'),
    path("profile/", views.manage_profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("api/appointment/<int:appointment_id>/", views.get_appointment_by_id),
    path('cancel_appointment/<int:cancel_appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('delete_pet/<int:delete_pet_id>/', views.delete_pet, name='delete_pet'),
    path("api/pet/<int:pet_id>/", views.get_pet_by_id),
    path("api/user/<int:delete_user_id>/", views.delete_user, name='delete_user'),
    path("api/service/price/<int:service_id>/", views.get_service_price, name='service_price'),
]