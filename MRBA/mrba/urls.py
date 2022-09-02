from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'))
]

admin.site.site_header = "Admin Page"
admin.site.site_title = "MRBA"
admin.site.index_title = "MRBA"