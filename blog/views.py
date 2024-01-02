from django.views import generic
from django.urls import reverse_lazy

from .models import Post
from .forms import PostForm


class PostListView(generic.ListView):
    # model = Post
    template_name = "blog/posts_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(status="pub").order_by('-datetime_modified')


class PostDetailView(generic.DetailView):
    model = Post


class PostCreateView(generic.CreateView):
    form_class = PostForm
    template_name = "blog/add_post.html"


# .../blog/10/update
class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/add_post.html"


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("post_list")

# def post_list_view(request):
#     posts = Post.objects.filter(status="pub").order_by('-datetime_modified')
#     context = {'posts': posts, "title": "Post List"}
#     return render(request, 'blog/posts_list.html', context)


# def post_detail_view(request, pk):
#     # post = Post.objects.get(pk=pk)
#     # try:
#     #     post = Post.objects.get(pk=pk)
#     # except ObjectDoesNotExist:
#     #     post = None
#     post = get_object_or_404(Post, pk=pk)  # status code: 404
#     context = {
#         "post": post
#     }
#     return render(request, "blog/post_detail.html", context)


# def create_post_view(request):
#     form = NewPostForm(request.POST or None)
#     if request.method == "POST":
#         print(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("post_list")
#     context = {'form': form}
#     return render(request, "blog/add_post.html", context)


# def update_post_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # form = NewPostForm(initial={'title': post.title, "text": post.text, 'status': post.status, 'author': post.author})
#     form = NewPostForm(request.POST or None, instance=post)
#     # if request.method == "POST":
#     if form.is_valid():
#         form.save()
#         return redirect(reverse("post_detail", args=(post.pk,)))
#     context = {'form': form}
#     return render(request, "blog/add_post.html", context)


# def delete_post_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         post.delete()
#         return redirect("post_list")
#     context = {"post": post}
#     return render(request, "blog/post_delete.html", context)
