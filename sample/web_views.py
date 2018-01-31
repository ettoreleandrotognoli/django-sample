from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Avg, Min, Max, Sum, DecimalField
from django.db.models import Value as V
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from django_extensions.messages import SuccessMessageMixinWithDeleteSupport as SuccessMessageMixin
from django_extensions.views import CreateGenericMultipleFormViewMixin, UpdateGenericMultipleFormViewMixin
from .forms import MovementAnnexFormSet
from .models import Movement


@method_decorator([
    login_required,
    permission_required('sample.list_movement')
], 'dispatch')
class MovementListView(ListView):
    template_name = 'movement/list.html'
    model = Movement


@method_decorator([
    login_required,
    permission_required('sample.show_movement')
], 'dispatch')
class MovementDetailView(DetailView):
    template_name = 'movement/detail.html'
    model = Movement


@method_decorator([
    login_required,
    permission_required('sample.change_movement')
], 'dispatch')
class MovementUpdateView(UpdateGenericMultipleFormViewMixin, SuccessMessageMixin, UpdateView):
    model = Movement
    inline_formsets_titles = [
        _('Anexos')
    ]
    inline_formsets_classes = [
        MovementAnnexFormSet
    ]
    fields = '__all__'
    template_name = 'movement/form.html'
    model = Movement
    success_message = _('Movimento "%(remark)s" atualizado com sucesso!')

    def get_success_url(self):
        return resolve_url('sample:web:movement-detail', pk=self.object.pk)


@method_decorator([
    login_required,
    permission_required('sample.add_movement')
], 'dispatch')
class MovementCreateView(CreateGenericMultipleFormViewMixin, SuccessMessageMixin, CreateView):
    model = Movement
    inline_formsets_titles = [
        _('Anexos')
    ]
    inline_formsets_classes = [
        MovementAnnexFormSet
    ]
    fields = '__all__'
    template_name = 'movement/form.html'
    model = Movement
    success_message = _('Movimento "%(remark)s" adicionado com sucesso!')

    def get_success_url(self):
        return resolve_url('sample:web:movement-detail', pk=self.object.pk)


@method_decorator([
    login_required,
    permission_required('sample.delete_movement')
], 'dispatch')
class MovementDeleteView(SuccessMessageMixin, DeleteView):
    model = Movement
    template_name = 'movement/delete.html'
    success_url = reverse_lazy('sample:web:movement-list')
    success_message = _('Movimento "%(remark)s" removido com sucesso!')


def summary_view(request):
    object_list = Movement.objects.aggregate(**{
        ugettext('Valor Médio'): Avg('value'),
        ugettext('Valor Minimo'): Min('value'),
        ugettext('Valor Máximo'): Max('value'),
        ugettext('Valor Total'): Coalesce(Sum('value'), V(0), output_field=DecimalField()),
    }).items()
    return render(request, 'movement/summary.html', locals())
