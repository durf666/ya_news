from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
from news.models import Comment, News
from news.forms import CommentForm

User = get_user_model()


class TestHomePage(TestCase):
    HOME_URL = reverse('news:home')

    @classmethod
    def setUpTestData(cls):
        News.objects.bulk_create(
            News(title=f'Новость {index}', text='Просто текст.')
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        )

    def test_news_count(self):
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        news_count = object_list.count()
        self.assertEqual(news_count, settings.NEWS_COUNT_ON_HOME_PAGE)

    def test_news_order(self):
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        all_dates = [news.date for news in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, sorted_dates)


class TestDetailPage(TestCase):
    """
    Set up the test data for the test case.

    This class method creates a new `News` object with the title 'Заголовок новости' and the text 'Просто текст.'.
    It then retrieves the URL for the detail page of the created news object using the `reverse` function.
    Next, it creates a new `User` object with the username 'Комментатор'.
    The method then iterates 10 times, creating a new `Comment` object for each iteration.
    The `news` attribute of the comment is set to the created news object.
    The `author` attribute of the comment is set to the created user object.
    The `text` attribute of the comment is set to 'Tекст {index}', where {index} is the current iteration index.
    The `created` attribute of the comment is set to the current time plus an incremental timedelta of days for each iteration.
    Finally, the comment object is saved to the database.

    Parameters:
        cls (type): The class object.

    Returns:
        None
    """
    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(
            title='Заголовок новости',
            text='Просто текст.',
        )
        cls.detail_url = reverse('news:detail', args=(cls.news.id,))
        cls.author = User.objects.create(username='Комментатор')
        now = timezone.now()
        for index in range(10):
            comment = Comment.objects.create(
                news=cls.news, author=cls.author, text=f'Tекст {index}',
            )
            comment.created = now + timedelta(days=index)
            comment.save()

    def test_comments_order(self):
        response = self.client.get(self.detail_url)
        self.assertIn('news', response.context)
        news = response.context['news']
        all_comments = news.comment_set.all()
        all_timestamps = [comment.created for comment in all_comments]
        sorted_timestamps = sorted(all_timestamps)
        self.assertEqual(all_timestamps, sorted_timestamps)

    def test_anonymous_client_has_no_form(self):
        response = self.client.get(self.detail_url)
        self.assertNotIn('form', response.context)

    def test_authorized_client_has_form(self):
        # Авторизуем клиент при помощи ранее созданного пользователя.
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        self.assertIn('form', response.context)
        # Проверим, что объект формы соответствует нужному классу формы.
        self.assertIsInstance(response.context['form'], CommentForm)