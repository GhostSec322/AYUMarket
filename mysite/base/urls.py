from django.urls import path, include
from base import views
from .views import QnaList, OrderPrcCntViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', OrderPrcCntViewSet)

urlpatterns = [
    path('example/', views.base_list),
    path('getimage/<str:filename>/',views.get_image),
    path('qna/', QnaList.as_view(), name='qna-list'),
    path('', include(router.urls)),
]