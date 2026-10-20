from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("mothers/", views.mother_list, name="mother_list"),
    path("mothers/add/", views.mother_create, name="mother_create"),
    path("infants/", views.infant_list, name="infant_list"),
    path("infants/add/", views.infant_create, name="infant_create"),
    path("predict/", views.predict_page, name="predict"),
    path("history/", views.prediction_history, name="prediction_history"),
    path("users/", views.manage_users, name="manage_users"),
    path("users/<int:user_id>/toggle-active/", views.toggle_user_active, name="toggle_user_active"),
]
