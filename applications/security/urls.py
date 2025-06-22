from django.urls import path

from applications.security.views.auth import signin, signout
from applications.security.views.menu import MenuCreateView, MenuDeleteView, MenuListView, MenuUpdateView
from applications.security.views.module import ModuleCreateView, ModuleDeleteView, ModuleListView, ModuleUpdateView
from applications.security.views import user as user_views # Import user views

app_name='security' # define un espacio de nombre para la aplicacion
urlpatterns = [

  # Rutas de Usuarios
  path('users/', user_views.UserListView.as_view(), name="user_list"),
  path('users/create/', user_views.UserCreateView.as_view(), name="user_create"),
  path('users/<int:pk>/', user_views.UserDetailView.as_view(), name="user_detail"),
  path('users/update/<int:pk>/', user_views.UserUpdateView.as_view(), name="user_update"),
  path('users/delete/<int:pk>/', user_views.UserDeleteView.as_view(), name="user_delete"),

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

  # rutas de autenticacion
  path('logout/', signout, name='signout'),
  path('signin/', signin, name='signin'),
]
