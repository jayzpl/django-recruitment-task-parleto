from django.views.generic.list import ListView
from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, calculate_total_amount, summary_per_year, summary_per_month
from .searching import generate_search_result


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        total_amount = 0
        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            date_from = form.cleaned_data.get('date_from', '')
            date_to = form.cleaned_data.get('date_to', '')
            categories = form.cleaned_data.get('categories', )
            date_sorting = form.cleaned_data.get('date_sorting')
            categories_sorting = form.cleaned_data.get('categories_sorting')

            queryset = generate_search_result(queryset, name, date_from, date_to, categories, date_sorting,
                                              categories_sorting)

            total_amount = calculate_total_amount(queryset)
            summary_year = summary_per_year(queryset)
            summary_month = summary_per_month(queryset)


        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            total_amount=total_amount,
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5
