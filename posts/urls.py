from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('details/<slug>', views.Details.as_view(), name='details'),
    path('category/<str:category>', views.Category.as_view(), name='category')
]
