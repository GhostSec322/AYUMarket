from django.urls import path
from base import views

urlpatterns = [
    path('example/', views.base_list),
    path('getimage/<str:filename>/',views.get_image)
]