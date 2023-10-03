from django.core.management.base import BaseCommand
from ...tasks import set_shipping_cost


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        set_shipping_cost()