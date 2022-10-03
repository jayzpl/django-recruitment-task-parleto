from .forms import Sorting
from datetime import datetime
from .models import Expense


def sort_if_possible_by_field(queryset, sort_type: list[str], field: str):
    if sort_type[0] == str(Sorting.ASC) and len(sort_type) < 2:
        queryset = queryset.order_by(f"{field}")
    if sort_type[0] == str(Sorting.DSC) and len(sort_type) < 2:
        queryset = queryset.order_by(f"-{field}")
    return queryset


def generate_search_result(queryset, name, date_from, date_to, categories, date_sorting, categories_sorting):
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
        queryset = sort_if_possible_by_field(queryset, date_sorting, 'date')
    if categories_sorting:
        queryset = sort_if_possible_by_field(queryset, categories_sorting, 'category')
    return queryset
