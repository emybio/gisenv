from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Firma
from sahis.models import Sahis
from .forms import FirmaForm


@login_required
def firma_list(request):
    firmalar = Firma.objects.all()
    return render(request, 'firma/firma_list.html', {'firmalar': firmalar})

@login_required
def firma_detail(request, pk):
    firma = get_object_or_404(Firma, pk=pk)
    return render(request, 'firma/firma_detail.html', {'firma': firma})

@login_required
def firma_create(request):
    if request.method == 'POST':
        form = FirmaForm(request.POST)
        if form.is_valid():
            firma = form.save(commit=False)
            firma.user = request.user  # İşlemi yapan kullanıcıyı kaydedin
            firma.save()
            return redirect('firma_list')
    else:
        form = FirmaForm()
    return render(request, 'firma/firma_form.html', {'form': form})



@login_required
def firma_update(request, pk):
    firma = get_object_or_404(Firma, pk=pk)
    if request.method == 'POST':
        form = FirmaForm(request.POST, instance=firma)
        if form.is_valid():
            form.save()
            return redirect('firma_list')
    else:
        form = FirmaForm(instance=firma)
    return render(request, 'firma/firma_form.html', {'form': form})
@login_required
def firma_delete(request, pk):
    firma = get_object_or_404(Firma, pk=pk)
    if request.method == 'POST':
        firma.delete()
        return redirect('firma_list')
    return render(request, 'firma/firma_confirm_delete.html', {'firma': firma})
@login_required
def firma_sahis_list(request, pk):
    firma = get_object_or_404(Firma, pk=pk)
    sahislar = Sahis.objects.filter(firma=firma)
    return render(request, 'firma/firma_sahis_list.html', {'firma': firma, 'sahislar': sahislar})

