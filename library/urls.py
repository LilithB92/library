from rest_framework import routers

from library.apps import LibraryConfig
from library.views import AuthorViewSet

app_name = LibraryConfig.name

router = routers.SimpleRouter()
router.register(r"author", AuthorViewSet, basename="author")


urlpatterns = []

urlpatterns += router.urls
