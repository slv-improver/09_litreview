from django import forms
from authentication import models as auth_models
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

class DeletePostForm(forms.Form):
    delete = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = auth_models.UserFollows
        fields = ['followed_user']
        widgets = {
            'followed_user': forms.TextInput()
        }
        labels = {
            'followed_user': ''
        }

    # def clean(self):
    #     cleaned_data = super(FollowUsersForm, self).clean()
    #     followed_user = auth_models.User.objects.get(
    #         username=self.data['followed_user']
    #     )
    #     cleaned_data['followed_user'] = followed_user
    #     return cleaned_data

# class FollowForm(forms.Form):
#     followed_user = forms.CharField(label='', max_length=100)
