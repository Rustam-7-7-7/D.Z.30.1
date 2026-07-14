from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} subscribed to {self.course.title}"
