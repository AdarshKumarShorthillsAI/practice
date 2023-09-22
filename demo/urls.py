from django.urls import path
from .views import register_user, user_login,add_new_entry,fetch_all_usernames,update_table,empty_the_table,retrieve_table

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('add_new_entry/', add_new_entry, name='add_new_entry'),
    path('fetch/',fetch_all_usernames,name="fetch"),
    path('update/',update_table,name="update"),
    path('delete/',empty_the_table,name="delete"),
    path('retrieve/',retrieve_table,name="retrieve"),
]