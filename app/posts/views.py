from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView

from .models import Post, IPAddress


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(",")[0]
    else:
        ip_address = request.META.get("REMOTE_ADDR")
    return ip_address


class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        ip_address = get_client_ip(self.request)
        if IPAddress.objects.filter(ip_address=ip_address).exists():
            post_slug = request.GET.get("post-slug")
            post = Post.objects.get(slug=post_slug)
            post.views.add(IPAddress.objects.get(ip_address=ip_address))
        else:
            IPAddress.objects.create(ip_address=ip_address)
            post_slug = request.GET.get("post-slug")
            post = Post.objects.get(slug=post_slug)
            post.views.add(IPAddress.objects.get(ip_address=ip_address))
        return self.render_to_response(context)


class PostListView(ListView):
    model = Post
    paginate_by = 10


class PostCreateView(CreateView):
    model = Post
    fields = ["post_name", "post_content"]

    success_url = "/"
