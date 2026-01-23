from django.urls import path, include
from . import views

urlpatterns = [
    path('show/', views.product_list, name='product_list'),
    path('show/<int:id>/', views.product_detail, name='product_detail'),
    path('add/', views.product_create, name='product_create'),
    path('edit/<int:id>/', views.product_update, name='product_update'),
    path('delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('edit/image/<int:image_id>/', views.product_image_delete, name='product_image_delete'),
    path('pdf/<int:product_id>/', views.generate_pdf, name='product_pdf'),

    path('<int:product_id>/reviews/', include('reviews.urls')),
]