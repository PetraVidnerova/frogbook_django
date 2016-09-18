from django.conf.urls import url
from . import views

app_name = 'pulci'
urlpatterns = [
    url(r"vote(?P<id>[0-9]+)", views.vote, name="vote"),
    url(r"detail(?P<id>[0-9]+)", views.detail, name="detail"),
    #url(r"init", views.fill_datebase, name="init"), # should be commented out
    url(r"sort_(?P<sort_type>(date|likes))", views.pulci, name="pulci"),
    url(r"^$", views.pulci, name="pulci")
]
