
from django.core.management.base import BaseCommand

from newspaper.news.models import News


class Command(BaseCommand):
    help = 'count the news'

    def handle(self, *args, **options):
        # import pdb; pdb.set_trace() # añadir punto de ruptura
        print(News.objects.cunt())
