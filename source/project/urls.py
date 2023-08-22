from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path("admin/", admin.site.urls),
    
    # Production admin url
    path("00my11-1secure0-0admin1-11url00/", admin.site.urls),

    path("patients/", include("patient.urls")),
    
    path("doctors/", include("doctor.urls")),
    path("appointments/", include("appointment.urls")),
    path("reviews/", include("review.urls")),

    path("locations/", include("geo.urls")),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
