from django.shortcuts import render, redirect
from apps.login_register_app.models import User
from apps.favorite_book_app.models import Book
from django.contrib import messages

# Create your views here.
def book(request):
    if 'id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['id']),
            'all_books': Book.objects.all(),
        }
        print('user is in session')
        return render(request, 'books/add_book.html', context)
    return redirect('/')

def books(request):
    return render(request, 'books/add_book.html')

def logout(request):
    request.session.clear()
    return redirect('/')

def addbook(request):
    errors = Book.objects.validator_add(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/book/add_book')
    else:        
        DBtitle = request.POST['form_add_title']
        DBdesc = request.POST['form_add_description']
        uploaded_by_id = request.session['id']
        uploaded_by = User.objects.get(id=uploaded_by_id)
        new_book = Book.objects.create(
            DBtitle=DBtitle, DBdesc=DBdesc, uploaded_by=uploaded_by)
        new_book.users_who_like.add(uploaded_by)
        return redirect('/book/add_book')

def book_click(request, bookid):
    current_book = Book.objects.get(id=bookid)
    book_creator_id = current_book.uploaded_by_id
    if (request.session['id'] == book_creator_id):
        context = {
            'book': current_book,
            'users': current_book.users_who_like.all()
        }
        return render(request, 'books/edit_books.html', context)
    else:
        context = {
            'book': current_book,
            'users': current_book.users_who_like.all()
        }
        return render(request, 'books/view_books.html', context)

def edit_book(request, bookid):
    errors = Book.objects.validator_edit(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value,extra_tags=key)
            return redirect('/book/'+str(bookid))
    else:
        current_book = Book.objects.get(id=bookid)
        new_title = request.POST['form_edit_title']
        new_desc = request.POST['form_edit_description']
        current_book.DBtitle = new_title
        current_book.DBdesc = new_desc
        current_book.save()

        return redirect('/books/'+str(bookid))