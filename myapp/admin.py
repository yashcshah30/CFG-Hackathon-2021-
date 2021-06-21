from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Mentor)
admin.site.register(Phase)
admin.site.register(Question)
admin.site.register(Document)