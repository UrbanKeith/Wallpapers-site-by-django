from django.urls import path
from . import views

app_name = 'wallpapers_main'
urlpatterns = [
    path('load', views.load, name='load'),
    path('load/result', views.load_result, name='load_result'),

    path('sort', views.sort, name='sort'),
    path('category_take', views.category_take, name = 'category_take'),

    path('category/<str:category>', views.view_image, name = 'category'),
    path('category/<str:category>/<int:page>', views.view_image, name = 'category_page'),

    path('index/<str:image_name>', views.view_image_page, name = 'image_page'),

    path('error', views.error_redirect, name = 'error_redirect'),

    path('', views.view_image, name = 'recommend'),
]
