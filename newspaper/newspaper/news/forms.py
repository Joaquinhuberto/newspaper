# -*- coding: utf-8 -*-

from django import forms

from newspaper.news.models import News


class NewsForm(forms.ModelForm):

    def clean_title(self):
        if 'b' in self.cleaned_data['title']:
            raise forms.ValidationError("El campo titulo no puede contener B <Esto es una validación chorra>")
        return self.cleaned_data['title']

    class Meta:
        model = News
        fields = '__all__'
