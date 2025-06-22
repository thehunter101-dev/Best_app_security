from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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

# Re-defining UserForm with password fields for creation, and UserUpdateForm without them.
# This was defined in a previous step (Plan step 1).

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese la contraseña',
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }), label="Contraseña", required=True)

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirme la contraseña',
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }), label="Confirmar Contraseña", required=True)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'dni',
            'direction', 'phone', 'image',
            'is_active', 'is_staff',
            'groups',
        ]
        # Note: 'is_superuser' and 'user_permissions' are intentionally omitted for safety in general forms,
        # can be added if specific admin interfaces require them.
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de usuario',
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Ingrese los nombres',
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Ingrese los apellidos',
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico',
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
            'dni': forms.TextInput(attrs={
                'placeholder': 'Ingrese DNI/Cédula o RUC',
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
            'direction': forms.TextInput(attrs={
                'placeholder': 'Ingrese la dirección',
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Ingrese el teléfono',
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
            }),
            'groups': forms.SelectMultiple(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 h-40 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }),
        }
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'dni': 'DNI/Cédula o RUC',
            'direction': 'Dirección',
            'phone': 'Teléfono',
            'image': 'Imagen de Perfil',
            'is_active': 'Activo',
            'is_staff': 'Personal de Administración (Staff)',
            'groups': 'Grupos',
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.',
            'is_active': 'Designa si este usuario debe ser tratado como activo. Desmarque esto en lugar de borrar cuentas.',
            'is_staff': 'Designa si el usuario puede iniciar sesión en el sitio de administración y tiene permisos implícitos de staff.',
            'groups': 'Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos otorgados a cada uno de sus grupos.',
        }
        error_messages = {
            'username': {'unique': "Un usuario con ese nombre de usuario ya existe."},
            'email': {'unique': "Un usuario con ese correo electrónico ya existe."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False # Image is optional

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
        # Check for uniqueness if it's a new user or if the email has changed
        if self.instance and self.instance.pk: # if updating
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Un usuario con este correo electrónico ya existe.")
        else: # if creating
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Un usuario con este correo electrónico ya existe.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance and self.instance.pk: # if updating
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Un usuario con este nombre de usuario ya existe.")
        else: # if creating
             if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Un usuario con este nombre de usuario ya existe.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password: # Only set password if provided (relevant for create, or if changing password)
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m() # Important for saving ManyToMany fields like groups
        return user


class UserUpdateForm(forms.ModelForm): # This form is for updating, password is not directly handled here
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'dni',
            'direction', 'phone', 'image',
            'is_active', 'is_staff',
            'groups',
        ]
        # Widgets, labels, help_texts, error_messages are similar to UserForm but without password fields.
        # For brevity, reusing the Meta from UserForm and then adjusting.
        widgets = UserForm.Meta.widgets.copy()
        labels = UserForm.Meta.labels.copy()
        help_texts = UserForm.Meta.help_texts.copy()
        error_messages = UserForm.Meta.error_messages.copy()

        # Remove password related keys if they accidentally got copied (they shouldn't be in UserForm.Meta.fields)
        for key in ['password', 'confirm_password']:
            widgets.pop(key, None)
            labels.pop(key, None)
            help_texts.pop(key, None)
            error_messages.pop(key, None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        # Optionally disable username editing for existing users
        # if self.instance and self.instance.pk:
        #     self.fields['username'].disabled = True
        #     self.fields['username'].help_text = "El nombre de usuario no se puede cambiar una vez creado."

    def clean_email(self): # Ensure email uniqueness on change
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
        if self.instance and self.instance.pk:
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Un usuario con este correo electrónico ya existe.")
        return email

    def clean_username(self): # Ensure username uniqueness on change (if editable)
        username = self.cleaned_data.get('username')
        if self.instance and self.instance.pk and self.fields['username'].disabled == False:
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Un usuario con este nombre de usuario ya existe.")
        return username

    # save method is inherited from ModelForm, which is fine as password is not handled here.
    # Password changes should be done via a separate form/view.
