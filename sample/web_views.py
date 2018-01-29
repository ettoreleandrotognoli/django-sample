from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from django_extensions.messages import SuccessMessageMixinWithDeleteSupport as SuccessMessageMixin
from .models import Movement
from .forms import MovementForm,MovementAnnexForm


class MovementFormViewMixin(object):
    model = Movement
    form_class = MovementForm
    inline_forms_titles = [
        _('Anexos')
    ]
    inline_forms_classes = [
        MovementAnnexForm
    ]

    def get_inline_forms_titles(self):
        inline_forms_len = len(self.get_inline_forms_classes())
        return getattr(self,'inline_forms_titles',['']*inline_forms_len)

    def get_inline_forms_classes(self):
        return getattr(self,'inline_forms_classes',[])

    def get_inline_forms(self,*args,**kwargs):
        inline_forms_classes = self.get_inline_forms_classes()
        return [ inline_form_class(*args,**kwargs) for inline_form_class in inline_forms_classes]


    def get_context_data(**kwargs):
        context = super().get_context_data(**kwargs)
        context['inline_forms'] = zip(
            self.get_inline_forms_titles(),
            self.get_inline_forms_classes(
                instance=self.object
            )
        )
        return context


class MovementListView(ListView):
    template_name = 'movement/list.html'
    model = Movement


class MovementDetailView(DetailView):
    template_name = 'movement/detail.html'
    model = Movement


class MovementUpdateView(SuccessMessageMixin,MovementFormViewMixin, UpdateView):
    fields = '__all__'
    template_name = 'movement/form.html'
    model = Movement
    success_message = _('Movimento "%(remark)s" atualizado com sucesso!')

    def get_success_url(self):
        return resolve_url('sample:web:movement-detail', pk=self.object.pk)


class MovementCreateView(SuccessMessageMixin,MovementFormViewMixin, CreateView):
    fields = '__all__'
    template_name = 'movement/form.html'
    model = Movement
    success_message = _('Movimento "%(remark)s" adicionado com sucesso!')

    def get_success_url(self):
        return resolve_url('sample:web:movement-detail', pk=self.object.pk)


class MovementDeleteView(SuccessMessageMixin, DeleteView):
    model = Movement
    template_name = "movement/delete.html"
    success_url = reverse_lazy('sample:web:movement-list')
    success_message = _('Movimento "%(remark)s" removido com sucesso!')
