BEGIN;
TRUNCATE "django_content_type", "medical_specialty", "doctor", "person", "token_blacklist_outstandingtoken", "patient_profile", "appointment", "person_groups", "django_session", "person_user_permissions", "auth_group", "firm", "token_blacklist_blacklistedtoken", "area", "auth_permission", "review", "location", "clinic", "doctor_profile", "auth_group_permissions", "medical_insurance", "hospital", "django_admin_log", "patient" RESTART IDENTITY;
COMMIT;
