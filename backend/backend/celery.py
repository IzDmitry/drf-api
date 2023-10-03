import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Периодическая задача для запуска функции set_shipping_cost каждые пять минут.
app.conf.beat_schedule = {
    'set_usd_to_rub': {
        'task': 'parcel.tasks.set_usd_to_rub',
        'schedule': crontab(hour='*/24'),
    },
    'set-shipping-cost': {
        'task': 'parcel.tasks.set_shipping_cost',
        'schedule': crontab(minute='*/5'),
    },
}

if __name__ == '__main__':
    app.start()