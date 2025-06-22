from django import forms
from django.contrib.auth.models import Group
from applications.security.models import User

class UserUpdateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "select2 w-full",  # Assuming select2 is used
            "multiple": "multiple"
        }),
        required=False,
        label="Grupos"
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'dni',
            'image',
            'direction',
            'phone',
            'is_active',
            'is_staff',
            # 'is_superuser' # Usually managed separately or by specific roles
            'groups' # Add groups here to ensure it's part of cleaned_data
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input-tailwind', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input-tailwind', 'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input-tailwind', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-input-tailwind', 'placeholder': 'correo@ejemplo.com'}),
            'dni': forms.TextInput(attrs={'class': 'form-input-tailwind', 'placeholder': 'Cédula o RUC'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input-tailwind'}),
            'direction': forms.TextInput(attrs={'class': 'form-input-tailwind', 'placeholder': 'Dirección'}),
            'phone': forms.TextInput(attrs={'class': 'form-input-tailwind', 'placeholder': 'Teléfono'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox-tailwind'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-checkbox-tailwind'}),
        }
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'dni': 'Cédula/RUC',
            'image': 'Imagen de Perfil',
            'direction': 'Dirección',
            'phone': 'Teléfono',
            'is_active': 'Activo',
            'is_staff': 'Es Staff (permite acceso al admin)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Common styling for form inputs - replace 'form-input-tailwind'
        # and 'form-checkbox-tailwind' with actual Tailwind classes used in the project.
        tailwind_input_class = 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light'
        tailwind_checkbox_class = 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'

        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.ClearableFileInput, forms.PasswordInput, forms.NumberInput)):
                current_attrs = field.widget.attrs
                current_attrs['class'] = f"{current_attrs.get('class', '')} {tailwind_input_class}".strip()
            elif isinstance(field.widget, forms.CheckboxInput):
                 current_attrs = field.widget.attrs
                 current_attrs['class'] = f"{current_attrs.get('class', '')} {tailwind_checkbox_class}".strip()

        if self.instance and self.instance.pk:
            self.fields['groups'].initial = self.instance.groups.all()

    def save(self, commit=True):
        user = super().save(commit=False) # Don't commit yet, need to save m2m
        if commit:
            user.save()
            # The 'groups' field on the User model is special.
            # Django handles it automatically if it's part of Meta.fields and the widget is correct.
            # However, explicitly setting it is safer for m2m.
            if self.cleaned_data.get('groups') is not None:
                 user.groups.set(self.cleaned_data['groups'])
            self.save_m2m() # Necessary if 'groups' wasn't in Meta.fields or custom handling
        return user

# A similar form could be created for User Creation if needed
# class UserCreateForm(forms.ModelForm):
#     # ... similar fields, but might include password fields explicitly
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password', ...]
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user
