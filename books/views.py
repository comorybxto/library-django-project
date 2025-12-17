from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, ReadBook

@login_required
def catalogView(request):
    books = Book.objects.all()
    
    # Filtering
    genre_filter = request.GET.get('genre')
    author_filter = request.GET.get('author')
    
    if genre_filter and genre_filter != 'all':
        books = books.filter(genre=genre_filter)
    
    if author_filter:
        books = books.filter(author__icontains=author_filter)
    
    # Ordering
    order_by = request.GET.get('order_by', 'title')
    if order_by == 'year':
        books = books.order_by('-year')
    elif order_by == 'author':
        books = books.order_by('author')
    elif order_by == 'genre':
        books = books.order_by('genre')
    else:  # default: title
        books = books.order_by('title')
    
    user_read_books = []
    if request.user.user_type == 'reader':
        user_read_books = ReadBook.objects.filter(user=request.user).values_list('book_id', flat=True)
    
    # Get unique authors and genres for filters
    authors = Book.objects.values_list('author', flat=True).distinct().order_by('author')
    genres = Book.GENRE_CHOICES
    
    return render(request, "catalog.html", {
        "books": books,
        "user_read_books": user_read_books,
        "authors": authors,
        "genres": genres,
        "current_genre": genre_filter or 'all',
        "current_author": author_filter or '',
        "current_order": order_by,
    })

@login_required
def registerBookView(request):
    if request.user.user_type != 'librarian':
        messages.error(request, "Only librarians can register books")
        return redirect('books:catalog')
    
    if request.method == "POST":
        book = Book()
        book.title = request.POST["title"]
        book.author = request.POST["author"]
        book.year = request.POST["year"]
        book.description = request.POST.get("description", "")
        book.genre = request.POST.get("genre", "other")
        book.save()
        messages.success(request, "Book registered successfully!")
        return redirect('books:catalog')
    
    return render(request, "registerbook.html")

@login_required
def editBookView(request, book_id):
    if request.user.user_type != 'librarian':
        messages.error(request, "Only librarians can edit books")
        return redirect('books:catalog')
    
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == "POST":
        book.title = request.POST["title"]
        book.author = request.POST["author"]
        book.year = request.POST["year"]
        book.description = request.POST.get("description", "")
        book.genre = request.POST.get("genre", "other")
        book.save()
        messages.success(request, "Book updated successfully!")
        return redirect('books:catalog')
    
    return render(request, "editbook.html", {"book": book})

@login_required
def deleteBookView(request, book_id):
    if request.user.user_type != 'librarian':
        messages.error(request, "Only librarians can delete books")
        return redirect('books:catalog')
    
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect('books:catalog')

@login_required
def markAsReadView(request, book_id):
    if request.user.user_type != 'reader':
        messages.error(request, "Only readers can mark books as read")
        return redirect('books:catalog')
    
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == "POST":
        rating = request.POST.get("rating")
        if not rating or int(rating) < 1 or int(rating) > 5:
            messages.error(request, "Please provide a valid rating (1-5)")
            return redirect('books:catalog')
        
        read_book, created = ReadBook.objects.get_or_create(
            user=request.user, 
            book=book,
            defaults={'rating': int(rating)}
        )
        if not created:
            read_book.rating = int(rating)
            read_book.save()
        
        messages.success(request, f"'{book.title}' marked as read with {rating} stars!")
        return redirect('books:catalog')
    
    # This shouldn't happen with the modal, but just in case
    messages.error(request, "Invalid request")
    return redirect('books:catalog')

@login_required
def myProfileView(request):
    if request.user.user_type != 'reader':
        messages.error(request, "Only readers have profiles")
        return redirect('books:catalog')
    
    read_books = ReadBook.objects.filter(user=request.user).select_related('book')
    return render(request, "myprofile.html", {"read_books": read_books})

@login_required
def removeReadBookView(request, readbook_id):
    if request.user.user_type != 'reader':
        messages.error(request, "Only readers can remove books from their profile")
        return redirect('books:catalog')
    
    read_book = get_object_or_404(ReadBook, pk=readbook_id, user=request.user)
    read_book.delete()
    messages.success(request, "Book removed from your profile!")
    return redirect('books:myprofile')