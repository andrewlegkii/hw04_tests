from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from posts.forms import CommentForm, PostForm
from posts.models import Follow, Group, Post, User
from django.views.decorators.cache import cache_page

from yatube.settings import PAGINATION_NUM


def pagination(request, post_list, num_on_page):
    paginator = Paginator(post_list, num_on_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

@cache_page(20)
def index(request):
    """View - функция для главной страницы проекта."""

    post_list = Post.objects.all()
    page_obj = pagination(request, post_list, PAGINATION_NUM)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """View - функция для страницы с постами, отфильтрованными по группам."""

    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = pagination(request, posts, PAGINATION_NUM)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """View - функция для страницы с постами пользователя,
       вошедшего на сайт.
    """
    author = get_object_or_404(User, username=username)
    user = author.posts.all()
    page_obj = pagination(request, user, PAGINATION_NUM)

    context = {'author': author,
               'page_obj': page_obj,
               }
    return render(request, 'posts/profile.html', context)


def post_view(request, post_id):
    """View - функция для страницы определенного поста."""

    post = get_object_or_404(Post, pk=post_id)

    context = {'post': post}
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):

    form = PostForm(request.POST or None)
    """View - функция для создания поста."""

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user.username)
        return render(request, 'posts/create_post.html', {"form": form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {"form": form, })


@login_required
def post_edit(request, post_id):
    """View - функция для редактирования проекта."""

    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post_id)
    return render(request, 'posts/create_post.html',
                  {"form": form, 'post': post, })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Выводит посты авторов, на которых
       подписан текущий пользователь."""
    template = 'posts/follow.html'
    user = request.user
    post_list = Post.objects.filter(
        author__following__user=user
    )
    paginator = Paginator(post_list, PAGINATION_NUM)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """Делает подписку на автора."""
    user = request.user
    author = get_object_or_404(User, username=username)
    if author != user:
        user.follower.get_or_create(
            user=user,
            author=author
        )
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    """Отписывает пользователя от автора."""
    user = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(
        user=user,
        author=author
    )
    if follow.exists():
        follow.delete()
    return redirect('posts:profile', username)


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
