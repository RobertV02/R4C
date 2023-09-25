from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import json

from .models import Robot  # Замените на путь к вашей модели


class CreateRobotTest(TestCase):
    def test_create_robot(self):
        # Создаем JSON-данные для запроса
        data = {
            'model': 'R2',
            'version': 'D2',
            'created': '2022-12-31 23:59:59'
        }

        # Отправляем POST-запрос к вашему API-endpoint
        response = self.client.post(reverse('create_robot'), json.dumps(data), content_type='application/json')

        # Проверяем, что получили ожидаемый статус код (201 - Created)
        self.assertEqual(response.status_code, 201)

        # Проверяем, что запись о роботе была создана в базе данных
        self.assertTrue(Robot.objects.filter(model='R2', version='D2').exists())

    def test_create_robot_invalid_data(self):
        # Отправляем POST-запрос с неполными данными
        data = {
            'model': 'R2',
            'version': 'D2'
        }

        # Отправляем POST-запрос с недостающими данными
        response = self.client.post(reverse('create_robot'), json.dumps(data), content_type='application/json')

        # Проверяем, что получили ожидаемый статус код (400 - Bad Request)
        self.assertEqual(response.status_code, 400)

        # Проверяем, что запись о роботе не была создана в базе данных
        self.assertFalse(Robot.objects.filter(model='R2', version='D2').exists())
    def test_create_robot_invalid_validation_data(self):
        # Отправляем POST-запрос с неполными данными
        data = {
            'model': 'R2R',
            'version': 'D2е',
            'created': '2022-12-31T23:59:59Z',
        }

        # Отправляем POST-запрос с недостающими данными
        response = self.client.post(reverse('create_robot'), json.dumps(data), content_type='application/json')

        # Проверяем, что получили ожидаемый статус код (400 - Bad Request)
        self.assertEqual(response.status_code, 400)

        # Проверяем, что запись о роботе не была создана в базе данных
        self.assertFalse(Robot.objects.filter(model='R2R', version='D2е').exists())
