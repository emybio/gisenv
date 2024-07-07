from django.shortcuts import render, get_object_or_404, redirect
from .models import Sahis
from .forms import SahisForm
from django.urls import reverse

def sahis_list(request):
    sahislar = Sahis.objects.all()
    map_url = reverse('location_list')
    print("maps : ")
    print(map_url)
    return render(request, 'sahis/sahis_list.html', {'sahislar': sahislar,'map_url':map_url})

def sahis_detail(request, pk):
    sahis = get_object_or_404(Sahis, pk=pk)
    return render(request, 'sahis/sahis_detail.html', {'sahis': sahis})

def sahis_create(request):
    if request.method == 'POST':
        form = SahisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sahis_list')
    else:
        form = SahisForm()
    return render(request, 'sahis/sahis_form.html', {'form': form})

def sahis_update(request, pk):
    sahis = get_object_or_404(Sahis, pk=pk)
    if request.method == 'POST':
        form = SahisForm(request.POST, instance=sahis)
        if form.is_valid():
            form.save()
            return redirect('sahis_list')
    else:
        form = SahisForm(instance=sahis)
    return render(request, 'sahis/sahis_form.html', {'form': form})

def sahis_delete(request, pk):
    sahis = get_object_or_404(Sahis, pk=pk)
    if request.method == 'POST':
        sahis.delete()
        return redirect('sahis_list')
    return render(request, 'sahis/sahis_confirm_delete.html', {'sahis': sahis})


