from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category-list'),
    path('<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('<slug:slug>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('<slug:slug>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('brands/', views.BrandListView.as_view(), name='brand-list'),
    path('brands/create/', views.BrandCreateView.as_view(), name='brand-create'),
    path('brands/<slug:slug>/update/', views.BrandUpdateView.as_view(), name='brand-update'),
    path('brands/<slug:slug>/delete/', views.BrandDeleteView.as_view(), name='brand-delete'),
]
