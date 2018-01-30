import operator
from functools import reduce


class GenericMultipleFormViewMixin(object):
    object = None
    model = None
    inline_formsets_titles = [
    ]
    inline_formsets_classes = [
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
        kwargs = {}
        if request.method in ['POST']:
            kwargs['data'] = request.POST
            kwargs['files'] = request.FILES
        if hasattr(self, 'object'):
            kwargs['instance'] = self.object
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
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
