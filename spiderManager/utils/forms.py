# -*- coding: utf-8 -*-
from django import forms
from accounts.models import Acounts

class AccountForm(forms.ModelForm):
    class Meta:
        model = Acounts
        fields = [
            'phone',
            'password',
            'website'
        ]
