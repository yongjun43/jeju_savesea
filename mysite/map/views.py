from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def jeju_map(request):

    # 인공위성 사진 가져오기
    return render(request, 'map/layout.html')

