from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LinkViewSet, CollectionViewSet, RegisterAPI, LoginAPI, PasswordResetView


router = DefaultRouter()
router.register(r'links', LinkViewSet, basename='link')
router.register(r'collections', CollectionViewSet, basename='collection')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),

    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),


    path('auth/', include('rest_framework.urls'))
]
