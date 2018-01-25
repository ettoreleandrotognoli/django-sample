from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from django_extensions.messages import SuccessMessageMixinWithDeleteSupport as SuccessMessageMixin
from .models import Movement


class MovementListView(ListView):
    template_name = 'movement/list.html'
    model = Movement


class MovementDetailView(DetailView):
    template_name = 'movement/detail.html'
    model = Movement


class MovementUpdateView(SuccessMessageMixin, UpdateView):
    fields = '__all__'
    template_name = 'movement/form.html'
    model = Movement
    success_message = _('Movimento "%(remark)s" atualizado com sucesso!')

    def get_success_url(self):
        return resolve_url('movement-detail', pk=self.object.pk)


class MovementCreateView(SuccessMessageMixin, CreateView):
    fields = '__all__'
    template_name = 'movement/form.html'
    model = Movement
    success_message = _('Movimento "%(remark)s" adicionado com sucesso!')

    def get_success_url(self):
        return resolve_url('movement-detail', pk=self.object.pk)


class MovementDeleteView(SuccessMessageMixin, DeleteView):
    model = Movement
    template_name = "movement/delete.html"
    success_url = reverse_lazy('movement-list')
    success_message = _('Movimento "%(remark)s" removido com sucesso!')
