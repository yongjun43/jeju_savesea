from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# 인공위성 사진 가져오기
def index(request):
    return render(request, 'map/index.html')

def move(request):
    loc=request.session.get('loc_list',[])
    if request.method=='POST':
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')

        loc.append({'lat':lat})
        loc.append({'lon':lon})

    request.session['loc_list'] = loc

    return render(request, 'map/move.html', {'loc_list':loc})

def poi(request):
    return render(request, 'map/poi.html')