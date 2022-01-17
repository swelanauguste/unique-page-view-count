from django.db import models
from django.utils.text import slugify


class IPAddress(models.Model):
    """
    This class represents an IP address.
    """

    ip_address = models.GenericIPAddressField(
        verbose_name="IP Address",
        help_text="The IP address of the client.",
        unique=True,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "IP Address"
        verbose_name_plural = "IP Addresses"

    def __str__(self):
        return self.ip_address


class Post(models.Model):
    post_name = models.CharField(max_length=100)
    post_content = models.TextField(blank=True, null=True)
    post_created = models.DateTimeField(auto_now_add=True, null=True)
    post_updated = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    views = models.ManyToManyField(IPAddress, related_name="post_views")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.post_name)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/post/%s/" % self.slug

    class Meta:
        ordering = ["post_created"]

    @property
    def total_view_count(self):
        return self.views.count()

    def __str__(self):
        return self.post_name
