from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller, name='seller'),
    path('reg/', views.reg, name='reg'),
    path('qna/', views.QnA, name='QnA'),
    path('del/', views.Del, name='Del'),
    path('order/', views.Oreder, name='Order'),
    path('status/', views.Status, name='Status'),
    path('refund/', views.refund, name='refund'),
]