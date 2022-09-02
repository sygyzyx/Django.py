from django.shortcuts import render
from BookStoreWebsite.models import Books


def index(request):
    Book = Books.objects.all()
    context = {'bookList':Book}
    return render(request, 'index.html', context)


