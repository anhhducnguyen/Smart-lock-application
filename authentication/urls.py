from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.index, name='index'),
    
    # HomePage
    path('', views.home, name='home'),

    # Signup, Sign in, Sign out and activate account
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),

    # Google SSO
    path(
        "google_sso/", include("django_google_sso.urls", namespace="django_google_sso")
    ),

    # Forgot password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Regulations
    path('regulations', views.index, name='index'),

    # Capture image
    path('capture/', views.capture_img, name='capture_img'),
    path('display_name', views.display_user_images, name='display_name'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
