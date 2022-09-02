from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    Author = models.CharField(("Author Name"), max_length=50)
    def __str__(self):
        return self.Author
    
class Books(models.Model):
    BookName = models.CharField(("Book Name"), max_length=50, blank=True)
    BookId = models.AutoField(("Book Id"), primary_key=True)
    BookPrice = models.IntegerField(("BookPrice"), blank=True)
    Author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    def __str__(self):
        return self.BookName

