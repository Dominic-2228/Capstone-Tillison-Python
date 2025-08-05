"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import BookingTimesView, PackageServicesView, PackageView, ReviewsView, ServicesView, UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'reviews', ReviewsView, 'review')
router.register(r'services', ServicesView, 'service')
router.register(r'packages', PackageView, 'package')
router.register(r'packageservices', PackageServicesView, 'packageservice')
router.register(r'bookingtimes', BookingTimesView, 'bookingtime')
router.register(r'users', UserViewSet, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls)
]
