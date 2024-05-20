from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Qna
from .serializers import QnaSerializer
from base.models import Item, UserLogin, Cart
from base.serializers import ItemSerializer, CartSerializer
import os
#from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import RegisterSerializer,LoginSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET','POST']) #나열할 상품 전체 가져오기
def base_list(request, format=None):
    if request.method == 'GET':
        baseData= Item.objects.all()
        serializer=ItemSerializer(baseData, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
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
        product=Item.objects.get(pk=product_id)
    
    except Item.DoesNotExist:
        return Response({'에러 id 번호가 없는디?'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer=ItemSerializer(product)
    return Response(serializer.data)

class QnaList(APIView):
    def get(self, request):
        qna = Qna.objects.all()
        serializer = QnaSerializer(qna, many=True)
        return Response(serializer.data)

#회원가입 클래스 기반 버전   
class Register(generics.CreateAPIView):
    queryset = UserLogin.objects.all()
    serializer_class = RegisterSerializer

    
''' #회원가입 데코레이터 버전
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

#로그인 뷰
class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data #토큰 가져오기
        return Response({"token": token.key}, status=status.HTTP_200_OK)

#로그인 되었을때 접근하는 뷰
class Protected(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({"message": "This is a protected view"})
    
#(로그인 후) 장바구니 품목 생성 및 업데이트
class CartList(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartDelete(generics.RetrieveDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    