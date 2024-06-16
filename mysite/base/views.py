from django.http import HttpResponse
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .models import Cart, Item, Qna,Order,RefundRequest, Review, UserLogin
from .serializers import CartGetSerializer, CartSerializer, ItemSerializer, LoginSerializer, QnaSerializer,OrderSerializer, RegisterSerializer, ReviewSerializer
from .models import Cart, Category, Item, Qna,Order,RefundRequest, UserLogin, Order
from .serializers import *

import os
from django.utils import timezone
from django.http import JsonResponse
import datetime
from django.db.models import Sum
from django.shortcuts import render
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
class SellerLoginView(APIView):
    serializer_class = SellerLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # 사용자 인증
            user = authenticate(email=email, password=password)
            
            if user:
                # 토큰 생성 또는 기존 토큰 가져오기
                token, created = Token.objects.get_or_create(user=user)
                
                # 토큰을 사용자 모델에 저장
                user.token = token.key
                user.save()
                
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': '인증 실패'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RegisterSellerView(APIView):

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Seller registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class QnaCreateView(APIView):
    def post(self, request):
        serializer = QnaCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Serializer가 유효할 경우 DB에 저장
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
@api_view(['POST'])
def add_answer(request, qna_id):
    try:
        qna = Qna.objects.get(id=qna_id)
    except Qna.DoesNotExist:
        return Response({'error': 'QnA not found'}, status=status.HTTP_404_NOT_FOUND)

    answer = request.data.get('answer')
    if not answer:
        return Response({'error': 'Answer is required'}, status=status.HTTP_400_BAD_REQUEST)

    qna.answer = answer
    qna.save()
    
    serializer = QnaSerializer(qna)
    return Response(serializer.data, status=status.HTTP_200_OK)

#회원가입 클래스 기반 버전   
class Register(generics.CreateAPIView):
    queryset = UserLogin.objects.all()
    serializer_class = RegisterSerializer
