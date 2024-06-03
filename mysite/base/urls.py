from django.urls import path
from . import views
from .views import *  # 필요한 클래스 뷰 가져오기

urlpatterns = [
    path('example/', views.base_list),
    path('getimage/<str:filename>/', views.get_image),
    # path('detail/<int:pk>/', views.product_detail),
    path('detail/', views.product_detail),
    path('qna/',views.qna_list, name='qna-list'),
    path('qna/item/<int:item_id>/', views.qna_list_by_item, name='qna-list-by-item'), 
    path('orders/', OrderListByUsername.as_view(), name='order-list-by-username'),
    path('monthly-completed-orders-price/', MonthlyCompletedOrdersPriceAPI.as_view(), name='monthly_completed_orders_price'),
    path('refund-requests/', RefundRequestListCreateAPI.as_view(), name='refund_request_list_create'),
    path('itemlist/', views.base_list),
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('protected/', Protected.as_view()),
    path('cart/', CartList.as_view()),
    path('cartget/', CartGet.as_view()),
    path('cart/<int:pk>/', CartDelete.as_view()),
    #전체 가격 합산url
    path('api/monthly-completed-orders-total/', MonthlyCompletedOrdersTotalPriceAPI.as_view(), name='monthly-completed-orders-total'),
    path('total-price/', show_total_price, name='show-total-price'),
    #카테고리별 합산url
    path('category_totals/', category_totals, name='category_totals'),
    #전체 합산 그래프
    path('chart-data/', chart_view, name='chart-data'),
    #카테고리별 합산 그래프
    path('category-chart-data/', category_chart_view, name='category-chart-data'),
]

