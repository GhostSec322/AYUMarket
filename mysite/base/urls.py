from django.urls import path
from base import views
from .views import QnaList

urlpatterns = [
    path('example/', views.base_list),
    path('getimage/<str:filename>/',views.get_image),
    #path('detail/<int:pk>/', views.product_detail),
    path('detail/',views.product_detail),
    path('qna/', QnaList.as_view(), name='qna-list'),
]