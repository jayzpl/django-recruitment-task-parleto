from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
import calendar


def calculate_total_amount(queryset):
    return queryset.aggregate(Sum('amount'))['amount__sum']


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
            .annotate(category_name=Coalesce('category__name', Value('-')))
            .order_by()
            .values('category_name')
            .annotate(s=Sum('amount'))
            .values_list('category_name', 's')
    ))


def summary_per_year(queryset):
    year_in_queryset = [i[0].year for i in queryset.values_list('date')]
    year_in_queryset = [*set(year_in_queryset)]
    amounts_per_year = {}
    for year in year_in_queryset:
        amounts_per_year[year] = queryset.filter(date__year__gte=year, date__year__lte=year).aggregate(Sum('amount'))['amount__sum']
    return amounts_per_year


def summary_per_month(queryset):
    # add filter using year and month
    months_in_queryset = [i[0] for i in queryset.values_list('date').order_by()]
    print(months_in_queryset)
    print([*set(months_in_queryset)])
    """
    months_in_queryset = [*set(months_in_queryset)]
    amounts_per_month = {}
    for month in months_in_queryset:
        _temp = queryset.filter(date__month__gte=month, date__month__lte=month).aggregate(Sum('amount'))[
            'amount__sum']
        month = calendar.month_name[month]
        amounts_per_month[month] = _temp
    return amounts_per_month
    """
    return queryset