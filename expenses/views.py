from datetime import datetime

from django.views.generic.list import ListView

from .forms import ExpenseSearchForm, Sorting
from .models import Expense, Category
from .reports import summary_per_category


def sort_query_if_possible(queryset, sort_type: list[str], field: str):
    if sort_type[0] == str(Sorting.ASC) and len(sort_type) < 2:
        queryset = queryset.order_by(f"{field}")
    if sort_type[0] == str(Sorting.DSC) and len(sort_type) < 2:
        queryset = queryset.order_by(f"-{field}")
    return queryset


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

            if name:
                queryset = queryset.filter(name__icontains=name)
            if date_from and date_to is None:
                queryset = queryset.filter(date__range=[date_from, datetime.today().date()])
            if date_to and date_from:
                queryset = queryset.filter(date__range=[date_from, date_to])
            if date_to and date_from is None:
                queryset = queryset.filter(date__lte=date_to)
            if categories:
                queryset = queryset.filter(category__id__in=categories)
            if date_sorting:
                queryset = sort_query_if_possible(queryset, date_sorting, 'date')
            if categories_sorting:
                queryset = sort_query_if_possible(queryset, categories_sorting, 'category')

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5
