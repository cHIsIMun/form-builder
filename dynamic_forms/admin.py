from django.contrib import admin
from .models import Step, Section, Field, Submission, AnswerText, AnswerNumber, AnswerDate, AnswerFile, AnswerBoolean
admin.site.register(Step)
admin.site.register(Section)
admin.site.register(Field)
admin.site.register(Submission)
admin.site.register(AnswerText)
admin.site.register(AnswerNumber)
admin.site.register(AnswerDate)
admin.site.register(AnswerFile)
admin.site.register(AnswerBoolean)
