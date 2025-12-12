"""
URL config for the `county` Django app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recall_server.county.views import(
        CountyViewSet,
        SenatorViewSet,
        ConstituencyViewSet,
        MCAViewSet,
        WardViewSet
        )


router = DefaultRouter()
router.register(r'', CountyViewSet, basename='county')
router.register(r'', SenatorViewSet, basename='senator')
router.register(r'', ConstituencyViewSet, basename='constituency')
router.register(r'', MCAViewSet, basename='mca')
router.register(r'', WardViewSet, basename='ward')

urlpatterns = [
        path('', include(router.urls)),
        ]
