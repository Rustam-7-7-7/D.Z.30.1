from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreate, LessonRetrieveUpdateDestroy, SubscriptionView


from .views import CreateCheckoutSessionView


router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreate.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroy.as_view(), name='lesson-detail'),
    path('subscribe/', SubscriptionView.as_view(), name='subscription'),
    path('create-checkout-session/<int:course_id>/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
]
