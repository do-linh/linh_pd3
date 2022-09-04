from django.db import models

from ..checkout.models import Checkout, Address
from ..order.models import Order
from urllib import parse

class PaypalToken(models.Model):
    token_type = models.CharField(
        'Token Type', max_length=255, help_text='Identifies the type of token returned. At this time, this field will always have the value Bearer', null=True, blank=True)
    access_token = models.CharField(
        'Access Token', max_length=2048, help_text='The token that must be used to access the Core APIs')
    refresh_token = models.CharField('Refresh Token', max_length=2048, null=True,
                                     blank=True, help_text='A token used when refreshing the access token')
    expires_in = models.IntegerField('Expires In', null=True, blank=True,
                                     help_text='The remaining lifetime of the access token in seconds. The value always returned is 3600 seconds (one hour). Use the refresh token to get a fresh one')
    refresh_token_expires_in = models.IntegerField(
        'Refresh Token Expires In', null=True, blank=True, help_text='The remaining lifetime, in seconds, for the connection, after which time the user must re-grant access.')
    scope = models.CharField(max_length=255, default='', null=True, blank=True)

    endpoint = models.CharField(
        max_length=255, default='', null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def still_valid(self):
        from datetime import  timedelta
        from django.utils.timezone import now
        return self.createdAt + timedelta(seconds=self.expires_in) >= now()

    class Meta:
        ordering = ['-createdAt']

class PaypalOrder(models.Model):
    paypal_order_id = models.CharField(max_length=50, primary_key=True)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    links = models.TextField(null=True)
    approve_url = models.CharField(max_length=500, null=True) 
    capture_url = models.CharField(max_length=500, null=True)
    token = models.CharField(max_length=50, null=True)

    def save(self, *arg, **kwargs) -> None:
        links = self.links
        if links :
            self.approve_url = [link['href'] for link in links if link['rel'] == 'approve'][0]
            self.capture_url = [link['href'] for link in links if link['rel'] == 'capture'][0]

            self.token = parse.parse_qs(parse.urlparse(self.approve_url).query)['token'][0]
        return super(PaypalOrder, self).save(*arg, **kwargs)

class Payment(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.SET_NULL,null=True, related_name='payments')
    order = models.ForeignKey(Order, on_delete= models.PROTECT, null=True, related_name='payments')
    paypal_order = models.ForeignKey(PaypalOrder, on_delete=models.SET_NULL, null=True, related_name='payments')
    status = models.CharField(max_length=20, null=True, blank=True)

    email = models.EmailField(null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    address_line_1 = models.CharField(max_length=255, null=True)
    admin_area_2= models.CharField(max_length=255, null=True)
    admin_area_1= models.CharField(max_length=255, null=True)
    postal_code= models.CharField(max_length=255, null=True)
    country_code= models.CharField(max_length=255, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_billing_address(self):
        address = Address(
            first_name = self.first_name,
            last_name = self.last_name,
            company_name = '',
            street_address_1 = self.address_line_1,
            city = self.admin_area_1,
            postal_code = self.postal_code,
        )
        address.save()
        return address
    class Meta:
        ordering = ("pk",)