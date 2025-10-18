"""
URL configuration for api_nash_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def data_deletion(request):
    return HttpResponse("""
        <h1>Data Deletion Instructions</h1>
        <p>If you wish to delete your data from this app, please contact us at example@email.com.
        Your data will be permanently deleted within 7 days.</p>
    """)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('accounts/', include('allauth.urls')),
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('data-deletion/', data_deletion, name='data_deletion'),
    # Handle Facebook OAuth completion redirect
    path('complete/facebook/', RedirectView.as_view(url='/accounts/facebook/login/callback/', permanent=False)),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
