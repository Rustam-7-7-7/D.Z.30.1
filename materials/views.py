from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModerator, IsOwner

from .paginators import StandardResultsSetPagination

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), ~IsModerator()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsModerator() | IsOwner()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Subscription, Course

class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Subscription removed'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Subscription added'

        return Response({"message": message})


from django.http import JsonResponse
from django.views import View
from .models import Course
from .utils import create_stripe_product_and_price
import stripe


from rest_framework.views import APIView
from rest_framework.response import Response

class CreateCheckoutSessionView(APIView):
    def post(self, request, course_id):
        try:
            # Получаем курс по его ID
            course = Course.objects.get(id=course_id)

            # Создаем продукт и цену в Stripe
            product = stripe.Product.create(name=course.title)
            price = stripe.Price.create(
                unit_amount=int(course.price * 100),  # цена в центах
                currency='usd',
                product=product.id,
            )

            # Создаем сессию Stripe Checkout
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price.id,
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8000/success/',
                cancel_url='https://yourdomain.com/cancel/',
            )

            # Возвращаем sessionId и URL сессии
            return JsonResponse({
                'sessionId': checkout_session.id,
                'url': checkout_session.url
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return Response({'status': 'success'})
