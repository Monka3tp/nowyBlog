

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.forms import CommentForm
from django.forms import ModelForm
from blog.models import Post

'''
# Create your views here.
def post_list(request):
    posts = Post.published.all()
    return render(request, "blog/post/list.html", context={"posts": posts})
'''

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3 #ile elementow ma byc na jednej stronie
    template_name = "blog/post/list.html"

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post , slug=slug, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
    comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', context={"post": post
                                                             , "comments": comments
                                                             , "comment_form": comment_form})