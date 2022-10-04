from .forms import Sorting
from datetime import datetime
from .models import Category, Expense


def sort_by_field(queryset, sort_type: list[str], field: str):
    if sort_type[0] == str(Sorting.ASC) and len(sort_type) < 2:
        queryset = queryset.order_by(f"{field}")
    if sort_type[0] == str(Sorting.DSC) and len(sort_type) < 2:
        queryset = queryset.order_by(f"-{field}")
    return queryset


def search_by_name(queryset, name):
    if name:
        return queryset.filter(name__icontains=name)
    else:
        return queryset


def search_between_dates(queryset, date_from, date_to):
    if date_to and date_from:
        return queryset.filter(date__range=[date_from, date_to])
    else:
        return queryset


def search_from_date(queryset, date_from, date_to):
    if date_from and date_to is None:
        return queryset.filter(date__range=[date_from, datetime.today().date()])
    else:
        return queryset


def search_to_date(queryset, date_from, date_to):
    if date_to and date_from is None:
        return queryset.filter(date__lte=date_to)
    else:
        return queryset


def search_by_categories(queryset, categories):
    if categories:
        return queryset.filter(category__id__in=categories)
    else:
        return queryset


def sort_by_date(queryset, date_sorting):
    if date_sorting:
        return sort_by_field(queryset, date_sorting, 'date')
    else:
        return queryset


def sort_by_categories(queryset, categories_sorting):
    if categories_sorting:
        return sort_by_field(queryset, categories_sorting, 'category')
    else:
        return queryset


def count_expenses_per_category():
    categories = Category.objects.all().values_list()
    out = []
    if categories:
        for category in categories:
            out.append(Expense.objects.filter(category__id=category[0]).count())
    return out

