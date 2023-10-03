from celery import shared_task
from .models import Parcel
import redis

@shared_task
def set_usd_to_rub():
    import requests

    redis_client = redis.Redis(host='redis', port=6379, db=0)
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    exchange_rate_data = response.json()['Valute']['USD']['Value']
    redis_client.set('usd_to_rub', exchange_rate_data)


@shared_task
def set_shipping_cost():
    unprocessed_parcels = Parcel.objects.filter(price__isnull=True)
    try:
        redis_client = redis.Redis(host='redis', port=6379, db=0)
        try:
            usd_to_rub = float(redis_client.get('usd_to_rub'))
        except:
            # Этого здесь быть не должно.
            set_usd_to_rub()
            usd_to_rub = float(redis_client.get('usd_to_rub'))
    except:
        usd_to_rub = 30
    for parcel in unprocessed_parcels:
        parcel.price = (parcel.weight * 0.5 + parcel.worth * 0.01) * usd_to_rub
        parcel.save()