from django import forms
from django.contrib.auth.models import Group
from applications.security.models import User

class GroupForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "select2 w-full", # Assuming select2 is used, adjust class as needed
            "multiple": "multiple"
        }),
        required=False,
        label="Usuarios"
    )

    class Meta:
        model = Group
        fields = ['name', 'users']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ingrese nombre del grupo',
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
            }),
        }
        labels = {
            'name': 'Nombre del Grupo',
        }
        help_texts = {
            'name': 'El nombre del grupo debe ser único.',
        }
        error_messages = {
            "name": {
                "unique": "Ya existe un grupo con este nombre.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save(self, commit=True):
        group = super().save(commit=commit)
        if commit:
            group.user_set.set(self.cleaned_data['users'])
        return group
