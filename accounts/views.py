from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

def registerView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "register.html")

        user = User.objects.create_user(username=username, password=password)
        user.user_type = user_type
        user.save()

        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('books:catalog')

    return render(request, "register.html")

def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('books:catalog')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

@login_required
def logoutView(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('accounts:login')

@login_required
def userListView(request):
    users = User.objects.all()
    return render(request, "userlist.html", {"users": users})

@login_required
def userProfileView(request, user_id):
    from books.models import ReadBook

    profile_user = get_object_or_404(User, pk=user_id)
    read_books = ReadBook.objects.filter(user=profile_user).select_related('book')
    return render(request, "userprofile.html", {
        "profile_user": profile_user,
        "read_books": read_books
    })