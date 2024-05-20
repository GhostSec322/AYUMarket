from django.urls import path, include
from base import views
from .views import QnaList
from .views import ReviewList ,OrderList
urlpatterns = [
    path('seller/',include('sellerpage.urls')),
    path('example/', views.base_list),
    path('getimage/<str:filename>/',views.get_image),
    #path('detail/<int:pk>/', views.product_detail),
    path('detail/',views.product_detail),
    path('qna/', QnaList.as_view(), name='qna-list'),
    path('Review/',ReviewList.as_view(),name='review-list'),
    path('order/',OrderList.as_view(),name='order-list')
]