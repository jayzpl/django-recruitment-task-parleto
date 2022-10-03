from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


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
    print(queryset)
    print(queryset
          .values_list('date')
          )


def summary_per_month(queryset):
    pass
