from django.contrib import admin
from .models import Expense, Category

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount','description','owner','date','category')
    search_fields = ('description', 'date', 'category')
    list_per_page = 2

admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Category)
