from django import forms

from reviews.models import Review, ReviewReport


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']


class ReviewReportForm(forms.ModelForm):
    class Meta:
        model = ReviewReport
        fields = ['reason']
        widgets = {
            'reason': forms.Select(choices=ReviewReport.REASON_TYPES),
        }