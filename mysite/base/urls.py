from django.urls import path
from . import views
from .views import OrderListByUsername, qna_list  # 필요한 클래스 뷰 가져오기

urlpatterns = [
    path('example/', views.base_list),
    path('getimage/<str:filename>/', views.get_image),
    # path('detail/<int:pk>/', views.product_detail),
    path('detail/', views.product_detail),
    path('qna/',views.qna_list, name='qna-list'),
    path('qna/item/<int:item_id>/', views.qna_list_by_item, name='qna-list-by-item'), 
    path('orders/', OrderListByUsername.as_view(), name='order-list-by-username'),
]
