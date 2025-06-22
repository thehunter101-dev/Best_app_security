from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin # Standard Django login required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q

from applications.security.models import User
from applications.security.forms.user import UserForm, UserUpdateForm

# Custom Mixins from the project
from applications.security.components.mixin_crud import (
    ListViewMixin,
    CreateViewMixin,
    UpdateViewMixin,
    DeleteViewMixin,
    PermissionMixin
)

class UserListView(LoginRequiredMixin, PermissionMixin, ListViewMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    permission_required = 'view_user'

    def get_queryset(self):
        q_param = self.request.GET.get('q')
        # self.query is initialized by ListViewMixin's dispatch()
        if q_param:
            self.query.add(Q(username__icontains=q_param), Q.OR)
            self.query.add(Q(first_name__icontains=q_param), Q.OR)
            self.query.add(Q(last_name__icontains=q_param), Q.OR)
            self.query.add(Q(email__icontains=q_param), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:user_create')
        return context

class UserDetailView(LoginRequiredMixin, PermissionMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user_object'
    permission_required = 'view_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.object
        display_name = user_obj.get_full_name().strip() if user_obj.get_full_name().strip() else user_obj.username

        context['title'] = f'Usuario: {display_name}'
        context['title1'] = f'Detalle del Usuario'
        context['back_url'] = reverse_lazy('security:user_list')

        from applications.security.components.menu_module import MenuModule
        from applications.security.components.group_session import UserGroupSession
        from applications.security.components.group_permission import GroupPermission

        MenuModule(self.request).fill(context)
        user_group_session = UserGroupSession(self.request)
        group = user_group_session.get_group_session()

        if group:
            context['permissions'] = GroupPermission.get_permission_dict_of_group(self.request.user, group)
        else:
            context['permissions'] = {}
        return context

class UserCreateView(LoginRequiredMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('security:user_list')
    permission_required = 'add_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Crear Usuario'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"Éxito al crear el usuario {user.username}.")
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('security:user_list')
    permission_required = 'change_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Usuario'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"Éxito al actualizar el usuario {user.username}.")
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('security:user_list')
    permission_required = 'delete_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.object
        display_name = user_obj.get_full_name().strip() if user_obj.get_full_name().strip() else user_obj.username
        context['grabar'] = 'Eliminar Usuario'
        context['description'] = f"¿Desea eliminar el usuario: {display_name} ({user_obj.username})?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        user_obj = self.object
        user_display_name = user_obj.get_full_name().strip() if user_obj.get_full_name().strip() else user_obj.username
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar el usuario {user_display_name}.")
        return response
