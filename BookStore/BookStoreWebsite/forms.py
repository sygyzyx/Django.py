from django.forms import ModelForm
from .models import Books, Author


class BookForm(ModelForm):
    class Meta:
        model = Books
        exclude = ['User',]
        
class AuthorInput(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'