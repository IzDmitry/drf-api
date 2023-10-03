import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

class Parcel(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    weight = models.FloatField(validators=[MinValueValidator(0.1)], null=False, blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, null=False, blank=False)
    worth = models.FloatField(validators=[MinValueValidator(0.0)], null=False, blank=False)
    price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Переопределили метод сохранения, чтобы сгенерировать уникальный идентификатор посылки.
        """
        if not self.id:
            self.id = self._generate_unique_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    def _generate_unique_id(self):
        """
        Создаёт уникальный идентификатор посылки.
        """
        while True:
            # генерирует случайное 10-значное целое число
            unique_id = uuid.uuid4().int % (10 ** 10)
            # проверяет существует ли он уже в базе данных
            if not Parcel.objects.filter(id=unique_id).exists():
                return unique_id

