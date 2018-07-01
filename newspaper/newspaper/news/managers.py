from django.db import models
from django.db.models.query import QuerySet

from datetime import datetime


class NewsQuerySet(QuerySet):

    def news_published(self):
        return self.filter(publish_date__lte=datetime.now())\
                   .order_by('publish_date')

    def news_next_published(self):
        return self.filter(publish_date__gte=datetime.now())\
            .order_by('publish_date')


class NewsManager(models.Manager):

    def get_queryset(self):
        return NewsQuerySet(self.model, using=self._db)

    def news_published(self):
        return self.get_queryset().news_published()

    def news_next_published(self):
        return self.get_queryset().news_next_published()
