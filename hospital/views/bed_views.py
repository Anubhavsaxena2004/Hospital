from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from ..models import Bed, Equipment
from ..forms import BedForm
from django.db.models import Q

def bed_create(request):
    if request.method == 'POST':
        form = BedForm(request.POST)
        if form.is_valid():
            bed = form.save()
            return redirect('bed_detail', pk=bed.pk)
    else:
        form = BedForm()
    
    context = {
        'form': form,
    }
    return render(request, 'hospital/bed_form.html', context)

def bed_detail(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    context = {
        'bed': bed,
    }
    return render(request, 'hospital/bed_detail.html', context)

def bed_edit(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    if request.method == 'POST':
        form = BedForm(request.POST, instance=bed)
        if form.is_valid():
            form.save()
            return redirect('bed_detail', pk=bed.pk)
    else:
        form = BedForm(instance=bed)
    
    context = {
        'form': form,
        'bed': bed,
    }
    return render(request, 'hospital/bed_form.html', context)

class BedDeleteView(DeleteView):
    model = Bed
    template_name = 'hospital/bed_confirm_delete.html'
    success_url = reverse_lazy('bed_management')

def bed_management(request):
    status_filter = request.GET.get('status')
    type_filter = request.GET.get('type')

    beds = Bed.objects.all()

    if status_filter and status_filter != "all":
        beds = beds.filter(status__iexact=status_filter)
    if type_filter and type_filter != "all":
        beds = beds.filter(ward__iexact=type_filter)

    context = {
        'beds': beds,
        'status_filter': status_filter or 'all',
        'type_filter': type_filter or 'all',
    }
    return render(request, 'hospital/bed_management.html', context)
