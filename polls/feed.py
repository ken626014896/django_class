from django.contrib.syndication.views import Feed
from django.urls import reverse
from polls.models import Question

class LatestEntriesFeed(Feed):
    title = "Police beat site news"
    link = "/sitenews/"
    description = "Updates on changes and additions to police beat central."

    def items(self):
        return Question.objects.all()

    def item_title(self, item):
        return item.question_text

    def item_data(self, item):
        return item.pub_date

    # item_link is only needed if NewsItem has no get_absolute_url method.
    # def item_link(self, item):
    #     return reverse('news-item', args=[item.pk])