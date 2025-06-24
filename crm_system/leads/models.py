from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class UserRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("done", "Завершена"),
    ]

    name = models.CharField("Имя", max_length=50)
    surname = models.CharField("Фамилия", max_length=50)
    phone = models.CharField("Телефон", max_length=15)
    orderinfo = models.TextField("Описание заявки")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("Дата создания", default=timezone.now)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} {self.surname} - {self.phone}"



