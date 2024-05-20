from django.shortcuts import render

# Create your views here.
def seller(request):
    return render(request,'sellerpage/admin.html')

def reg(request):
    return render(request,'sellerpage/templates/reg.html')


def QnA(request):
    return render(request,'sellerpage/templates/QnA.html')

def Del(request):
    return render(request,'sellerpage/template/Del.html')


def Oreder(request):
    return render(request,'sellerpage/templates/Order.html')
def Status(request):
    return render(request,'sellerpage/templates/status.html')

def refund(request):
    return render(request,'sellerpage/templates/refund.html')