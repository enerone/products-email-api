from rest_framework import routers
from . import views
from django.urls import path, include

from .views import emails_list

router=routers.DefaultRouter()

router.register('product', viewset=views.ProductList)

urlpatterns = [
    path('', include(router.urls)),
    path('list/',emails_list)
]