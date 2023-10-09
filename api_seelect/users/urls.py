from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

urlpatterns = [
    # Request to get all users.
    path('', views.UserList.as_view(), name='user-list'),
    # Request to get all users from a role.
    path('<str:role>/', views.RoleList.as_view(), name='role-list'),
    # Request to get specific user from a role by id.
    path('<str:role>/<int:pk>/', views.RoleDetail.as_view(), name='role-detail'),
    # Request to get specific profile from a role by id.
    path('<str:role>/<int:pk>/profile/', views.UserProfileDetail.as_view(), name='profile-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)