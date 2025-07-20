from django.urls import path
from . import views

app_name = 'floorplan'

urlpatterns = [
    path(
        'household/<int:pk>/3d-builder/',
        views.Builder3D.as_view(),
        name='builder3d'
    ),
    path(
        'household/<int:pk>/3d-save/',
        views.save_layout,
        name='save_layout'
    ),
]
