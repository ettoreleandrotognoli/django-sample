from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import model_to_dict


class SuccessMessageMixinWithDeleteSupport(SuccessMessageMixin):
    def delete_form_valid(self, object):
        success_message = self.get_success_message(model_to_dict(object))
        if success_message:
            messages.success(self.request, success_message)

    def delete(self, *args, **kwargs):
        object = self.get_object()
        result = super().delete(*args, **kwargs)
        self.delete_form_valid(object)
        return result
