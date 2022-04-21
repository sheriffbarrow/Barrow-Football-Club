from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from bfc.models import Post


class LastPostFeed(Feed):
  title = 'My Barrow fc'
  link = reverse_lazy('bfc:post_feed')
  description = 'News post of My Barrow fc.'

  def items(self):
    return Post.objects.all()[:5]

  def item_title(self, item):
    return item.title

  def item_description(self, item):
    return truncatewords(item.body, 30)