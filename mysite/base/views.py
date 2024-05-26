from django.http import HttpResponse
from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Qna,Order
from .serializers import QnaSerializer,OrderSerializer
from base.models import Example
from base.serializers import ExampleSerializer
import os

@api_view(['GET','POST']) #나열할 상품 전체 가져오기
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

@api_view(['GET'])  #서버내 저장된 이미지 가져오기
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

'''   
@api_view(['GET']) #특정 상품 detail 가져오기 쿼리 파라미터 안쓴 ver
def product_detail(request,pk):
    try:
        product = Example.objects.get(pk=pk) 
    except Example.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer=ExampleSerializer(product)
    return Response(serializer.data)
'''

@api_view(['GET'])
def product_detail(request):
    product_id=request.query_params.get('product_id',None)
    if product_id is None:
        return Response({'에러 에러 id 어디감?'},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        product=Example.objects.get(pk=product_id)
    
    except Example.DoesNotExist:
        return Response({'에러 id 번호가 없는디?'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer=ExampleSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def qna_list(request):
    qna = Qna.objects.all()
    serializer = QnaSerializer(qna, many=True)
    return Response(serializer.data)
class OrderListByUsername(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username')
        if username is not None:
            return Order.objects.filter(username=username)
        return Order.objects.all()
    
@api_view(['GET'])
def qna_list_by_item(request, item_id):
    qnas = Qna.objects.filter(item__id=item_id)
    if not qnas.exists():
        return Response({'error': 'No QnA found for the given item id'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QnaSerializer(qnas, many=True)
    return Response(serializer.data)