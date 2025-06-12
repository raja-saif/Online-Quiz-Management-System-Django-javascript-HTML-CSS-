
# Register your models here.

from django.contrib import admin
from .models import Question, Answer, Quiz, QuizQuestion,Student

# Register modelsfrom .models import Question, Answer, Quiz, QuizQuestion

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 0
    readonly_fields = ('question_text', 'question_type')
    
    def question_text(self, obj):
        return obj.question.text
    question_text.short_description = 'Question'
    
    def question_type(self, obj):
        return obj.question.question_type
    question_type.short_description = 'Type'

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'total_marks', 'question_count', 'created_at')
    list_filter = ('instructor', 'created_at')
    search_fields = ('title', 'instructor__username')
    inlines = [QuizQuestionInline]
    readonly_fields = ('total_marks',)
    
    def question_count(self, obj):
        return obj.get_question_count()
    question_count.short_description = 'Number of Questions'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'subject', 'question_type')
    list_filter = ('subject', 'question_type')
    search_fields = ('text',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'correct_answer')
    search_fields = ('question__text', 'correct_answer')

admin.site.register(Student)

