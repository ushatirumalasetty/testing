from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Reaction)
# Register your models here.