@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.filter(approve=False)  # 승인되지 않은 주문만 반환
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def approve_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Check if there's enough stock
    item = order.item
    if item.stock < order.count:
        return Response({'message': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

    # Update the approve status and stock
    order.approve = True
    order.save()
    item.stock -= order.count
    item.save()

    return Response({'message': '승인되었습니다.'}, status=status.HTTP_200_OK)
@api_view(['POST'])
def reject_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Get the rejection reason from the request data
    reason = request.data.get('reason', '')

    # Update the approve status and save the reason for rejection in the state field
    order.approve = False
    order.state = f"거절 사유: {reason}"
    order.save()

    return Response({'message': '거절되었습니다.', 'reason': reason}, status=status.HTTP_200_OK)

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

#(로그인 후) 사용자별 장바구니 품목 조회
class CartGet(generics.ListCreateAPIView):
    serializer_class = CartGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartDelete(generics.RetrieveDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

#(로그인 안해도됨) 제품에 대한 리뷰들 조회
class ItemReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        item_id = self.kwargs['item_id']
        return Review.objects.filter(item_id=item_id)

#(로그인 후) 리뷰 작성
class ReviewCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        item_id = self.kwargs['item_id']
        return Review.objects.filter(item_id=item_id)
    
    def perform_create(self, serializer):
        item_id = self.kwargs['item_id']
        serializer.save(user=self.request.user, item_id=item_id)
    
#(본인이 작성한 리뷰에 대해) 리뷰 수정, 삭제 
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] #권한 허용에 대해 정의

#특정 제품의 정보를 get 해오기
class ItemDetailView(APIView):
    def get(self, request, id):
        try:
            item = Item.objects.get(id=id)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response({"message": "해당 아이템이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
    
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
            return Order.objects.filter(username=username, approve=False)
        return Order.objects.filter(approve=False)


@api_view(['GET'])
def qna_list_by_item(request, item_id):
    qnas = Qna.objects.filter(item__id=item_id)
    if not qnas.exists():
        return Response({'error': 'No QnA found for the given item id'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QnaSerializer(qnas, many=True)
    return Response(serializer.data)

#배송완료 상품의 전체 가격 합산 api
class MonthlyCompletedOrdersTotalPriceAPI(APIView):
    def get(self, request, *args, **kwargs):
        today = timezone.now()
        one_month_ago = today - datetime.timedelta(days=30)
        completed_orders = Order.objects.filter(state='배송완료', created_at__gte=one_month_ago)
        total_price = completed_orders.aggregate(Sum('price'))['price__sum'] or 0
        return Response({'total_price': total_price})

def show_total_price(request):
    return render(request, 'total_price.html')

#filter로 category별 배송완료된 상품들의 가격을 합산하는 코드
def category_totals(request):
    categories = Category.objects.all()
    category_totals = []
    for category in categories:
        total_price = Order.objects.filter(item__category=category, state='배송완료').aggregate(Sum('price'))['price__sum'] or 0
        category_totals.append({'category': category.name, 'total': total_price})
    return JsonResponse(category_totals, safe=False)

#3주 전까지의 각 주차 합산 코드
def get_weekly_sales_data():
    today = timezone.now()
    weeks_ago_3 = today - datetime.timedelta(weeks=3)
    weeks_ago_2 = today - datetime.timedelta(weeks=2)
    weeks_ago_1 = today - datetime.timedelta(weeks=1)

    # 각 주별로 Order 데이터 가져오기
    sales_data = {
        '3_weeks_ago': Order.objects.filter(created_at__gte=weeks_ago_3, created_at__lt=weeks_ago_2, state='배송완료'),
        '2_weeks_ago': Order.objects.filter(created_at__gte=weeks_ago_2, created_at__lt=weeks_ago_1, state='배송완료'),
        '1_week_ago': Order.objects.filter(created_at__gte=weeks_ago_1, created_at__lt=today, state='배송완료'),
        'today': Order.objects.filter(created_at__gte=today - datetime.timedelta(days=1), state='배송완료')
    }

    # 각 주별 매출 합산
    weekly_sales = {
        '3_weeks_ago': sales_data['3_weeks_ago'].aggregate(total_price=Sum('price'))['total_price'] or 0,
        '2_weeks_ago': sales_data['2_weeks_ago'].aggregate(total_price=Sum('price'))['total_price'] or 0,
        '1_week_ago': sales_data['1_week_ago'].aggregate(total_price=Sum('price'))['total_price'] or 0,
        'today': sales_data['today'].aggregate(total_price=Sum('price'))['total_price'] or 0,
    }

    return weekly_sales

def chart_view(request):
    weekly_sales = get_weekly_sales_data()
    return JsonResponse({'weekly_sales': weekly_sales})


#카테고리별 합산 데이터
def get_weekly_category_sales_data():
    today = timezone.now()
    weeks_ago_3 = today - datetime.timedelta(weeks=3)
    weeks_ago_2 = today - datetime.timedelta(weeks=2)
    weeks_ago_1 = today - datetime.timedelta(weeks=1)

    sales_data = {
        '3_weeks_ago': Order.objects.filter(created_at__gte=weeks_ago_3, created_at__lt=weeks_ago_2, state='배송완료'),
        '2_weeks_ago': Order.objects.filter(created_at__gte=weeks_ago_2, created_at__lt=weeks_ago_1, state='배송완료'),
        '1_week_ago': Order.objects.filter(created_at__gte=weeks_ago_1, created_at__lt=today, state='배송완료'),
        'today': Order.objects.filter(created_at__gte=today - datetime.timedelta(days=1), state='배송완료')
    }

    categories = Category.objects.all()
    weekly_category_sales = {category.name: {} for category in categories}

    for category in categories:
        weekly_category_sales[category.name]['3_weeks_ago'] = sales_data['3_weeks_ago'].filter(item__category=category).aggregate(total_price=Sum('price'))['total_price'] or 0
        weekly_category_sales[category.name]['2_weeks_ago'] = sales_data['2_weeks_ago'].filter(item__category=category).aggregate(total_price=Sum('price'))['total_price'] or 0
        weekly_category_sales[category.name]['1_week_ago'] = sales_data['1_week_ago'].filter(item__category=category).aggregate(total_price=Sum('price'))['total_price'] or 0
        weekly_category_sales[category.name]['today'] = sales_data['today'].filter(item__category=category).aggregate(total_price=Sum('price'))['total_price'] or 0

    return weekly_category_sales

def category_chart_view(request):
    weekly_category_sales = get_weekly_category_sales_data()
    return JsonResponse({'weekly_category_sales': weekly_category_sales})

class MonthlyCompletedOrdersPriceAPI(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        # 현재 시간
        today = timezone.now()

        # 한 달 전의 시간
        one_month_ago = today - datetime.timedelta(days=30)

        # 한 달 전부터 현재까지 배송완료된 주문들의 총 가격을 합산
        completed_orders = Order.objects.filter(state='배송완료', created_at__gte=one_month_ago)
        return completed_orders
    
class RefundRequestListCreateAPI(generics.ListCreateAPIView):
    serializer_class = RefundRequestSerializer

    def get_queryset(self):
        return RefundRequest.objects.filter(approved=False, state__isnull=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        approved = serializer.validated_data.get('approved')
        return Response({'refund_request': serializer.data, 'approved': approved}, status=status.HTTP_201_CREATED)
    
class ProductListCreate(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

