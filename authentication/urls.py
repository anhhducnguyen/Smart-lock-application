from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path(
        "google_sso/", include("django_google_sso.urls", namespace="django_google_sso")
    ),

    path('forgotPassword', views.forgotPassword, name='forgotPassword'),

    # Quên mật khẩu
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
