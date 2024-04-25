from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
# Create your views here.
