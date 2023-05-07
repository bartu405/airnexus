from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),
    path("register", views.register_page, name="register") ,
    path("air", views.air, name="air"),
    path("cs", views.cs, name="cs"),
    path("flight", views.flight, name="flight"),
    path("details", views.details, name="details"),
    path("booked", views.booked, name="booked"),
    path('bookings', views.bookings, name='bookings'),
    path("<str:profile_name>", views.profile, name="profile"),
    path("<str:wrong_path>", views.error, name="error") 
]