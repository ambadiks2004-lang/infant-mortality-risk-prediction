from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from prediction import views as prediction_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/register/", prediction_views.doctor_register, name="doctor_register"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("prediction.urls")),
]
