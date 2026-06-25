from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Course, Lesson
from django.contrib.auth.models import User

class CourseLessonTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test Course', owner=self.user)

    def test_create_lesson(self):
        response = self.client.post(reverse('lesson-list-create'), {
            'course': self.course.id,
            'title': 'New Lesson',
            'description': 'This is a test lesson.',  # Добавлено описание
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        })
        print(response.data)  # Выводим детали ошибки
        self.assertEqual(response.status_code, 201)

    def test_subscription(self):
        response = self.client.post(reverse('subscription'), {'course_id': self.course.id})
        self.assertEqual(response.data['message'], 'Subscription added')
        response = self.client.post(reverse('subscription'), {'course_id': self.course.id})
        self.assertEqual(response.data['message'], 'Subscription removed')
