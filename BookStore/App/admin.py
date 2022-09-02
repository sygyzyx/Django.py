from django.contrib import admin
from .models import Author, Customer, Books

admin.site.register(Author)
admin.site.register(Customer)
admin.site.register(Books)
