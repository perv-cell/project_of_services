#добавленный файл
from django.urls import path
from .views import MainView, PostDetailView, SignUp, Authorize,Contact,SuccessView,SearchView,TagView
from django.contrib.auth.views import LogoutView
#from blog.blog import settings
urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('blog/<slug>/',PostDetailView.as_view(),name='post'),
    path('signup/',SignUp.as_view(),name='signup'),
    path('authorize/',Authorize.as_view(),name='auth'),
                                                #settings.LOGOUT_REDIRECT_URL
    path('signout/',LogoutView.as_view(), {'next_page': '/'}, name='signout'),
    path('contacts/',Contact.as_view(), name='contact'),
    path('contacts/success/', SuccessView.as_view(), name='success'),
    path('search/',SearchView.as_view(),name='search_results'),
    path('tag/<slug:slug>',TagView.as_view(),name='tag')
]