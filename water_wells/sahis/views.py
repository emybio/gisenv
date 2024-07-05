from django.shortcuts import render, redirect
from .forms import SahisForm

def sahis_kayit(request):
    if request.method == 'POST':
        form = SahisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sahis_kayit')
    else:
        form = SahisForm()
    return render(request, 'sahis/sahis_kayit.html', {'form': form})
