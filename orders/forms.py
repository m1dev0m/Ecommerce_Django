from django import forms

class OrderForm(forms.Form):
    shipping_address = forms.CharField(label="Shipping Address", max_length=255)
    contact_number = forms.CharField(label="Contact Number", max_length=15)



class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=16, label="Номер карты")
    cvv = forms.CharField(max_length=3, min_length=3, label="CVV")
    expiration_date = forms.CharField(max_length=5, label="Срок действия (MM/YY)")
