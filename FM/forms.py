from django import forms
from The_Investor.models import InvestmentRequest
from FM.models import *
#######invvvvvreeeqqq#############
class InvForm(forms.ModelForm):
    class Meta:
        model = InvestmentRequest
        fields = ['payer_name','image']
        labels = {
            'payer_name': 'اسم المودع',
            'image': 'صورة الفاتورة/البيان',
        }
        
        widgets = {
            'payer_name': forms.TextInput(attrs={'required': True}),
            'image': forms.FileInput(attrs={'required': True}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(InvForm, self).__init__(*args, **kwargs)
        if user:
            self.initial['investor'] = user.investor.id
            self.fields['investor'].widget.attrs['readonly'] = True
            



#################proomoooreeeq####################


class PromoForm(forms.ModelForm):
    class Meta:
        model = PromoRequest
        fields = ['pay_name','image','promo_type']
        labels = {
            'pay_name': 'اسم المودع',
            'image': 'صورة الفاتورة/البيان',
            'promo_type': 'اختار نوع الباقة',
        }

        widgets = {
            'pay_name': forms.TextInput(attrs={'required': True}),
            'image': forms.FileInput(attrs={'required': True}),
            'promo_type': forms.Select(attrs={'required': True}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PromoForm, self).__init__(*args, **kwargs)
        if user:
            self.initial['owner'] = user.owner.id
            self.fields['owner'].widget.attrs['readonly'] = True