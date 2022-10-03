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


def create_list_of_years(queryset):
    year_in_queryset = [i[0].year for i in queryset.values_list('date')]
    return [*set(year_in_queryset)]


def summary_per_year(queryset):
    year_in_queryset = create_list_of_years(queryset)
    amounts_per_year = {}
    for year in year_in_queryset:
        amounts_per_year[year] = queryset.filter(date__year__gte=year, date__year__lte=year).aggregate(Sum('amount'))[
            'amount__sum']
    return amounts_per_year


def summary_per_month(queryset):
    year_in_queryset = create_list_of_years(queryset)
    amount_per_each_month_in_year = {}
    for year in year_in_queryset:
        months_in_year = []
        for data_row in queryset.filter(date__year=year).values_list():
            months_in_year.append(data_row[4].month)
        months_in_year = [*set(months_in_year)]
        for month in months_in_year:
            amount_per_each_month_in_year[f'{year}-{calendar.month_name[month]}'] = \
                queryset.filter(date__year=year, date__month__gte=month, date__month__lte=month).aggregate(
                    Sum('amount'))['amount__sum']
    print(amount_per_each_month_in_year)
    return amount_per_each_month_in_year
