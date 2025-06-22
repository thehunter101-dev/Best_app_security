from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q

from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.security.forms.group import GroupForm
from applications.security.forms.group_module_permission import GroupModulePermissionForm
from applications.security.models import User, GroupModulePermission # Assuming User model is needed, adjust if not

# Group CRUD Views
class GroupListView(LoginRequiredMixin, PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/groups/list.jinja' # Adjusted path
    model = Group
    context_object_name = 'groups'
    permission_required = 'view_group' # Django's default permission for Group model

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        query = Q()
        if q1:
            query.add(Q(name__icontains=q1), Q.OR)
        return self.model.objects.filter(query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:group_create')
        context['title1'] = 'Grupos'
        context['title2'] = 'Listado de Grupos del Sistema'
        # context['permissions'] is already added by PermissionMixin
        return context


class GroupCreateView(LoginRequiredMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = Group
    template_name = 'security/groups/form.jinja' # Adjusted path
    form_class = GroupForm
    success_url = reverse_lazy('security:group_list')
    permission_required = 'add_group' # Django's default permission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'Crear Grupo'
        context['title2'] = 'Nuevo Grupo'
        context['grabar'] = 'Grabar Grupo'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        group = self.object
        messages.success(self.request, f"Éxito al crear el grupo {group.name}.")
        return response


class GroupUpdateView(LoginRequiredMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = Group
    template_name = 'security/groups/form.jinja' # Adjusted path
    form_class = GroupForm
    success_url = reverse_lazy('security:group_list')
    permission_required = 'change_group' # Django's default permission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'Actualizar Grupo'
        context['title2'] = f'Editando Grupo: {self.object.name}'
        context['grabar'] = 'Actualizar Grupo'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        group = self.object
        messages.success(self.request, f"Éxito al actualizar el grupo {group.name}.")
        return response


class GroupDeleteView(LoginRequiredMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = Group
    template_name = 'core/delete.html' # Using generic delete template
    success_url = reverse_lazy('security:group_list')
    permission_required = 'delete_group' # Django's default permission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'Eliminar Grupo'
        context['grabar'] = 'Eliminar Grupo'
        context['description'] = f"¿Desea eliminar el grupo: {self.object.name}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        group_name = self.object.name
        # Instead of logical delete, Group model is usually hard deleted or handled by Django's auth
        self.object.delete()
        messages.success(self.request, f"Éxito al eliminar el grupo {group_name}.")
        # No need to call super().form_valid(form) if manually deleting,
        # but DeleteViewMixin might expect it. If issues, revert to:
        # response = super().form_valid(form)
        # messages.success(self.request, f"Éxito al eliminar el grupo {group_name}.")
        # return response
        return_url = self.get_success_url()
        from django.shortcuts import redirect
        return redirect(return_url)


# Placeholder for GroupDetailView if needed later, e.g., to show users in a group or manage module permissions
class GroupDetailView(LoginRequiredMixin, PermissionMixin, DetailView):
    model = Group
    template_name = 'security/groups/detail.jinja' # Create this template later
    context_object_name = 'group'
    permission_required = 'view_group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'Detalle del Grupo'
        context['title2'] = f'Detalles para {self.object.name}'
        # Add users list and link to manage GroupModulePermissions
        context['users_in_group'] = self.object.user_set.all()
        context['group_module_permissions_url'] = reverse_lazy('security:groupmodulepermission_list', kwargs={'group_pk': self.object.pk})
        context['add_group_module_permission_url'] = reverse_lazy('security:groupmodulepermission_create', kwargs={'group_pk': self.object.pk})
        context['back_url'] = reverse_lazy('security:group_list')
        return context

# GroupModulePermission CRUD Views
class GroupModulePermissionListView(LoginRequiredMixin, PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/group_module_permissions/list.jinja'
    model = GroupModulePermission
    context_object_name = 'group_module_permissions'
    permission_required = 'view_groupmodulepermission' # Assumes this permission exists

    def get_queryset(self):
        self.group = Group.objects.get(pk=self.kwargs['group_pk'])
        q_filter = self.request.GET.get('q')
        query = Q(group=self.group)
        if q_filter:
            query.add(Q(module__name__icontains=q_filter), Q.AND)
        return self.model.objects.filter(query).select_related('module', 'group').order_by('module__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.group
        context['title1'] = f'Permisos para {self.group.name}'
        context['title2'] = 'Listado de Módulos y Permisos Asignados'
        context['create_url'] = reverse_lazy('security:groupmodulepermission_create', kwargs={'group_pk': self.group.pk})
        context['back_url'] = reverse_lazy('security:group_detail', kwargs={'pk': self.group.pk})
        return context

class GroupModulePermissionCreateView(LoginRequiredMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = GroupModulePermission
    template_name = 'security/group_module_permissions/form.jinja'
    form_class = GroupModulePermissionForm
    permission_required = 'add_groupmodulepermission'

    def get_success_url(self):
        return reverse_lazy('security:groupmodulepermission_list', kwargs={'group_pk': self.kwargs['group_pk']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.group = Group.objects.get(pk=self.kwargs['group_pk'])
        kwargs['group_instance'] = self.group
        # Pass initial data for the group
        if self.request.method == 'GET':
            kwargs['initial'] = {'group': self.group}
        elif self.request.method == 'POST':
            # When POSTing, Django's ModelForm handling usually takes care of it via `self.instance.group = self.group`
            # or if 'group' is a field in the form. Since it's HiddenInput, ensure it's in POST data or set on instance.
            data = self.request.POST.copy()
            data['group'] = self.group.pk
            kwargs['data'] = data
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = Group.objects.get(pk=self.kwargs['group_pk'])
        context['title1'] = f'Asignar Permisos a {group.name}'
        context['title2'] = 'Nuevo Módulo y Permisos para el Grupo'
        context['grabar'] = 'Grabar Permiso'
        context['back_url'] = self.get_success_url()
        context['group'] = group
        return context

    def form_valid(self, form):
        form.instance.group = Group.objects.get(pk=self.kwargs['group_pk'])
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al asignar permisos del módulo {form.instance.module.name} al grupo {form.instance.group.name}.")
        return response

class GroupModulePermissionUpdateView(LoginRequiredMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = GroupModulePermission
    template_name = 'security/group_module_permissions/form.jinja'
    form_class = GroupModulePermissionForm
    permission_required = 'change_groupmodulepermission'

    def get_success_url(self):
        # The 'group_pk' needed for the success_url might not be directly in self.kwargs if the URL uses 'pk' for GMP instance.
        # We get it from the instance.
        return reverse_lazy('security:groupmodulepermission_list', kwargs={'group_pk': self.object.group.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # self.object is the GroupModulePermission instance
        kwargs['group_instance'] = self.object.group
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = f'Actualizar Permisos para {self.object.group.name}'
        context['title2'] = f'Editando Permisos del Módulo: {self.object.module.name}'
        context['grabar'] = 'Actualizar Permiso'
        context['back_url'] = self.get_success_url()
        context['group'] = self.object.group
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al actualizar los permisos del módulo {self.object.module.name} para el grupo {self.object.group.name}.")
        return response

class GroupModulePermissionDeleteView(LoginRequiredMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = GroupModulePermission
    template_name = 'core/delete.html'
    permission_required = 'delete_groupmodulepermission'

    def get_success_url(self):
        # Similarly, get group_pk from the object before it's deleted.
        # Store it if needed, or ensure the object is available via a different mechanism if deletion logic in mixin removes it too soon.
        # For now, assuming self.object is available until after success_url is determined.
        return reverse_lazy('security:groupmodulepermission_list', kwargs={'group_pk': self.object.group.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'Eliminar Permiso de Módulo'
        context['grabar'] = 'Eliminar Permiso'
        context['description'] = f"¿Desea eliminar los permisos del módulo {self.object.module.name} para el grupo {self.object.group.name}?"
        context['back_url'] = self.get_success_url()
        return context

    def form_valid(self, form):
        module_name = self.object.module.name
        group_name = self.object.group.name

        # Perform the delete operation
        response = super().form_valid(form) # This calls self.object.delete()

        messages.success(self.request, f"Éxito al eliminar los permisos del módulo {module_name} para el grupo {group_name}.")
        return response
