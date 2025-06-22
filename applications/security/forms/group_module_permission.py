from django import forms
from django.contrib.auth.models import Group, Permission

from applications.security.models import Module, GroupModulePermission

class GroupModulePermissionForm(forms.ModelForm):
    module = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        widget=forms.Select(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
        }),
        label="Módulo"
    )
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),  # Populate dynamically in __init__
        widget=forms.SelectMultiple(attrs={
            "class": "select2 w-full", # Assuming select2 is used
            "multiple": "multiple"
        }),
        required=True,
        label="Permisos"
    )

    class Meta:
        model = GroupModulePermission
        fields = ['group', 'module', 'permissions']
        widgets = {
            'group': forms.HiddenInput(), # Group will be set from URL or context
        }
        labels = {
            'group': 'Grupo',
        }
        error_messages = {
            'module': {
                'unique_together': 'Ya existe una asignación de permisos para este grupo y módulo.',
            }
        }

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group_instance', None)
        super().__init__(*args, **kwargs)

        if group:
            self.fields['group'].initial = group
            self.instance.group = group # Ensure instance has group for validation

        # Populate permissions based on selected module (if any) or existing instance
        selected_module_id = None
        if self.data.get('module'): # If form submitted
            selected_module_id = self.data.get('module')
        elif self.instance and self.instance.module: # If editing existing instance
            selected_module_id = self.instance.module.id

        if selected_module_id:
            try:
                module = Module.objects.get(pk=selected_module_id)
                # Filter permissions relevant to the module's content type
                # This assumes permissions are associated with models, and modules relate to these models.
                # If Module model itself has permissions, adjust accordingly.
                # For now, let's assume Module model has a content_type or similar
                # or that permissions are generically applicable.
                # A more robust way would be to filter permissions by content_type of models related to the module
                self.fields['permissions'].queryset = Permission.objects.filter(content_type__app_label=module._meta.app_label)
                # Or, if Module itself defines its relevant permissions:
                # self.fields['permissions'].queryset = module.permissions.all()
            except Module.DoesNotExist:
                self.fields['permissions'].queryset = Permission.objects.none()
        else:
             # Default to all permissions if no module context, or narrow down as needed
            self.fields['permissions'].queryset = Permission.objects.all()


    def clean(self):
        cleaned_data = super().clean()
        group = cleaned_data.get('group')
        module = cleaned_data.get('module')

        if group and module:
            # Check for uniqueness constraint (group, module)
            # Exclude current instance if updating
            queryset = GroupModulePermission.objects.filter(group=group, module=module)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError(
                    "Ya existe una asignación de permisos para este grupo y módulo. Edite la existente.",
                    code='unique_group_module'
                )
        return cleaned_data
