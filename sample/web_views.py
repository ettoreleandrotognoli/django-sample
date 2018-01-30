import operator
from functools import reduce

from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from django_extensions.messages import SuccessMessageMixinWithDeleteSupport as SuccessMessageMixin
from .forms import MovementAnnexFormSet
from .models import Movement


class MovementFormViewMixin(object):
    model = Movement
    # form_class = MovementForm
    inline_formsets_titles = [
        _('Anexos')
    ]
    inline_formsets_classes = [
        MovementAnnexFormSet
    ]

    def get_inline_formsets_titles(self):
        inline_forms_len = len(self.get_inline_formsets_classes())
        return getattr(self, 'inline_formsets_titles', [''] * inline_forms_len)

    def get_inline_formsets_classes(self):
        return getattr(self, 'inline_formsets_classes', [])

    def get_inline_formsets(self):
        inline_forms_classes = self.get_inline_formsets_classes()
        kwargs = self.get_inline_formsets_kwargs()
        return [inline_form_class(**kwargs) for inline_form_class in inline_forms_classes]

    def get_inline_formsets_kwargs(self):
        request = self.request
        if request.method in ['POST']:
            data = request.POST
            files = request.FILES
        else:
            files = None
            data = None
        return dict(
            data=data,
            files=files,
        )

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        inline_formsets = self.get_inline_formsets()
        if reduce(operator.and_, list([formset.is_valid() for formset in inline_formsets]), form.is_valid()):
            return self.form_valid(form=form, inline_formsets=inline_formsets)
        else:
            return self.form_invalid(form=form, inline_formsets=inline_formsets)

    def form_valid(self, form, inline_formsets):
        response = super().form_valid(form)
        instance = self.object
        for inline_formset in inline_formsets:
            inline_formset.instance = instance
            inline_formset.save()
        return response

    def form_invalid(self, form, inline_formsets):
        return self.render_to_response(self.get_context_data(
            form=form,
            inline_formsets=zip(self.get_inline_formsets_titles(), inline_formsets)
        ))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'inline_formsets' not in context:
            context['inline_formsets'] = zip(
                self.get_inline_formsets_titles(),
                self.get_inline_formsets()
            )
        return context


class MovementListView(ListView):
    template_name = 'movement/list.html'
    model = Movement


class MovementDetailView(DetailView):
    template_name = 'movement/detail.html'
    model = Movement


class MovementUpdateView(MovementFormViewMixin, SuccessMessageMixin, UpdateView):
    fields = '__all__'
    template_name = 'movement/form.html'
    model = Movement
    success_message = _('Movimento "%(remark)s" atualizado com sucesso!')

    def get_success_url(self):
        return resolve_url('sample:web:movement-detail', pk=self.object.pk)


class MovementCreateView(MovementFormViewMixin, SuccessMessageMixin, CreateView):
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
