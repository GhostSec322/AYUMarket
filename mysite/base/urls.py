from django.urls import path
from base import views
from .views import QnaList

urlpatterns = [
    path('example/', views.base_list),
    path('getimage/<str:filename>/',views.get_image),
    path('qna/', QnaList.as_view(), name='qna-list'),
]