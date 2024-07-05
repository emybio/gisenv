from django.shortcuts import render, redirect
from .forms import FirmaForm

def firma_kayit(request):
    if request.method == 'POST':
        form = FirmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('firma_kayit')
    else:
        form = FirmaForm()
    return render(request, 'firma/firma_kayit.html', {'form': form})
