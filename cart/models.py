from django.db import models

from account.models import User
from home.models import SeriesModel
from django.apps import AppConfig

class DiscountCode(models.Model):
    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کد های تخفیف"

    name = models.CharField(max_length=10, unique=True, verbose_name="نام")
    percentage = models.SmallIntegerField(default=0, verbose_name="درصد")
    quantity = models.SmallIntegerField(default=1, verbose_name="تعداد")

    def __str__(self):
        return self.name


class UserDiscountCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'discount_code')













class Order(models.Model):
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name='کاربر')
    total_price = models.IntegerField(default=0, verbose_name='مبلغ کل')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده')

    def __str__(self):
        return f"سفارش {self.id} برای {self.user.fullname}"


class OrderItem(models.Model):
    class Meta:
        verbose_name = "اقلام سفارش"
        verbose_name_plural = "اقلام سفارش ها"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="سفارش")
    product = models.ForeignKey(SeriesModel, on_delete=models.CASCADE, related_name="order_items", verbose_name="محصول")
    price = models.PositiveIntegerField(verbose_name="قیمت")

    def __str__(self):
        return f"اقلام سفارش {self.order.id} برای {self.product.title}"





