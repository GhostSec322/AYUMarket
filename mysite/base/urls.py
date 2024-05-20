from django.urls import path
from base import views
from .views import QnaList
from .views import Register,Login

urlpatterns = [
    path('example/', views.base_list),
    path('getimage/<str:filename>/',views.get_image),
    #path('detail/<int:pk>/', views.product_detail),
    path('detail/',views.product_detail),
    path('qna/', QnaList.as_view(), name='qna-list'),
    path('register/', Register.as_view()),
    path('login/', Login.as_view())
]