from django.contrib import admin

# Register your models here.
from .models import Organization, Events, session, samQuestion, samAnswer, evaluation_Event
admin.site.register(Organization)
admin.site.register(Events)
admin.site.register(session)
admin.site.register(evaluation_Event)


class ChoiceInline(admin.TabularInline):
    model = samAnswer
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields':['session','question_text']}),
            # ('Answers', {'fields': ['pub_date'], 'classes':['collapse']}),
                ]
    inlines = [ChoiceInline]

admin.site.register(samQuestion, QuestionAdmin)