import stripe
from django.conf import settings

# Устанавливаем секретный ключ Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product_and_price(course):
    # Создание продукта в Stripe
    product = stripe.Product.create(name=course.title)

    # Создание цены для продукта
    price = stripe.Price.create(
        unit_amount=int(course.price * 100),  # цена в центах
        currency='usd',
        product=product.id,
    )

    return product, price
