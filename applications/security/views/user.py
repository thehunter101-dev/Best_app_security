from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from applications.security.components.mixin_crud import PermissionMixin, UpdateViewMixin
from applications.security.forms.user import UserUpdateForm
from applications.security.models import User

class UserUpdateView(LoginRequiredMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'security/users/form.jinja'  # Needs to be created
    success_url = reverse_lazy('security:user_list') # Assumes a user_list view exists or will be created
    permission_required = 'change_user' # Django's default permission for User model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'Actualizar Usuario'
        context['title2'] = f'Editando Usuario: {self.object.username}'
        context['grabar'] = 'Actualizar Usuario'
        # Try to get pk for the back_url from the object itself if it's an update view
        # Or, if you have a different logic for user_list or user_detail, adjust accordingly.
        # For now, using the general success_url.
        context['back_url'] = self.success_url
        # If you have a user detail page:
        # context['back_url'] = reverse_lazy('security:user_detail', kwargs={'pk': self.object.pk})
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        messages.success(self.request, f"Éxito al actualizar el usuario {user.username}.")
        return response

# To make this fully functional, you would also typically have:
# - UserListView (referenced by success_url)
# - UserCreateView
# - UserDeleteView
# - UserDetailView
# - Corresponding templates for list and detail.
# - URL patterns for all these views.

# For now, only UserUpdateView is implemented as per the immediate requirement.
# A placeholder user_list URL will be added, but the view itself is not implemented here.
# A simple user form template 'security/users/form.jinja' will also be needed.
