from django.core.management.base import BaseCommand
from ...models import Category


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        categorys = ['Одежда', 'Электроника', 'Разное']
        for category in categorys:
        	Category.objects.get_or_create(name=category)