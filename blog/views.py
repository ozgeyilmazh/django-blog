from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from blog.models import Post, Category, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from blog.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import F
# Create your views here.

def index(request):
    context = dict()
    post_list = Post.objects.all()

    query = request.GET.get('q')

    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(user__first_name__icontains=query)
        ).distinct()
        
    paginator = Paginator(post_list, 3) # bir sayfada kaç tane görünmesi gerek
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    
    context['posts'] = posts
    context['post_list'] = Post.objects.distinct()
    context['cat'] = Category.objects.all()
    context['popular_list'] = Post.objects.all().order_by('-read', '-id')[:3]

    
    #   pagination, search
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post=post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    
    read = post.read
    read += 1
    degıs = Post.objects.filter(slug=slug).update(read=read)

    context = {
        'post' : post,
        'form' : form,
    }
    return render(request, 'detail.html', context)


def add_comment_to_post(request, pk):
    post = Pos.get_object_or_404(Post, pk=pk)

    if request.POST == "POST":
        form  = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'forms.html', {'form': form})


@login_required
def comment_approved(request,pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.approve()
    return redirect('detail', pk = comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.delete()
    return redirect('detail', pk = comment.post.pk)


def category_show(request, category_slug):
    context = dict()
    context['category'] = get_object_or_404(
        Category, slug=category_slug,
    )

    context['items'] = Post.objects.filter(
        category=context['category'],
    )

    return render(request, 'category_show.html', context)

