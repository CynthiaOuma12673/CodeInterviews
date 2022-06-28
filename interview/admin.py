from django.contrib import admin
from .models import Question,Profile

# Register your models here.
admin.site.register(Profile),
admin.site.register(Question),