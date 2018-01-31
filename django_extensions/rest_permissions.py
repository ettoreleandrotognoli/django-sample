from rest_framework.permissions import DjangoModelPermissions


class ModelPermissions(DjangoModelPermissions):
    perms_map = {**DjangoModelPermissions.perms_map, **{
        'GET': ['%(app_label)s.list_%(model_name)s']
    }}
