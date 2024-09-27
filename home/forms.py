from django import forms
from .models import Comment, CommentSectionModel, SeriesModel, Reply


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'name', 'email', 'phone']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-textarea w-full !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5', 'placeholder': 'دیدگاه شما '}),
            'name': forms.TextInput(attrs={'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5', 'placeholder': 'نام '}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5', 'placeholder': 'ایمیل '}),
            'phone': forms.TextInput(attrs={'class': 'form-input w-full h-11 !ring-0 !ring-offset-0 bg-secondary border-border focus:border-border rounded-xl text-sm text-foreground px-5', 'placeholder': 'شماره تلفن '}),
        }





class CommentSectionForm(forms.ModelForm):
    class Meta:
        model = CommentSectionModel
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-textarea w-full !ring-0 !ring-offset-0 bg-secondary border-0 focus:border-border border-border rounded-xl text-sm text-foreground p-5', 'placeholder': 'متن مورد نظر خود را وارد کنید'}),
        }









class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-textarea w-full !ring-0 !ring-offset-0 bg-secondary border-0 focus:border-border border-border rounded-xl text-sm text-foreground p-5',
                'placeholder': 'پاسخ خود را بنویسید...',
                'rows': 3,
            }),
        }

        labels = {
            'text': '',
        }


