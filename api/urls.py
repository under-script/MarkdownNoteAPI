from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'notes', views.NoteViewSet, basename='note')
urlpatterns = router.urls
