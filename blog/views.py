from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, PostCountView
from blog.forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from taggit.models import Tag


def post_list(request, tag_slug=None):
    object_list = Post.objects.filter(status=1).order_by('-created_on')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым число, возращаемся на 1 страницу
        post_list = paginator.page(1)
    except EmptyPage:
        # Если страница находится вне диапазона поиска, вернуть последнюю страницу поиска
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'post/home.html', {'page': page, 'post_list': post_list, 'tag': tag})


def post_detail(request, slug):
    template_name = 'post/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    is_views = PostCountView.objects.filter(postId=post.id, sesId=session_key)
    if is_views.count() == 0 and str(session_key) != 'None':
        views = PostCountView()
        views.sesId = session_key
        views.postId = post
        views.save()
        post.count_views += 1
        post.save()
    comments = post.comments.filter(active=True)
    new_comment = None
    # Коммент опубликован
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем объект комментарий, но не сохраняем его в базу
            new_comment = comment_form.save(commit=False)
            # Назначаем соответствующему посту комментарий
            new_comment.post = post
            # Сохраняем комментарий
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'post': post, 'comments': comments,
                                           'new_comment': new_comment, 'comment_form': comment_form})


def post_like(request, slug):
    if slug in request.COOKIES:
        return HttpResponseRedirect('/')
    else:
        post = get_object_or_404(Post, slug=slug)
        post.likes += 1
        post.save()
        response = HttpResponseRedirect('/')
        response.set_cookie(slug, "test")
        return response


def post_dislike(request, slug):
    if slug in request.COOKIES:
        return HttpResponseRedirect('/')
    else:
        post = get_object_or_404(Post, slug=slug)
        post.dislikes += 1
        post.save()
        response = HttpResponseRedirect('/')
        response.set_cookie(slug, "test")
        return response
