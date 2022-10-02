from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):

    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                           choices=Category.objects.all().values_list().order_by('id'), required=False)

    class Meta:
        model = Expense
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
