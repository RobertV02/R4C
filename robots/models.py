from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from orders.models import Order


class Robot(models.Model):
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)
    def __str__(self):
        return f"{self.model}-{self.version}"

    @property
    def serial(self):
        return f"{self.model}-{self.version}"

@receiver(pre_save, sender=Robot)
def check_orders(sender, instance, **kwargs):
    # Проверяем наличие заказов с таким же robot_serial
    orders_with_same_serial = Order.objects.filter(robot_serial=instance.serial)

    if orders_with_same_serial.exists():
        customer_email = orders_with_same_serial.first().customer.email
        send_mail(
            'Ваш заказ в наличии!',
            f'Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.Этот робот теперь в наличии. '
            'Если вам подходит этот вариант - пожалуйста, свяжитесь с нами',
            'rob.pap@mail.ru',
            [customer_email],
            fail_silently=False,
        )
        orders_with_same_serial.delete()