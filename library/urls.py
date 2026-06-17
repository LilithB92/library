from rest_framework import routers

from library.apps import LibraryConfig
from library.views import AuthorViewSet, BookViewSet

app_name = LibraryConfig.name

router = routers.SimpleRouter()
router.register(r"author", AuthorViewSet, basename="author")
router.register(r"book", BookViewSet, basename="book")


urlpatterns = []

urlpatterns += router.urls
