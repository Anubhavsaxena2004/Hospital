
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from hospital.models import MaintenanceRecord, Bed
from hospital.forms import MaintenanceRecordForm

class MaintenanceListView(LoginRequiredMixin, ListView):
    model = MaintenanceRecord
    template_name = 'hospital/maintenance_list.html'
    context_object_name = 'maintenance_records'
    paginate_by = 10
    ordering = ['-created_at']

class MaintenanceDetailView(LoginRequiredMixin, DetailView):
    model = MaintenanceRecord
    template_name = 'hospital/maintenance_detail.html'
    context_object_name = 'object'

class MaintenanceCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = 'hospital/maintenance_form.html'
    success_url = reverse_lazy('maintenance_list')

    def get_initial(self):
        initial = super().get_initial()
        if 'bed_id' in self.kwargs:
            initial['bed'] = get_object_or_404(Bed, pk=self.kwargs['bed_id'])
        return initial

class MaintenanceUpdateView(LoginRequiredMixin, UpdateView):
    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = 'hospital/maintenance_form.html'
    success_url = reverse_lazy('maintenance_list')

def maintenance_create(request, bed_id=None):
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            if bed_id:
                maintenance.bed = get_object_or_404(Bed, pk=bed_id)
            maintenance.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceRecordForm()
        if bed_id:
            form.fields['bed'].initial = get_object_or_404(Bed, pk=bed_id)
    
    return render(request, 'hospital/maintenance_form.html', {'form': form})
