from django.urls import path

from .views import HealthView, LoginView, RejectView, ScanView, VerifyView

urlpatterns = [
    path('health', HealthView.as_view()),
    path('login', LoginView.as_view()),
    path('scan', ScanView.as_view()),
    path('verify', VerifyView.as_view()),
    path('reject', RejectView.as_view()),
]
