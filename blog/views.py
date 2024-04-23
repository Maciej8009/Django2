from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Post, CommentsPost
from .forms import PostForm, SignUpForm, UpdateUserForm, ChangePasswordForm, CommentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


def post_list(request):
    posts = Post.objects.filter().order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            CommentsPost = form.save(commit=False)
            CommentsPost.author = request.user
            CommentsPost.created_date = timezone.now()
            CommentsPost.postID = post
            CommentsPost.save()
            return redirect('post_detail', pk=post.pk)
        else:
            form = CommentForm()
            return render(request, 'blog/add_comment.html', {'form': form})
    else:
        form = CommentForm()
        return render(request, 'blog/add_comment.html', {'form': form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})



def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, ("Błąd, Spróbuj ponownie!"))
            return redirect('login_user')
    else:
        return render(request, 'authenticate/loginUser.html', {})
    
        


def logout_user(request):
    logout(request)
    messages.success(request, ("Zostałeś wylogowany!"))
    return redirect("/")

def register_user(request):
    signUpForm = SignUpForm()
    if request.method == "POST":
        signUpForm = SignUpForm(request.POST)
        if signUpForm.is_valid():
            signUpForm.save()
            username = signUpForm.cleaned_data['username']
            password = signUpForm.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Konto utworzone pomyślnie!"))
            return redirect('/')
        else:
            messages.success(request, ("Wystąpił problem, spróbuj ponownie"))
            return redirect('register_user')
    else:
        return render(request, 'authenticate/registerUser.html', {'signUpForm':signUpForm})
    

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Zmieniłeś Dane")
            login(request, current_user)
            return redirect('/')
        return render(request, "authenticate/editUser.html", {'user_form': user_form})
    else:
        messages.success(request, "Musisz być zalogowany!")
        return redirect('/')
    

def change_passwd(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            passwd_form = ChangePasswordForm(current_user, request)
            if passwd_form.is_valid():
                passwd_form.save()
                messages.success(request, "Hasło zostało zmienione")
                login(request, current_user)
                return redirect('edit_user')
            else:
                for error in list(passwd_form.errors.values()):
                    messages.error(request, error)
                return redirect('/')
        else:
            passwd_form = ChangePasswordForm(current_user)
            return render(request, "authenticate/changePasswd.html", {'passwd_form': passwd_form})
    else:
        messages.success(request, "Musisz być zalogowany!")
        return redirect('/')