from django.shortcuts import render
from robots.models import Robot
from orders.models import Order
from customers.models import Customer
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            need_serial = data.get('serial')
            if email and need_serial:
                if '-' in need_serial:
                    need_model, need_version = need_serial.split('-')  # Разделить need_serial на model и version
                    if len(need_model) == 2 and len(need_version) == 2:

                        # Фильтруем объекты Robot по model и version
                        robots = Robot.objects.filter(model=need_model, version=need_version).first()

                        if robots:
                            robots.delete()
                            return JsonResponse({'message': 'Покупка успешна'}, status=200)
                        else:
                            # Проверяем существует ли покупатель с указанным email
                            customer, created = Customer.objects.get_or_create(email=email)

                            # Создаем заказ и связываем его с покупателем
                            order = Order(customer=customer, robot_serial=need_serial)
                            order.save()
                            return JsonResponse({'message': 'Заказ создан, ожидайте письма когда товар будет в наличии'}, status=201)
                    else:
                        return JsonResponse({'error': 'Invalid data'}, status=400)
                else:
                    return JsonResponse({'error': 'Invalid data'}, status=400)
            else:
                return JsonResponse({'error': 'Invalid data'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


