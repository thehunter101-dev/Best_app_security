from django.http import JsonResponse
from applications.security.models import Module

def module_permissions(request, module_id):
    try:
        module = Module.objects.get(pk=module_id)
        permissions = list(module.permissions.values('id', 'name'))
        return JsonResponse({'permissions': permissions})
    except Module.DoesNotExist:
        return JsonResponse({'permissions': []})
