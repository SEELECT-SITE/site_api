from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from kits import views

urlpatterns = [
    # Request to get all kits.
    path('', views.KitsList.as_view(), name='kits-list'),
    # Request to get specific kit by id.
    path('<int:pk>/', views.KitsDetail.as_view(), name='kits-detail'),
    # Request to get all kits models.
    path('models/', views.KitsModelsList.as_view(), name='kits-models-list'),
    # Request to get specific kit model by id.
    path('models/<int:pk>/', views.KitsModelsDetail.as_view(), name='kits-models-detail'),
    # Requesto to confirm payement
    path('<int:pk>/confirm_payement/', views.confirm_payement, name='kits-confirm-payement'),
    # Request to get all kits discounts.
    path('discount/', views.KitsDiscountList.as_view(), name='kits-discount-list'),
    # Request to get specific kit discount by id.
    path('discount/<int:pk>/', views.KitsDiscountDetail.as_view(), name='kits-discount-detail'),
    # Requesto to change the discount of the kit.   
    path('<int:pk>/change_discount/', views.change_discount, name='kits-change-discount'),
]

urlpatterns = format_suffix_patterns(urlpatterns)