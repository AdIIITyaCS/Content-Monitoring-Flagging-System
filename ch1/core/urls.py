from django.urls import path,include
from rest_framework.routers import DefaultRouter
from core.views import KeywordViewSet,FlagViewSet, run_scan

router=DefaultRouter()
router.register(r'keywords', KeywordViewSet, basename='keyword')
router.register(r'flags', FlagViewSet, basename='flag')

urlpatterns = [
    path('', include(router.urls)),
    path('scan/', run_scan,name='run_scan'),
]
