from django.contrib import admin
from .models import *

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Donation)
admin.site.register(Rate)
admin.site.register(Comment)
admin.site.register(ReportComment)
admin.site.register(ReportProject)
admin.site.register(Tag)
admin.site.register(Picture)
admin.site.register(FeatureProject)

