from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import MotherDetailsForm, InfantDetailsForm, DoctorRegistrationForm
from .models import MotherDetails, InfantDetails, Prediction
from .ml_service import predict_infant, ModelArtifactError


def doctor_register(request):
    """Public self-registration for doctor accounts; new accounts are not staff/admins."""
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = DoctorRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        login(request, user)
        messages.success(request, "Your doctor account has been created. Welcome to InfantCare AI.")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})

@login_required
def dashboard(request):
    context = {
        "mother_count": MotherDetails.objects.count(),
        "infant_count": InfantDetails.objects.count(),
        "prediction_count": Prediction.objects.count(),
        "user_count": User.objects.filter(is_staff=False, is_superuser=False).count(),
        "recent_predictions": Prediction.objects.select_related("mother", "infant", "user")[:5],
    }
    return render(request, "prediction/dashboard.html", context)

@login_required
def mother_list(request):
    mothers = MotherDetails.objects.order_by("-created_at")
    return render(request, "prediction/mother_list.html", {"mothers": mothers})

@login_required
def mother_create(request):
    form = MotherDetailsForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        mother = form.save(commit=False)
        mother.created_by = request.user
        mother.save()
        messages.success(request, f"Mother record saved. Mother ID: {mother.mother_id}")
        return redirect("mother_list")
    return render(request, "prediction/mother_form.html", {"form": form})

@login_required
def infant_list(request):
    infants = InfantDetails.objects.select_related("mother").order_by("-created_at")
    return render(request, "prediction/infant_list.html", {"infants": infants})

@login_required
def infant_create(request):
    form = InfantDetailsForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        infant = form.save(commit=False)
        infant.created_by = request.user
        infant.save()
        messages.success(request, f"Infant record saved. Infant ID: {infant.infant_id}")
        return redirect("infant_list")
    return render(request, "prediction/infant_form.html", {"form": form})

@login_required
def predict_page(request):
    result = None
    infant = None
    infant_id = request.POST.get("infant_id", "").strip() if request.method == "POST" else request.GET.get("infant_id", "").strip()

    if request.method == "POST":
        if not infant_id.isdigit():
            messages.error(request, "Enter a valid numeric infant ID.")
        else:
            infant = get_object_or_404(InfantDetails.objects.select_related("mother"), infant_id=int(infant_id))
            try:
                label, probability, raw = predict_infant(infant.mother, infant)
                saved = Prediction.objects.create(
                    user=request.user,
                    mother=infant.mother,
                    infant=infant,
                    prediction_result=label,
                    probability=probability,
                )
                result = {
                    "record": saved,
                    "label": "High Risk" if label == 1 else "Low Risk",
                    "is_high": label == 1,
                    "probability_percent": round(probability * 100, 2),
                    "raw": raw,
                }
            except ModelArtifactError as exc:
                messages.error(request, str(exc))
    return render(request, "prediction/predict.html", {"infant": infant, "result": result, "infant_id": infant_id})

@login_required
def prediction_history(request):
    predictions = Prediction.objects.select_related("mother", "infant", "user").all()
    return render(request, "prediction/history.html", {"predictions": predictions})


@staff_member_required(login_url="login")
def manage_users(request):
    """Administrator-only user management screen."""
    users = User.objects.order_by("-is_staff", "username")
    return render(request, "prediction/manage_users.html", {"managed_users": users})

@staff_member_required(login_url="login")
def toggle_user_active(request, user_id):
    """Allow administrators to activate/deactivate doctor accounts via POST."""
    if request.method != "POST":
        return redirect("manage_users")
    target = get_object_or_404(User, pk=user_id)
    if target.pk == request.user.pk:
        messages.error(request, "You cannot deactivate your own administrator account.")
    elif target.is_superuser:
        messages.error(request, "A superuser account cannot be changed from this screen.")
    elif target.is_staff:
        messages.error(request, "Administrator accounts cannot be changed from doctor management.")
    else:
        target.is_active = not target.is_active
        target.save(update_fields=["is_active"])
        state = "activated" if target.is_active else "deactivated"
        messages.success(request, f"Account '{target.username}' was {state}.")
    return redirect("manage_users")
