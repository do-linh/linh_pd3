from rest_framework import serializers
from .models import Checkout, CheckoutLine
from ..order.models import Address
from ..warehouse.availabiltity import check_stock_quantity, InsufficientStock
from rest_framework.exceptions import ValidationError

def check_lines_quantity(books, quantities):
    for book,quantity in zip(books, quantities):
        try:
            check_stock_quantity(book,quantity)
        except InsufficientStock as e:
            msg = f"Could not add item {book.pk}-{book.namebook}. Out of stock"
            raise ValidationError({"quantity": ValidationError(msg,code=e.get_codes())})

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class CheckoutLineSerializer(serializers.ModelSerializer):
    class Meta:
        
        fields = ["book", "quantity"]
        model = CheckoutLine



class ReadCheckoutSerializer(serializers.ModelSerializer):
    billing_address = AddressSerializer(read_only=True)
    shipping_address = AddressSerializer(read_only=True)
    lines = CheckoutLineSerializer(many=True)
    class Meta:
        model = Checkout
        fields = "__all__"

class WriteCheckoutSerializer(serializers.ModelSerializer):
    billing_address = AddressSerializer(write_only=True)
    shipping_address = AddressSerializer(write_only=True)

    lines = CheckoutLineSerializer(many=True)
    class Meta:
        fields = ['email', 'billing_address','shipping_address', "lines"]
        model = Checkout
    def create(self, validated_data):
        user = self.request.user
        lines = validated_data.pop('lines')
        books = [line.get('book') for line in lines]
        quantities = [line.get('quantity') for line in lines]

        check_lines_quantity(books,quantities)
        checkout, created = Checkout.objects.get_or_create(user=user)
        checkout.email = validated_data.get('email')
        self.save_addresses(checkout)
        
        if created:
            for checkout_line in lines :
                CheckoutLine.objects.create(checkout=checkout, **checkout_line)

        return checkout
    def perform_update(self, instance):
        lines = self.validated_data.pop("lines")
        books = [line.get('book') for line in lines]
        quantities = [line.get('quantity') for line in lines]

        check_lines_quantity(books,quantities)
        for checkout_line in lines :
            pass
            # CheckoutLine.objects.create(checkout=checkout, **checkout_line)
        return  
    def save_addresses(self, instance: "Checkout"):
        
        billing_address, _ = Address.objects.get_or_create(**self.request.data.get("billing_address"))
        shipping_address, _ =Address.objects.get_or_create(**self.request.data.get("shipping_address"))

        update_fields = []
        if billing_address :
            billing_address.save()
            instance.billing_address = billing_address
            update_fields.append("billing_address")
        if shipping_address :
            shipping_address.save()
            instance.shipping_address= shipping_address
            update_fields.append("shipping_address")
        instance.save(update_fields=update_fields)

         
