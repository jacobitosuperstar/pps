"""Machines module endpoints.
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')


router.register(r'ooo', views.OOOViewSet, basename='ooo')


urlpatterns = [
    path(
        "login/",
        views.EmployeeLoginView.as_view(),
        name="employees_login"
    ),
    path('', include(router.urls))
]
