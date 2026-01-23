from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.review_create, name='review_create'),
    path('edit/<int:review_id>/', views.review_edit, name='review_edit'),
    path('delete/<int:review_id>/', views.review_delete, name='review_delete'),
    path('vote/<int:review_id>/<str:choice>', views.review_vote, name='review_vote'),
    path('report/<int:review_id>/', views.review_report, name='review_report'),
]