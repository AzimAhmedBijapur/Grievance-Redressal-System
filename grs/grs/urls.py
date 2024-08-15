from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "GRS"
admin.site.index_title = "MHSSCE"
admin.site.site_title = "GRS"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("login.urls")),
    path('', include("faculty.urls")),
    path('', include("review.urls")),
    path('', include("ho.urls")),
    path('', include("assessment.urls")),
    path('', include("grievances.urls")),
]
