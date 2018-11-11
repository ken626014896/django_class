from django.contrib import admin

# Register your models here.
from polls.models import Question,Choice
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], }),
    ]

    list_display = ['question_text','pub_date','was_published_recently' ]
    #过滤
    list_filter = ['pub_date']
    #查询
    search_fields = ['question_text']
    inlines = [ChoiceInline]
admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)
