from django.db import models
   
class Author(models.Model):
    AuthorName = models.CharField("Author Name", max_length=50)
    def __str__(self):
        return self.AuthorName

class Books(models.Model):
    BookName = models.CharField("Book Name", max_length=50)
    BookId = models.IntegerField("Book Id", primary_key=True)
    BookPrice = models.CharField("Book Price", max_length=50)
    Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    def __str__(self):
        return self.BookName     

class Customer(models.Model):
    Name = models.CharField("Customer Name", max_length=50)
    id = models.IntegerField("Customer Id", primary_key=True)
    Book = models.ForeignKey(Books, on_delete=models.CASCADE)
    def __str__(self):
        return self.Name
        