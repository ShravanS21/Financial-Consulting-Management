"""A1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from A1App.views import *
from django.conf import settings
from django.conf.urls.static import static
from A1App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    #public urls
    path('public/', publicview),
    path('member_register/', member_registerview),
    path('userlogin/', userloginview, name='userloginview'),
    path('events/', events_view),
    path('generalfeedback/', generalfeedbackview),
    path('user_registration/', member_registerview),
    path('document/', documentview),
    path('public_eventregister/', public_eventregisterview),
    path('events/upcoming/', views.events_upcoming, name='events_upcoming'),
    path('events/completed/', views.events_completed, name='events_completed'),
    path('event_feedback/', event_feedback_view),
    path('members_trainings/', members_trainingsview),
    path('public_videogallery/', public_videogalleryview),
    path('public_trainings/', public_trainingsview),


    


    # path('mainuserlogin/', mainuserview),
    path('adminloginpage/', adminloginpageview),
    path('adminlogin/', adminloginview),
    path('adminhome/', adminhomeview),
    path('adminUpcomingevents/', adminUpcomingeventsviews),
    path('adminCompletedevents/', adminCompletedeventsviews),
    path('adminaddevents/', adminaddeventsview),
    path('adminaddtrainings/', adminaddtrainingsview),
    path('admin_view_trainings/', view_trainingsview),
    path('admin_edit_training/<int:id>/', edit_training_view, name='edit_training'),
    path('adminview_public_eventregister/', adminview_public_eventregisterview),
    path('adminview_members_eventregister/', adminview_members_eventregisterview),
    path('edit_event/<int:event_id>/', views.admin_edit_event, name='admin_edit_event'),
    path('end_event/<int:event_id>/', views.end_event, name='end_event'),
    path('event_feedback/', event_feedbackview),
    path('admin_viewpayment/', admin_view_paymentview),


    path('save_event/', save_event),
    path('adminaddblogs/', adminaddblogsview),
    path('save_document/', save_documentview),
    path('adminflashnews/', adminflashnewsview),
    path('uploadvideo/', uploadvideoview),
    path('view_videos/', views.view_videos, name='view_videos'),
    path('edit_video/<int:video_id>/', views.edit_video, name='edit_video'),
    path('inactivebtn/',inactivebtnview),
    path('activebtn/',activebtnview),
    path('eventregister/',eventregisterview),
    path('approveuser/', approveuserview),
    path('viewfeedback/',viewfeedbackview),
    path('adminadd_blogs/', adminadd_blogsview),
    path('admin_view_blogs/', view_blogs, name='viewblogs'),
    path('edit_blog/<int:blog_id>/', edit_blog_view, name='editblog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('like_blog/<int:blog_id>/', views.like_blog, name='like_blog'),

    #members ulrs
    path('memberhome/', memberhomeview),
    path('members_videogallery/', members_videogalleryview),
    path('members_blogs/', members_blogsviews),
    path('members_editprofile/', edit_profile),
    path('change_password/', views.change_password, name='change_password'),
    path('members_events/', views.members_events_view, name='members_events'), 
    path('members_eventregister/', views.members_eventregister_view, name='members_eventregister'),
    path('events/membersupcoming/', views.members_eventsupcoming, name='members_eventsupcoming'),
    path('events/memberscompleted/', views.members_eventscompleted, name='members_eventscompleted'),
    path('event_feedback/', event_feedback_view),
    path('members_event_feedback/', members_event_feedbackview),
    path('members_generalfeedback/', members_generalfeedbackview),
    path('trainingspayment_page/', trainingspayment_pageview),
    path('payment_page/', payment_pageview),

    

    

    # path('admin_chat/', admin_chat_view, name='admin_chat_view'),
    # path('member_chat/', member_chat_view, name='member_chat_view'),
    # path('send_message/', send_message, name='send_message'),

  
    
    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
