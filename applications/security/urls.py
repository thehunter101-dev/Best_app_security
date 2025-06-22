from django.urls import path

from applications.security.views.auth import signin, signout
from applications.security.views.menu import MenuCreateView, MenuDeleteView, MenuListView, MenuUpdateView
from applications.security.views.module import ModuleCreateView, ModuleDeleteView, ModuleListView, ModuleUpdateView
from applications.security.views.group import (
    GroupListView, GroupCreateView, GroupUpdateView, GroupDeleteView, GroupDetailView,
    GroupModulePermissionListView, GroupModulePermissionCreateView,
    GroupModulePermissionUpdateView, GroupModulePermissionDeleteView
)
from applications.security.views.user import UserUpdateView
# Placeholder for UserListView if it were to be created
from django.views.generic import TemplateView


app_name='security' # define un espacio de nombre para la aplicacion
urlpatterns = [

  # rutas de modulos
  path('module_list/',ModuleListView.as_view() ,name="module_list"),
  path('module_create/', ModuleCreateView.as_view(),name="module_create"),
  path('module_update/<int:pk>/', ModuleUpdateView.as_view(),name='module_update'),
  path('module_delete/<int:pk>/', ModuleDeleteView.as_view(),name='module_delete'),

  # rutas de menus
  path('menu_list/',MenuListView.as_view() ,name="menu_list"),
  path('menu_create/', MenuCreateView.as_view(),name="menu_create"),
  path('menu_update/<int:pk>/', MenuUpdateView.as_view(),name='menu_update'),
  path('menu_delete/<int:pk>/', MenuDeleteView.as_view(),name='menu_delete'),

  # rutas de grupos
  path('group_list/', GroupListView.as_view(), name="group_list"),
  path('group_create/', GroupCreateView.as_view(), name="group_create"),
  path('group_detail/<int:pk>/', GroupDetailView.as_view(), name='group_detail'),
  path('group_update/<int:pk>/', GroupUpdateView.as_view(), name='group_update'),
  path('group_delete/<int:pk>/', GroupDeleteView.as_view(), name='group_delete'),

  # rutas de GroupModulePermission (asociadas a un grupo específico)
  path('group/<int:group_pk>/permissions/', GroupModulePermissionListView.as_view(), name='groupmodulepermission_list'),
  path('group/<int:group_pk>/permissions/add/', GroupModulePermissionCreateView.as_view(), name='groupmodulepermission_create'),
  path('groupmodulepermission/<int:pk>/update/', GroupModulePermissionUpdateView.as_view(), name='groupmodulepermission_update'),
  path('groupmodulepermission/<int:pk>/delete/', GroupModulePermissionDeleteView.as_view(), name='groupmodulepermission_delete'),

  # rutas de usuarios
  # Placeholder for user_list - replace with actual UserListView when created
  path('user_list/', TemplateView.as_view(template_name="core/coming_soon.html"), name='user_list'),
  path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
  # Add other user routes (create, detail, delete) here when implemented

  # rutas de autenticacion
  path('logout/', signout, name='signout'),
  path('signin/', signin, name='signin'),
]
