# Infant Mortality Risk Prediction System

A Django + SQLite3 academic prototype with:
- Doctor login using Django's built-in authentication
- Mother details entry and storage
- Infant details entry linked to a mother
- Prediction by `infant_id`
- Saved prediction history
- Responsive CSS dashboard
- Separate Healthcare Professional and Administrator experiences
- Administrator-only user management (activate/deactivate doctor accounts)

## Important model setup
The ZIP does **not** contain your trained model binaries because they were saved separately in Google Drive/Colab. Copy the matching files from your training workflow into `ml_models/`:

- `xgboost_infant_mortality.pkl`
- `xgb_preprocessing.pkl`

The model and preprocessing file must come from the same training run. This app expects the preprocessing dictionary keys:
`feature_columns`, `median_values`, `unknown_codes`, and `sex_mapping`.

If your files use different names, either rename them as above or change the constants in `prediction/ml_service.py`.

## Windows setup (VS Code terminal)

```powershell
py -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign in with the superuser account you created.
The first superuser is also allowed to use the application; create more users in `/admin/` if needed.

## Workflow
1. Sign in.
2. Add a mother's antenatal details.
3. Add an infant after birth and select the mother record.
4. Open Prediction, enter the `infant_id`, and generate a prediction.
5. View saved prediction history.

## Feature mapping
The application maps database fields into the exact expected model feature names:
`mother_age`, `education`, `prenatal_visits`, `cigarettes`, `bmi`, `pre_diabetes`, `gest_diabetes`, `pre_hypertension`, `gest_hypertension`, `apgar5`, `plurality`, `infant_sex`, `gestational_age`, `birth_weight`.

Education is stored as the CDC numeric code. The diabetes and hypertension fields are encoded as 1 for Yes and 0 for No. Infant sex is mapped using `prep["sex_mapping"]` where available.

## Model behavior
The risk label uses a 0.50 threshold: probability >= 0.50 is labelled High Risk; otherwise Low Risk. This threshold is configurable in `prediction/ml_service.py`.

## Important research limitation
This is an academic prototype, not a clinically validated medical device. The available death-linkage labels in the current project may be incomplete, so predictions must not be used for clinical decisions. The probability is the model's output, not a calibrated clinical probability.

## Troubleshooting
- `Model files not found`: copy the two model artifacts into `ml_models/`.
- `Unexpected feature columns`: confirm `xgb_preprocessing.pkl` belongs to the same trained model.
- If model loading fails after a scikit-learn/XGBoost upgrade, install versions compatible with the environment used to save the model.


## Actor permissions (matches the use-case diagram)

- **Healthcare Professional / User:** Registers through `/accounts/register/`, signs in, records maternal information, records infant information linked to a mother, generates predictions by infant ID, and views prediction history. A newly registered account is always a regular user.
- **Administrator:** Create the administrator account from the terminal using `python manage.py createsuperuser`. Administrators can manage registered doctor accounts at `/users/` (activate/deactivate) and view prediction history. The Django admin site is available at `/admin/` for broader database administration.
- **Access control:** The Manage Users page is restricted to staff/admin accounts. Public registration never grants administrator privileges. The app uses Django's built-in `is_staff` flag for the Administrator role.
- **Logout:** Use the Log out button on the dashboard or the sign-out icon at the bottom of the sidebar.

For a project demonstration, consider restricting public doctor registration or adding administrator approval before using real patient data.
