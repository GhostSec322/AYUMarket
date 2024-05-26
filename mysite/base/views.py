from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import Qna, Order, Item
from django.shortcuts import render, redirect, get_object_or_404
from .serializers import QnaSerializer, OrderPrcCntSerializer
from base.models import Example
from base.serializers import ExampleSerializer
import os
from django.http import HttpResponse

@api_view(['GET','POST'])
def base_list(request, format=None):
    if request.method == 'GET':
        baseData= Example.objects.all()
        serializer=ExampleSerializer(baseData, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ExampleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_image(request, filename):
    current_directory=os.getcwd() #현재 디렉토리 추출
    file_path = os.path.join('base\photos', filename) #url에서 입력된 파일 이름으로 서버내 파일로 진입
    total_path = os.path.join(current_directory,file_path) #url 결합
    print(total_path)

    try:
        with open(file_path, 'rb') as f:
            photo_data = f.read()

        return HttpResponse(photo_data, content_type='image/png')
    except FileNotFoundError:
        return HttpResponse(status=404)

class QnaList(APIView):
    def get(self, request):
        qna = Qna.objects.all()
        serializer = QnaSerializer(qna, many=True)
        return Response(serializer.data)
    
class OrderPrcCntViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderPrcCntSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # 주문의 가격과 수량 추가
        for order_data in data:
            order_instance = Order.objects.get(id=order_data['id'])
            order_data['price'] = order_instance.price
            order_data['count'] = order_instance.count

        return Response(data)

def create_ordre(request):
    if request.method == 'POST':
        item_id = request.POST['item_id']
        username = request.POST['username']
        count = int(request.POST['count'])

        item = Item.objects.get(id=item_id)
        order = Order(item=item, username= username, count=count)
        order.save()

        return HttpResponse('주문이 정상적으로 처리되었습니다.')
    else:
        items = Item.objects.all()
        return render(request,{'items': items})
