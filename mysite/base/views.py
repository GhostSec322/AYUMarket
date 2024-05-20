from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Qna, Review ,Order
from .serializers import QnaSerializer, ReviewSerializer,OrderSerialzer
from base.models import Example
from base.serializers import ExampleSerializer
import os

@api_view(['GET', 'POST'])  # 나열할 상품 전체 가져오기
def base_list(request, format=None):
    if request.method == 'GET':
        baseData = Example.objects.all()
        serializer = ExampleSerializer(baseData, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ExampleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])  # 서버내 저장된 이미지 가져오기
def get_image(request, filename):
    current_directory = os.getcwd()  # 현재 디렉토리 추출
    file_path = os.path.join('base/photos', filename)  # url에서 입력된 파일 이름으로 서버내 파일로 진입
    total_path = os.path.join(current_directory, file_path)  # url 결합
    print(total_path)

    try:
        with open(total_path, 'rb') as f:  # total_path를 사용해야 합니다.
            photo_data = f.read()
        return HttpResponse(photo_data, content_type='image/png')
    except FileNotFoundError:
        return HttpResponse(status=404)

@api_view(['GET'])
def product_detail(request):
    product_id = request.query_params.get('product_id', None)
    if product_id is None:
        return Response({'error': 'Product ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Example.objects.get(pk=product_id)
    except Example.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ExampleSerializer(product)
    return Response(serializer.data)

class QnaList(APIView):
    def get(self, request):
        qna = Qna.objects.all()
        serializer = QnaSerializer(qna, many=True)
        return Response(serializer.data)

class ReviewList(APIView):  # Review 대신 ReviewList로 클래스명 수정
    def get(self, request):
        reviews = Review.objects.all()  # ReviewList 대신 reviews로 변수명 수정
        serializer = ReviewSerializer(reviews, many=True)  # ReviewSerializer로 변경
        return Response(serializer.data)
class OrderList(APIView):
    def get(slef,request):
        order = Order.objects.all()
        serizer = OrderSerialzer(order, many=True)
        return Response(serizer.data)