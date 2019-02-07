from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Home"),
    path('form/', views.first_form, name="create_project"),
    path('show/<int:pro_id>', views.show_project, name="show_project"),
    path('report/pro/<int:pro_id>', views.add_report, name="report"),
    path('report/comment/<int:com_id>', views.add_report_comment, name="report_comment"),
    path('categories/<int:cat_id>', views.categories, name='category'),
]