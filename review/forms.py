from django import forms
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ('title', 'description', 'image')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ('headline', 'rating', 'body')
        widgets = {
            'rating': forms.RadioSelect(choices=[
                (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')
            ], attrs={ 'class': 'star-rating'}),
        }
