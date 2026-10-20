# Generated for the Infant Mortality Risk Prediction project.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="MotherDetails",
            fields=[
                ("mother_id", models.AutoField(primary_key=True, serialize=False)),
                ("mother_name", models.CharField(max_length=120)),
                ("mother_age", models.PositiveSmallIntegerField()),
                ("education", models.PositiveSmallIntegerField(choices=[(1, "8th grade or less"), (2, "9th–12th grade, no diploma"), (3, "High school graduate / GED"), (4, "Some college, no degree"), (5, "Associate degree"), (6, "Bachelor's degree"), (7, "Master's degree or higher"), (8, "Other / not classified"), (9, "Unknown")])),
                ("prenatal_visits", models.PositiveSmallIntegerField()),
                ("cigarettes", models.PositiveSmallIntegerField(help_text="Average number of cigarettes per day")),
                ("bmi", models.FloatField(blank=True, help_text="Maternal BMI", null=True)),
                ("pre_diabetes", models.BooleanField(choices=[(0, "No"), (1, "Yes")], default=False)),
                ("gest_diabetes", models.BooleanField(choices=[(0, "No"), (1, "Yes")], default=False)),
                ("pre_hypertension", models.BooleanField(choices=[(0, "No"), (1, "Yes")], default=False)),
                ("gest_hypertension", models.BooleanField(choices=[(0, "No"), (1, "Yes")], default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="mother_records", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="InfantDetails",
            fields=[
                ("infant_id", models.AutoField(primary_key=True, serialize=False)),
                ("apgar5", models.PositiveSmallIntegerField(help_text="Apgar score at 5 minutes (0–10)")),
                ("plurality", models.PositiveSmallIntegerField(default=1, help_text="Number of infants in pregnancy")),
                ("infant_sex", models.CharField(choices=[("M", "Male"), ("F", "Female")], max_length=1)),
                ("gestational_age", models.PositiveSmallIntegerField(help_text="Gestational age in completed weeks")),
                ("birth_weight", models.PositiveSmallIntegerField(help_text="Birth weight in grams")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="infant_records", to=settings.AUTH_USER_MODEL)),
                ("mother", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="infants", to="prediction.motherdetails")),
            ],
        ),
        migrations.CreateModel(
            name="Prediction",
            fields=[
                ("prediction_id", models.AutoField(primary_key=True, serialize=False)),
                ("prediction_result", models.PositiveSmallIntegerField(choices=[(0, "Low Risk"), (1, "High Risk")])),
                ("probability", models.FloatField()),
                ("prediction_date", models.DateTimeField(auto_now_add=True)),
                ("infant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="predictions", to="prediction.infantdetails")),
                ("mother", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="predictions", to="prediction.motherdetails")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="risk_predictions", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-prediction_date"]},
        ),
    ]
