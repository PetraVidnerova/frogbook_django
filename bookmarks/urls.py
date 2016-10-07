from django.conf.urls import url
from . import views

app_name = "bookmarks"
urlpatterns = [
    url(r"^$", views.bookmarks, name="bookmarks")
]
