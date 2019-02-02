from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="Home"),
    path('form/<int:id>', views.first_form, name="create_project"),
    path('show/<int:pro_id>', views.show_project, name="show_project")
]