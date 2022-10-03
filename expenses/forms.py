from django import forms
from .models import Expense, Category
from enum import Enum


class Sorting(Enum):
    ASC = 'Ascending'
    DSC = 'Descending'


def create_choices(input_list):
    input_list = [*set(input_list)]
    choices = [(0, None)]
    for i, value in enumerate(input_list):
        choice = (i+1, value)
        choices.append(choice)
    return choices


class ExpenseSearchForm(forms.ModelForm):
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    date_sorting = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             choices=((Sorting.ASC, Sorting.ASC.value),
                                                      (Sorting.DSC, Sorting.DSC.value)), required=False)
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                           choices=Category.objects.all().values_list().order_by('id'), required=False)
    categories_sorting = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                   choices=((Sorting.ASC, Sorting.ASC.value),
                                                            (Sorting.DSC, Sorting.DSC.value)), required=False)
    #years = [date[0].year for date in Expense.objects.values_list('date')]
    #months = [date[0].month for date in Expense.objects.values_list('date')]
    #summary_per_year = forms.ChoiceField(choices=create_choices(years), required=False)
    #summary_per_month = forms.ChoiceField(choices=create_choices(months), required=False)

    class Meta:
        model = Expense
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
