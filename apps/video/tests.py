from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Topics, Video

User = get_user_model()

class ModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем пользователя для тестов
        cls.user = User.objects.create(email='test@example.com', password='testpassword')

        # Создаем объект Topics для тестов
        cls.topic = Topics.objects.create(title='TestTopic')

        # Создаем объект Video для тестов
        cls.video = Video.objects.create(
            topics=cls.topic,
            videos='test_video.mp4',
            video_preview='test_preview.jpg',
            title='TestVideo',
            description='Test description',
            user=cls.user
        )

    def test_topic_creation(self):
        topic = Topics.objects.get(title='TestTopic')
        self.assertEqual(topic.title, 'TestTopic')
        self.assertEqual(topic.slug, 'testtopic')

    def test_video_creation(self):
        video = Video.objects.get(title='TestVideo')
        self.assertEqual(video.title, 'TestVideo')
        self.assertEqual(video.slug, 'testvideo')
        self.assertEqual(video.topics, self.topic)

    def test_video_description(self):
        video = Video.objects.get(title='TestVideo')
        self.assertEqual(video.get_description(), 'Test description')

    def test_str_methods(self):
        topic = Topics.objects.get(title='TestTopic')
        video = Video.objects.get(title='TestVideo')

        self.assertEqual(str(topic), 'TestTopic')
        self.assertEqual(str(video), 'TestVideo')
