from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from BookStoreWebsite.models import Books, Author
from BookStoreWebsite.forms import BookForm, AuthorInput
import re


def book(request):
    if request.user.is_authenticated: 
        # import ipdb
        # ipdb.set_trace()
        form = BookForm()
        bookList = Books.objects.all()
        # UserSname = User.objects.get(username=request.user)
        # print(UserSname)
        if request.method == 'POST':    
            form = BookForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.User = request.user
            form.save()
            return redirect('book')
        context = {'bookList':bookList, 'form':form}
        return render(request, 'books.html', context)
    else:
        messages.error(request, 'You cannot access this page Please Login')
        return redirect('/')
    

def author(request):
    if request.user.is_authenticated: 
        author = AuthorInput()
        authorList = Author.objects.order_by('Author')
        #authorList = Author.objects.all() (Gets all the elements but unsorted)
        #order_by sorts the authorList alphabetically
        if request.method == 'POST':
            author = AuthorInput(request.POST)
        if author.is_valid():
            author.save()
            return redirect('author')
        context = {'authorList':authorList, 'author':author}
        return render(request, 'authors.html',context)
    else:
        messages.error(request, 'You cannot access this page Please Login')
        return redirect('/')
    
    
   
def delete(request, id):
    if request.method == 'POST':
        Book = Books.objects.get(BookId = id)
        Book.delete()
        return redirect('book')
    return render(request, 'books.html')


def details(request, id):
    if request.method == 'POST':
        Book = Books.objects.get(BookId = id)
    context = {'Book':Book}
    return render(request, 'bookdetails.html', context)


def edit(request, id):
    if request.user == Books.User:
        # Book = Books.objects.get(BookId = id)
        # or 
        Book = get_object_or_404(Books, BookId = id)
        #returns a 404 error if the BookId is not found
        form = BookForm(request.POST or None,instance=Book)
        if form.is_valid():
            form.save()
            messages.info(request, 'Book Updated Successfully')
            return redirect('book')
        context = {'form':form}
        return render(request, 'editBook.html', context)
    else:
        logout(request)
        messages.error(request, 'You cannot access this page Please Login')
        return redirect('/')
    
    
def signup(request):
    if request.method == 'POST':
        userName = request.POST.get('Username')
        email = request.POST.get('Email')
        pass1 = request.POST.get('Pass1')
        pass2 = request.POST.get('Pass2')
        print(pass1,pass2)
        if User.objects.filter(username = userName).exists():
            messages.info(request, 'User already exists')
            return redirect('/')
        elif len(pass1)<5:
            messages.info(request, 'Password too short')
        elif pass1 != pass2:
            print('True')
            messages.info(request, 'Passwords do not Match')
            return redirect('/')
        elif re.search('[!@#$%&()\-_[\]}{;:"./<>?]', pass1) is None:
            messages.info(request, "Password denied: must contain a special character") 
        else:
            user = User.objects.create_user(userName, email, pass1)
            user.save()
            messages.success(request, 'You are now a registered User')
        return redirect('/')


def signin(request):
    if request.method == 'POST':
        # import ipdb
        # ipdb.set_trace()
        # ipdb checks for errors line by line so it is really helpful if you want to see where your code goes bad.
        Username = request.POST['Username']
        # if request.POST use [] instead of request.POST.get() 
        Password = request.POST['Password']
        user = authenticate(username = Username, password = Password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('index')
        else:
            messages.info(request, 'Username and Password donot match')
            return redirect('/')
    return redirect('/')


def signout(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return render(request, 'index.html')