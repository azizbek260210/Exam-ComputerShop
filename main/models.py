from decimal import Decimal
from django.db import models
import qrcode
from django.core.files import File
from io import BytesIO

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.FileField(upload_to='media/products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(blank=True, upload_to="media/qr_codes")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        url = (
            f'Maxsulot nomi: {self.name}\n'
            f'Maxsulot haqida: {self.description}\n'
            f'Maxsulot narxi: {self.price}\n'
            f'Maxsulot miqdori: {self.quantity}\n'
            f'Maxsulot yaratilingan vaqt: {self.created_at}'
        )
        qr_image = qrcode.make(url, box_size=15)
        qr_image_pil = qr_image.get_image()
        stream = BytesIO()
        qr_image_pil.save(stream, format='PNG')
        self.qr_code.save(
            f"{self.name}_{self.quantity}.png", File(stream), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class EnterProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    entered_at = models.DateField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.price = Decimal(self.quantity) * self.product.price
        super().save(*args, **kwargs)
        self.product.quantity += self.quantity
        self.product.save()

    def __str__(self):
        return f"{self.product.name}-{self.quantity}-{self.entered_at}"

    class Meta:
        ordering = ['-entered_at']

class SellProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sold_at = models.DateField(auto_now_add=True)
    refunded = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.price = Decimal(self.quantity) * self.product.price
        super().save(*args, **kwargs)
        self.product.quantity -= self.quantity
        self.product.save()

    @property
    def refund(self):
        if not self.refunded:
            refund_amount = self.price
            Refund.objects.create(sell_product=self)
            self.refunded = True
            self.save()
            return refund_amount
        return 0

    def __str__(self):
        if self.refunded:
            return f"{self.product.name} - {self.sold_at}"
        return f"{self.product.name} - {self.sold_at}"

    class Meta:
        ordering = ['-sold_at']

class Refund(models.Model):
    sell_product = models.OneToOneField(SellProduct, on_delete=models.CASCADE)
    refunded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sell_product} - {self.refunded_at}"

    @property
    def price(self):
        return self.sell_product.price

    class Meta:
        ordering = ['-refunded_at']
