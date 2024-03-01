from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.Quiz)
admin.site.register(models.Question)
admin.site.register(models.Comment)

class UserAnswerSubmitAdmin(admin.ModelAdmin):
    list_display=['id','question','user','right_ans']
admin.site.register(models.UserAnswerSubmit,UserAnswerSubmitAdmin)
class userQuizAttemptsAdmin(admin.ModelAdmin):
    list_display=['quiz','user','attemp_time']
admin.site.register(models.userQuizAttempts,userQuizAttemptsAdmin)
