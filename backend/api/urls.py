from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r"tasks", views.TaskViewSet, basename="task")
router.register(r"categories", views.CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
]
