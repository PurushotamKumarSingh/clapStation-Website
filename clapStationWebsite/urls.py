from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.starting_page, name='starting-page'),
    path('postdelete/<int:id>',views.postdelete,name='postdelete'),
    path('postedit/<int:id>',views.postedit,name='postedit'),
    path('postupdate/<str:id>',views.postupdate,name='postupdate'),
    path('Addcomment/<int:post_id>/', views.Addcomment, name='Addcomment'),
    path('like/',views.like_post,name='like-post'),
    path('Tutor_view/', views.Tutor_view, name='Tutor_view'),
    path('TutorContact/<int:id>', views.TutorContact, name='TutorContact'),

    path('groups/', views.groups_page, name='groups'),
    path('groupdelete/<int:id>',views.groupdelete,name='groupdelete'),
    path('groupedit/<int:id>',views.groupedit,name='groupedit'),
    path('groupupdate/<str:id>',views.groupupdate,name='groupupdate'),
    
    path('bands/', views.bands_page, name='bands'),
    path('bandsdelete/<int:id>',views.bandsdelete,name='bandsdelete'),
    path('bandsedit/<int:id>',views.bandsedit,name='bandsedit'),
    path('bandsupdate/<str:id>',views.bandsupdate,name='bandsupdate'),
    path('bandbooking/<int:id>',views.bandbooking,name='bandbooking'),
    
    path('academies/', views.academies_page, name='academies'),
    path('academy_detail/<int:id>/',views.academy_detail, name='academy_detail'),


    path('events/', views.events_page, name='events'),
    path('eventsdata/<int:id>', views.eventsdata, name='eventsdata'),
    path('addEvents/', views.add_event, name='add_event'),
    path('deleteEvent/<int:id>', views.delete_event, name='delete_event'),
    path('eventsedit/<int:id>',views.eventsedit,name='eventsedit'),
    path('eventsupdate/<str:id>',views.eventsupdate,name='eventsupdate'),
    path('eventbooking/<int:id>', views.eventbooking, name='booking'),

    path('artists/', views.artists_page, name='artists'),
    path('artist-profile/<int:pk>', views.artist_profile, name='artistProfile'),
    
    path('about/', views.about_page, name='about'),
    
    path('contact/', views.contact_page, name='contact'),


    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    
    path('profile/', views.profile_page, name='profile'),
    path('delete_video/<int:id>', views.deleteVideo, name='delete-video'),
    path('delete_photo/<int:id>', views.deletePhoto, name='delete-photo'),
    path('edit_profile/<int:id>', views.edit_profile, name='editProfile'),
    path('jammingstation/', views.jammingstation_page, name='jammingstation'),
    
    
    
    
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()