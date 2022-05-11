from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Address


class CreateAddress(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    model = Address
    fields = '__all__'
    template_name = 'addresses/create_address.html'
    success_url = reverse_lazy('home_tournaments')
    success_message = 'Pomyślnie dodano nowy adres'
    permission_required = ('add_address',)
