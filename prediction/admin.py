from django.contrib import admin
from .models import MotherDetails, InfantDetails, Prediction

@admin.register(MotherDetails)
class MotherDetailsAdmin(admin.ModelAdmin):
    list_display = ("mother_id", "mother_name", "mother_age", "created_by", "created_at")
    search_fields = ("mother_name",)
    list_filter = ("pre_diabetes", "gest_diabetes", "pre_hypertension", "gest_hypertension")

@admin.register(InfantDetails)
class InfantDetailsAdmin(admin.ModelAdmin):
    list_display = ("infant_id", "mother", "infant_sex", "gestational_age", "birth_weight", "created_at")
    search_fields = ("infant_id", "mother__mother_name")

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("prediction_id", "infant", "mother", "prediction_result", "probability", "prediction_date")
    list_filter = ("prediction_result",)
