from django.shortcuts import render
from django.http import HttpResponse
from .models import Bookmark

# Create your views here.
def bookmarks(request):

    bookmarks = Bookmark.objects.order_by("-date")
    context = {
        "bookmarks" : bookmarks
    }
    return render(request, "bookmarks/index.html", context)