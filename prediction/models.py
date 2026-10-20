from django.conf import settings
from django.db import models

class MotherDetails(models.Model):
    EDUCATION_CHOICES = [
        (1, "8th grade or less"),
        (2, "9th–12th grade, no diploma"),
        (3, "High school graduate / GED"),
        (4, "Some college, no degree"),
        (5, "Associate degree"),
        (6, "Bachelor's degree"),
        (7, "Master's degree or higher"),
        (8, "Other / not classified"),
        (9, "Unknown"),
    ]
    YES_NO = [(0, "No"), (1, "Yes")]

    mother_id = models.AutoField(primary_key=True)
    mother_name = models.CharField(max_length=120)
    mother_age = models.PositiveSmallIntegerField()
    education = models.PositiveSmallIntegerField(choices=EDUCATION_CHOICES)
    prenatal_visits = models.PositiveSmallIntegerField()
    cigarettes = models.PositiveSmallIntegerField(help_text="Average number of cigarettes per day")
    bmi = models.FloatField(null=True, blank=True, help_text="Maternal BMI")
    pre_diabetes = models.BooleanField(choices=YES_NO, default=False)
    gest_diabetes = models.BooleanField(choices=YES_NO, default=False)
    pre_hypertension = models.BooleanField(choices=YES_NO, default=False)
    gest_hypertension = models.BooleanField(choices=YES_NO, default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="mother_records")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mother #{self.mother_id} — {self.mother_name}"

class InfantDetails(models.Model):
    SEX_CHOICES = [("M", "Male"), ("F", "Female")]
    infant_id = models.AutoField(primary_key=True)
    mother = models.ForeignKey(MotherDetails, on_delete=models.PROTECT, related_name="infants")
    apgar5 = models.PositiveSmallIntegerField(help_text="Apgar score at 5 minutes (0–10)")
    plurality = models.PositiveSmallIntegerField(default=1, help_text="Number of infants in pregnancy")
    infant_sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    gestational_age = models.PositiveSmallIntegerField(help_text="Gestational age in completed weeks")
    birth_weight = models.PositiveSmallIntegerField(help_text="Birth weight in grams")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="infant_records")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Infant #{self.infant_id} (mother #{self.mother_id})"

class Prediction(models.Model):
    LOW = 0
    HIGH = 1
    RISK_CHOICES = [(LOW, "Low Risk"), (HIGH, "High Risk")]

    prediction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="risk_predictions")
    mother = models.ForeignKey(MotherDetails, on_delete=models.PROTECT, related_name="predictions")
    infant = models.ForeignKey(InfantDetails, on_delete=models.PROTECT, related_name="predictions")
    prediction_result = models.PositiveSmallIntegerField(choices=RISK_CHOICES)
    probability = models.FloatField()
    prediction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-prediction_date"]

    def __str__(self):
        return f"Prediction #{self.prediction_id} — {self.get_prediction_result_display()}"
