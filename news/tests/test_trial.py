from django.test import TestCase
from unittest import skip
# Импортируем модель, чтобы работать с ней в тестах.
from news.models import News


# Создаём тестовый класс с произвольным названием, наследуем его от TestCase.
class TestNews(TestCase):

    # В методе класса setUpTestData создаём тестовые объекты.
    # Оборачиваем метод соответствующим декоратором.
    @classmethod
    @skip('Пропускаем тест из test_trial')
    def setUpTestData(cls):
        # Стандартным методом Django ORM create() создаём объект класса.
        # Присваиваем объект атрибуту класса: назовём его news.
        cls.news = News.objects.create(
            title='Заголовок новости',
            text='Тестовый текст',
        )
    # @skip('Пропускаем тест')
    # Проверим, что объект действительно было создан.
    def test_successful_creation(self):
        # При помощи обычного ORM-метода посчитаем количество записей в базе.
        news_count = News.objects.count()
        # Сравним полученное число с единицей.
        self.assertEqual(news_count, 1)