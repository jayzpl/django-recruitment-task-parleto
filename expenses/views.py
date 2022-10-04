from django.views.generic.list import ListView
from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, calculate_total_amount, summary_per_year, summary_per_month
from .searching import *


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            date_from = form.cleaned_data.get('date_from', '')
            date_to = form.cleaned_data.get('date_to', '')
            categories = form.cleaned_data.get('categories', )
            date_sorting = form.cleaned_data.get('date_sorting')
            categories_sorting = form.cleaned_data.get('categories_sorting')

            queryset = search_by_name(queryset, name)
            queryset = search_between_dates(queryset, date_from, date_to)
            queryset = search_from_date(queryset, date_from, date_to)
            queryset = search_to_date(queryset, date_from, date_to)
            queryset = search_by_categories(queryset, categories)
            queryset = sort_by_date(queryset, date_sorting)
            queryset = sort_by_categories(queryset, categories_sorting)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_per_year=summary_per_year(queryset),
            summary_per_month=summary_per_month(queryset),
            total_amount=calculate_total_amount(queryset),
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        expenses_per_category = count_expenses_per_category()
        expenses_per_category = list(zip(self.object_list, expenses_per_category))

        return super().get_context_data(
            object_list=expenses_per_category,
            **kwargs)


