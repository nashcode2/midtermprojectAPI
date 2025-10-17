from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home),
    path('dashboard/', views.dashboard),
    path('profile/', views.profile),
    path('settings/', views.settings_page),
    path('qr/', views.generate_qr),
    path('joke/', views.joke),
    path('weather/', views.weather),
    path('cipher/', views.cipher),

    # New API endpoints
    path('news/', views.news),
    path('currency/', views.currency),
    path('ip-info/', views.ip_info),
    path('password/', views.password_generator),
    path('colors/', views.color_palette),
    path('stats/', views.user_stats),
    path('profile/update/', views.update_profile),

    # Facebook OAuth (custom endpoints)
    path('facebook-login/', views.facebook_login, name='facebook_login'),
    path('facebook-callback/', views.facebook_callback, name='facebook_callback'),
]