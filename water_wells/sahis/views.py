from django.shortcuts import render, get_object_or_404, redirect
from .models import Sahis
from .forms import SahisForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from wells_map.models import Location

from turkiye.models import Il

@login_required
def basvuru_list(request):
    basvurular = Sahis.objects.all()
    map_url = reverse('location_list')
    print("maps : ")
    print(map_url)
    return render(request, 'basvuru/basvuru_list.html', {'basvurular': basvurular,'map_url':map_url})

@login_required
def basvuru_detail(request, pk):
    basvuru = get_object_or_404(Sahis, pk=pk)
    return render(request, 'basvuru/basvuru_detail.html', {'basvuru': basvuru})

@login_required
def basvuru_create(request):
    iller = Il.objects.all()
    if request.method == 'POST':
        lat= request.POST.get("koordinat1")
        lon= request.POST.get("koordinat2")
        info=request.POST.get("info")
        form = SahisForm(request.POST)
        if form.is_valid():
            location = Location(latitude=lat, longitude=lon, info="")
            basvuru=form.save(commit=False)
            basvuru.user= request.user #işlem yapan kullanıcı 
            location.save()            
            basvuru.save()
            return redirect('basvuru_list')
    else:
        form = SahisForm()
    return render(request, 'basvuru/basvuru_form.html', {'form': form,'iller':iller})

@login_required
def basvuru_update(request, pk):
    basvuru = get_object_or_404(Sahis, pk=pk)
    if request.method == 'POST':
        form = SahisForm(request.POST, instance=basvuru)
        if form.is_valid():
            form.save()
            return redirect('basvuru_list')
    else:
        form = SahisForm(instance=basvuru)
    return render(request, 'basvuru/basvuru_form.html', {'form': form})

@login_required
def basvuru_delete(request, pk):
    basvuru = get_object_or_404(Sahis, pk=pk)
    if request.method == 'POST':
        basvuru.delete()
        return redirect('basvuru_list')
    return render(request, 'basvuru/basvuru_confirm_delete.html', {'basvuru': basvuru})


