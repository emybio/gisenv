from django.shortcuts import render

# Create your views here.

def proj(request):
     return render(request, 'maps/projections/map.html', {})
 
def proj2(request):
     return render(request, 'maps/projections/map2.html', {})        