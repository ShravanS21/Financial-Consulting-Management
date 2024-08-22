from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from A1App.models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout
from django.http import JsonResponse
from django.http import HttpResponseBadRequest, HttpResponse
from datetime import datetime
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
    
#All Public views appear here
def publicview(request):
    flash_news = FlashNews.objects.order_by('-created_at').first()
    return render(request, 'public.html', {'flash_news': flash_news})

def member_registerview(request):
    return render(request, 'register.html')

def userloginview(request):
    if request.method == "POST":
        email = request.POST.get('user_email')
        password = request.POST.get('password')

        try:
            user = Member.objects.get(email=email)
            if user.password == password:
                if user.is_active:
                    # Login successful
                    request.session['user_id'] = user.id  # Store user's ID in session
                    request.session['user_name'] = user.username
                    request.session['user_email'] = user.email
                    messages.success(request, 'Logged in successfully.')
                    return redirect('/memberhome/', {'popup_message': 'Logged in successfully.'})
                else:
                    # User is not active
                    messages.error(request, 'User not active. Please contact support.')
                    return render(request, 'userlogin.html', {'error_message': 'User not active. Please contact support.'})
            else:
                # Incorrect password
                messages.error(request, 'Invalid email or password.')
                return render(request, 'userlogin.html', {'error_message': 'Invalid email or password.'})
        except Member.DoesNotExist:
            # Email not found
            messages.error(request, 'Invalid email or password.')
            return render(request, 'userlogin.html', {'error_message': 'Invalid email or password.'})
    else:
        return render(request, 'userlogin.html')

    

def eventsview(request):
    return render(request, 'events.html')

def generalfeedbackview(request):
    if request.method == 'POST':
        gfeedback_username = request.POST.get('gfeedback_username')
        gfeedback_email = request.POST.get('gfeedback_email')
        gfeedback_contactno = request.POST.get('gfeedback_contactno')
        gfeedback_eventname = request.POST.get('gfeedback_eventname')
        gfeedback = request.POST.get('gfeedback')

        feedback = Feedback(gfeedback_username=gfeedback_username, gfeedback_email=gfeedback_email, gfeedback_contactno=gfeedback_contactno, gfeedback_eventname=gfeedback_eventname, gfeedback=gfeedback)
        feedback.save()  
        return render(request, 'generalfeedback.html', {'popup_message': 'Form Submitted successfully.'})
    return render(request, 'generalfeedback.html')

@csrf_exempt
def member_registerview(request):
    if request.method == 'POST':
        username = request.POST['username']
        age = request.POST['age']
        gender = request.POST['member_gender']
        contactno = request.POST['contactno']
        email = request.POST['email']
        password = request.POST['password']

        # Handle file upload
        profile_picture = request.FILES.get('profile_picture')

        # Save the member data
        member = Member(
            username=username,
            age=age,
            gender=gender,
            contactno=contactno,
            email=email,
            is_active=False,
            password=password, 
            profile_picture=profile_picture  # Save the uploaded profile picture
        )
        member.save()

        
        return redirect('/member_register/', {'popup_message': 'Form Submitted successfully.'})

    return render(request, 'register.html')


        
def eventregisterview(request):
    return render(request, 'events.html')  

def blog_detail(request, pk):
    blog = get_object_or_404(Blogs, pk=pk)
    print(blog)
    return render(request, 'blog_detail.html', {'blog': blog})     

def public_eventregisterview(request):
    if request.method == "POST":
        public_eventusername = request.POST.get('public_eventusername')
        public_eventage = request.POST.get('public_eventage')
        public_eventcontactno = request.POST.get('public_eventcontactno')
        public_eventgender = request.POST.get('public_eventgender')
        public_eventemail = request.POST.get('public_eventemail')
        public_eventname = request.POST.get('public_eventname')

        # Assuming you want to fetch the event from the event table
        event = get_object_or_404(Event, event_name=public_eventname)
        
        # Register the event
        public_events_register = public_eventsregister(
            public_eventusername=public_eventusername, 
            public_eventage=public_eventage, 
            public_eventcontactno=public_eventcontactno, 
            public_eventgender=public_eventgender,
            public_eventemail=public_eventemail,
            public_eventname=public_eventname
        )
        public_events_register.save()
        return render(request, 'public_eventregister.html', {'popup_message': 'Form Submitted successfully.', 'event_name': event.event_name})
    
    # For GET requests, pass the event name to the template
    # Here, you should provide the logic to select the correct event or handle this as needed
    event = Event.objects.first()  # Example: get the first event; adjust as needed
    return render(request, 'public_eventregister.html', {'event_name': event.event_name})


def events_upcoming(request):
    now = timezone.now()  # Use timezone-aware datetime
    events = Event.objects.filter(event_date__gte=now, event_status='Upcoming')  # Filter events by future dates
    return render(request, 'events_upcoming.html', {'events': events})


def events_completed(request):
    completed_events = Event.objects.filter(event_status='Completed')  # Filter completed events
    return render(request, 'events_completed.html', {'events': completed_events})


def event_feedback_view(request, event_name):
    event = Event.objects.get(event_name=event_name)
    
    if request.method == 'POST':
        contact_no = request.POST.get('contact_no')
        user_name = request.POST.get('user_name')
        feedback = request.POST.get('event_feedback')
        
        EventFeedback.objects.create(event=event, contact_no=contact_no, user_name=user_name, feedback=feedback)
        messages.success(request, 'Thank you for your feedback!')
        return redirect('/events/completed/')
    
    return render(request, 'events_completed.html', {'event_name': event_name})

def public_videogalleryview(request):
    videos = Video.objects.all()
    return render(request, 'videogallery.html', {'videos': videos})  

def public_trainingsview(request):
    trainings = Training.objects.all()
    return render(request, 'public_training.html', {'trainings': trainings})

# ------------------------------------------------------------------------------------------------------------------

#All Admin Views appear here
def adminloginpageview(request):
    return render(request, 'adminlogin.html')

def adminloginview(request):
    admin_name = request.POST.get("admin_name")
    adminpassword = request.POST.get("adminpassword")
    if admin_name == "admin" and adminpassword == "123456":
        request.session['admin_name'] = admin_name
        request.session['is_admin'] = True
        return redirect('/adminhome/')
    else:
        messages.error(request, 'Invalid admin credentials.')
        return render(request, 'adminlogin.html', {'error_message': 'Invalid admin credentials.'}) 
    
    
def adminhomeview(request):
    total_members = Member.objects.count()
    total_blogs = Blogs.objects.count()
    total_events = Event.objects.count()
    total_trainings = Training.objects.count()

    now = timezone.now()

    # Get ongoing events: Events that are happening today and are still upcoming
    ongoing_events = Event.objects.filter(
        event_date=now.date(),
        event_time__gte=now.time(),
        event_status='Upcoming'
    ).order_by('event_time')

    # Get all blogs
    blogs = Blogs.objects.order_by('-blog_date')

    # Get the number of events per month for the current year
    events_per_month = (
        Event.objects
        .filter(event_date__year=now.year)
        .annotate(month=TruncMonth('event_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    months = []
    counts = []
    for event in events_per_month:
        months.append(event['month'].strftime('%B'))  # Get the month name
        counts.append(event['count'])

    # Get events from the previous year
    last_year = now.year - 1
    previous_year_events = Event.objects.filter(event_date__year=last_year)

    context = {
        'total_members': total_members,
        'total_blogs': total_blogs,
        'total_events': total_events,
        'total_trainings': total_trainings,
        'months': months,
        'counts': counts,
        'previous_year_events': previous_year_events,
        'ongoing_events': ongoing_events,
        'blogs': blogs,
    }

    return render(request, 'Admin/adminhome.html', context)


def approveuserview(request):
    users = Member.objects.all()  # Fetch all user registrations
    return render(request, 'Admin/adminapprovemembers.html', {'registers': users})


def inactivebtnview(request):
    userid=request.GET["userid"]
    Member.objects.filter(id=userid).update(is_active=0)
    userlist=Member.objects.all()
    return render(request,'Admin/adminapprovemembers.html',{'registers':userlist})

def activebtnview(request):
    userid=request.GET["userid"]
    Member.objects.filter(id=userid).update(is_active=1)
    userlist=Member.objects.all()
    return render(request,'Admin/adminapprovemembers.html',{'registers':userlist})

def adminaddeventsview(request):
    return render(request, 'Admin/adminaddevents.html')

def save_event(request):
    if request.method == "POST":
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        event_details = request.POST.get('event_details')
        meeting_link = request.POST.get('meeting_link')
        event_image = request.FILES.get('event_image')
        by = request.POST.get('by')

        # Basic validation
        if not all([event_name, event_date, event_time, event_details, meeting_link, by]):
            messages.error(request, 'All fields are required.')
            return redirect('/admin/add_event/')  # Redirect back to the form

        # Save the event details to the database
        event = Event(
            event_name=event_name,
            event_date=event_date,
            event_time=event_time,
            event_details=event_details,
            meeting_link=meeting_link,
            event_image=event_image,
            by=by
        )
        event.save()
        return render(request, 'Admin/adminaddevents.html', {'popup_message': 'Form Submitted successfully.'})
    return render(request, 'Admin/adminaddevents.html')

def events_view(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'events.html', context)  

def adminflashnewsview(request):
    popup_message = None
    
    if request.method == 'POST':
        flash_news = request.POST.get('admin_flash')
        if flash_news:
            # Save the flash news to the database
            FlashNews.objects.create(admin_flash=flash_news)
            popup_message = 'Form Submitted successfully.'

    # Fetch all flash news from the database
    flashnews = FlashNews.objects.all().order_by('-created_at')

    return render(request, 'Admin/adminflashnews.html', {'flashnews': flashnews, 'popup_message': popup_message})  # You might want to order by date

    

def viewfeedbackview(request):
    viewfeed = Feedback.objects.all()
    return render(request, 'Admin/adminviewfeedback.html', {'feeds':viewfeed})

def adminadd_blogsview(request):
    if request.method == "POST":
        blog_date = request.POST.get('blog_date')
        blog_title = request.POST.get('blog_title')
        blog_authorName = request.POST.get('blog_authorName')
        blog_authorRole = request.POST.get('blog_authorRole')
        blog_author_image = request.FILES.get('blog_author_image')
        blog_information = request.POST.get('blog_information')
        blog_sub_heading = request.POST.get('blog_sub_heading')
        blog_sub_information = request.POST.get('blog_sub_information')
        # Save the event details to the database
        blog = Blogs(blog_date=blog_date, blog_title=blog_title, blog_authorName=blog_authorName, blog_authorRole=blog_authorRole, blog_author_image=blog_author_image, blog_information=blog_information, blog_sub_heading=blog_sub_heading, blog_sub_information=blog_sub_information)
        blog.save()
        return render(request, 'Admin/adminaddblogs.html', {'popup_message': 'Form Submitted successfully.'})
    return render(request, 'Admin/adminaddblogs.html')


def view_blogs(request):
    blogs = Blogs.objects.all()
    return render(request, 'Admin/admin_viewblogs.html', {'blogs': blogs})

def edit_blog_view(request, blog_id):
    blog = get_object_or_404(Blogs, pk=blog_id)
    
    if request.method == 'POST':
        blog.blog_date = request.POST.get('blog_date')
        blog.blog_title = request.POST.get('blog_title')
        blog.blog_authorName = request.POST.get('blog_authorName')
        blog.blog_authorRole = request.POST.get('blog_authorRole')
        
        if 'blog_author_image' in request.FILES:
            blog.blog_author_image = request.FILES['blog_author_image']
        
        blog.blog_information = request.POST.get('blog_information')
        blog.blog_sub_heading = request.POST.get('blog_sub_heading')
        blog.blog_sub_information = request.POST.get('blog_sub_information')
        
        blog.save()
        return redirect('/admin_view_blogs/', {'popup_message': 'Form Submitted successfully.'})

    return render(request, 'Admin/admin_editblog.html', {'blog': blog})


def adminview_public_eventregisterview(request):
    public_eventregister = public_eventsregister.objects.all()
    return render(request, 'Admin/adminview_public_eventregister.html', {'registrations':public_eventregister})

def adminview_members_eventregisterview(request):
    members_eventregisters = members_eventregister.objects.all()
    return render(request, 'Admin/adminview_members_eventregister.html', {'registration':members_eventregisters})

def admin_edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event.event_name = request.POST.get('event_name')
        event.event_date = request.POST.get('event_date')
        event.event_time = request.POST.get('event_time')
        event.event_details = request.POST.get('event_details')
        event.meeting_link = request.POST.get('meeting_link')
        event.event_image = request.FILES.get('event_image')
        event.by = request.POST.get('by')  # New field
        event.save()
        return redirect('/adminUpcomingevents/', {'popup_message': 'Event updated successfully.'})
    
    return render(request, 'Admin/admin_editevents.html', {'event': event})

def adminUpcomingeventsviews(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(event_date__gte=today, event_status='Upcoming')

    for event in upcoming_events:
        event.check_and_update_status()

    # Refetch the updated events
    upcoming_events = Event.objects.filter(event_date__gte=today, event_status='Upcoming')
    
    return render(request, 'Admin/adminUpcomingevents.html', {'events': upcoming_events})


def end_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.event_status = 'Completed'  # Set status or a flag to mark as completed
        event.save()
        return render(request, 'Admin/adminUpcomingevents.html', {'popup_message': 'Event Ended Successfully.'})  # Redirect to Upcoming Events page
    return render(request, 'Admin/adminUpcomingevents.html')

def adminCompletedeventsviews(request):
    completed_events = Event.objects.filter(event_status='Completed')
    return render(request, 'Admin/adminCompletedevents.html', {'events': completed_events})

def adminaddtrainingsview(request):
    if request.method == 'POST':
        training_title = request.POST.get('training_title')
        training_description = request.POST.get('training_description')
        video_file = request.FILES.get('video_file')
        video_link = request.POST.get('video_link')
        training_image = request.FILES.get('training_image')

        # Create and save the Training instance
        training = Training(
            training_title=training_title,
            training_description=training_description,
            video_file=video_file if video_file else None,
            video_link=video_link if video_link else None,
            training_image=training_image if training_image else None
        )
        training.save()
        return redirect('/adminaddtrainings/', {'popup_message': 'Form Submitted successfully.'})

    return render(request, 'Admin/adminaddtrainings.html')
    

def view_trainingsview(request):
    trainings = Training.objects.all()
    return render(request, 'Admin/admin_viewtrainings.html', {'trainings': trainings})

def edit_training_view(request, id):
    training = get_object_or_404(Training, id=id)

    if request.method == 'POST':
        training_title = request.POST.get('training_title')
        training_description = request.POST.get('training_description')
        video_file = request.FILES.get('video_file')
        video_link = request.POST.get('video_link')
        training_image = request.FILES.get('training_image')

        # Update the Training instance
        training.training_title = training_title
        training.training_description = training_description
        if video_file:
            training.video_file = video_file
        if video_link:
            training.video_link = video_link
        if training_image:
            training.training_image = training_image

        # Save the updated instance
        training.save()

        messages.success(request, "Training updated successfully!")
        return render(request, 'Admin/admin_edit_training.html', {'training': training, 'popup_message': 'Form Submitted successfully.'})

    return render(request, 'Admin/admin_edit_training.html', {'training': training})

def uploadvideoview(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')  # Retrieve thumbnail file

        # Create a new Video object and save to database
        video = Video(title=title, description=description, video_file=video_file, thumbnail=thumbnail)
        video.save()

        # Redirect to a success page or render a success message
        return render(request, 'Admin/adminaddvideos.html', {'popup_message': 'Form Submitted successfully.'})  # Replace 'success-url' with your actual success URL or view name

    return render(request, 'Admin/adminaddvideos.html')

def view_videos(request):
    videos = Video.objects.all()
    return render(request, 'Admin/admin_viewgallery.html', {'videos': videos})

def edit_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
    
    if request.method == 'POST':
        video.title = request.POST.get('title')
        video.description = request.POST.get('description')
        if request.FILES.get('video_file'):
            video.video_file = request.FILES.get('video_file')
        if request.FILES.get('thumbnail'):
            video.thumbnail = request.FILES.get('thumbnail')

        video.save()

        return redirect('/view_videos/', {'popup_message': 'Form Submitted successfully.'})
    
    return render(request, 'Admin/admin_edit_gallery.html', {'video': video})


def admin_view_paymentview(request):
    payments = Payment.objects.all()
    return render(request, 'Admin/admin_viewpayment.html', {'payments': payments})

# -------------------------------------------------------------------------------------------------------------
# All Members view appear here

from django.shortcuts import render, redirect
from .models import Member, members_eventregister, Event, Blogs, FlashNews

def memberhomeview(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        user = Member.objects.get(pk=user_id)

        # Calculate counts
        total_events = Event.objects.count()
        event_registrations_count = members_eventregister.objects.filter(email=user.email).count()
        total_blogs = Blogs.objects.count()
        total_trainings = Training.objects.count()

        # Fetch registered events
        registered_event_names = members_eventregister.objects.filter(email=user.email).values_list('event_name', flat=True)
        registered_events = Event.objects.filter(event_name__in=registered_event_names).distinct()

        # Fetch flash news
        flash_news = FlashNews.objects.order_by('-created_at').first()

        return render(request, 'Members/membershomepage.html', {
            'username': user.username,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,  # Pass profile picture URL
            'flash_news': flash_news,
            'total_events': total_events,
            'event_registrations_count': event_registrations_count,
            'total_blogs': total_blogs,
            'total_trainings': total_trainings,
            'registered_events': registered_events
        })
    else:
        return redirect('/login/')





def user_logout(request):
    logout(request)
    return redirect('/userlogin/')

def adminaddblogsview(request):
    return render(request, 'Admin/adminaddblogs.html')

def save_documentview(request):
    if request.method == "POST":
        doc_name = request.POST.get('doc_name')
        about_doc = request.POST.get('about_doc')

        # Handle image upload
        if request.FILES.get('admin_doc'):
            admin_doc = request.FILES['admin_doc']
            fs = FileSystemStorage()
            filename = fs.save(admin_doc.name, admin_doc)
            admin_doc_url = fs.url(filename)
        else:
            admin_doc_url = None

        # Save the event details to the database
        document = Document(doc_name=doc_name, about_doc=about_doc, admin_doc=admin_doc_url)
        document.save()

        return render(request, 'Admin/admindocument.html')
    return render(request, 'Admin/admindocument.html')

def documentview(request):
    blogs = Blogs.objects.all()
    return render(request, 'document.html', {'blogs': blogs})

      
def members_videogalleryview(request):
    videos = Video.objects.all()
    return render(request, 'Members/members_videogallery.html', {'videos': videos})    


def members_blogsviews(request):
    blogs = Blogs.objects.all()
    return render(request, 'Members/members_blogs.html', {'blogs': blogs})

def like_blog(request, blog_id):
    blog = get_object_or_404(Blogs, pk=blog_id)
    if request.user.is_authenticated:
        if request.user not in blog.likes.all():
            blog.likes.add(request.user)
            likes_count = blog.likes.count()
            return JsonResponse({'success': True, 'likes_count': likes_count})
        else:
            return JsonResponse({'success': False, 'error': 'User already liked this blog.'})
    else:
        return JsonResponse({'success': False, 'error': 'User is not authenticated.'})
    


def edit_profile(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')  # Retrieve user ID from session
        if user_id:
            user = Member.objects.get(pk=user_id)
            # Update user fields based on the form data
            user.username = request.POST.get('username')
            user.age = request.POST.get('age')
            user.gender = request.POST.get('member_gender')  # Ensure this matches the form field
            user.contactno = request.POST.get('contactno')
            user.email = request.POST.get('email')
            
            # Handle profile picture
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            
            user.save()
            return redirect('/memberhome/')  # Redirect to profile page after editing
    else:
        user_id = request.session.get('user_id')
        if user_id:
            user = Member.objects.get(pk=user_id)
            return render(request, 'Members/edit_profile.html', {'user': user})
        else:
            return redirect('/public/')  # Redirect to login if not authenticated




        


def change_password(request):
    popup_message = None
    if request.method == 'POST':
        user_email = request.POST.get('user_email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            # Fetch the user based on email
            user = Member.objects.get(email=user_email)
            
            # Check if the current password matches
            if user.password == current_password:
                # Check if new password and confirm password match
                if new_password == confirm_password:
                    # Update the password
                    user.password = new_password
                    user.save()
                    popup_message = 'Password successfully changed.'
                    return redirect('/memberhome/', {'popup_message': popup_message})  # Redirect to homepage with popup
                else:
                    popup_message = 'New password and confirm password do not match.'
            else:
                popup_message = 'Current password is incorrect.'
        except Member.DoesNotExist:
            popup_message = 'User not found.'

    return render(request, 'Members/change_password.html', {'popup_message': popup_message})


def like_post(request, blog_id):
    if request.method == 'POST':
        blog = Blogs.objects.get(pk=blog_id)
        if request.user in blog.likes.all():
            blog.likes.remove(request.user)
        else:
            blog.likes.add(request.user)
        return redirect('documentview')  # Redirect back to the document view or wherever appropriate
    else:
        return HttpResponseBadRequest('Only POST requests are allowed')



def members_events_view(request):
    events = Event.objects.all()
    return render(request, 'Members/members_events.html', {'events': events})



def members_eventregister_view(request):
    user_email = request.session.get('user_email')
    event_id = request.GET.get('event_id')  # Get event ID from query parameter

    if not user_email:
        messages.error(request, 'Please log in first.')
        return redirect('/userlogin/')  # Redirect to login if not authenticated

    try:
        user = Member.objects.get(email=user_email)
    except Member.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('/userlogin/')  # Redirect to login if user not found

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        messages.error(request, 'Event not found.')
        return redirect('/events/')  # Redirect to events page if event not found

    if request.method == 'POST':
        # Save form data into members_eventregister
        new_registration = members_eventregister(
            username=request.POST.get('members_eventusername'),
            age=int(request.POST.get('members_eventage')),
            contactno=request.POST.get('members_eventcontactno'),
            gender=request.POST.get('gender'),
            email=request.POST.get('members_eventemail'),
            event_name=request.POST.get('members_eventname')
        )
        new_registration.save()
        messages.success(request, 'Registration successful!')
        return render(request, 'Members/members_eventregister.html')  # Redirect to a success page

    return render(request, 'Members/members_eventregister.html', {'user': user, 'event': event})
   


def members_eventsupcoming(request):
    now = timezone.now()  # Use timezone-aware datetime
    events = Event.objects.filter(event_date__gte=now, event_status='Upcoming')  # Filter upcoming events
    return render(request, 'Members/members_upcomingevents.html', {'events': events})


def members_eventscompleted(request):
    completed_events = Event.objects.filter(event_status='Completed')  # Filter completed events
    return render(request, 'Members/members_completedevents.html', {'events': completed_events})
    



def event_feedbackview(request):
    event_id = request.GET.get('event_id')
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        contact_no = request.POST.get('contact_no')
        user_name = request.POST.get('user_name')
        feedback = request.POST.get('event_feedback')
        
        EventFeedback.objects.create(
            event=event,
            contact_no=contact_no,
            user_name=user_name,
            feedback=feedback
        )
        
        messages.success(request, 'Thank you for your feedback!')
        return redirect('/events/completed/')
    
    # Pass the event name directly to the form
    return render(request, 'Members/members_event_feedback.html', {
        'event_name': event.event_name,
        'event': event,
    })





    # Redirect to a success page or another relevant page

def members_event_feedbackview(request, event_id):
    if request.method == "POST":
        user_email = request.POST.get('user_email')
        eventname = request.POST.get('eventname')
        event_feedback = request.POST.get('event_feedback')
        
        feedback = Event_Feedback(user_email=user_email, 
                              eventname=eventname, 
                              event_feedback=event_feedback)
        feedback.save()
        return render(request, 'Members/members_event_feedback.html')
    return render(request, 'Members/members_event_feedback.html')
    

def members_trainingsview(request):
    trainings = Training.objects.all()
    user_email = request.session.get('user_email')
    user_id = request.session.get('user_id')

    if user_id:
        try:
            payment = Payment.objects.get(email=user_email)
            if payment.payment_status != 'Completed':
                messages.error(request, 'Payment is pending. Please complete the payment to access the training videos.')
                return redirect('/payment_page/')  # Redirect to payment page
        except Payment.DoesNotExist:
            messages.error(request, 'No payment record found. Please complete the payment to access the training videos.')
            return redirect('/trainingspayment_page/')  # Redirect to payment page

    return render(request, 'Members/members_trainings.html', {'trainings': trainings})

def members_generalfeedbackview(request):
    user_name = request.session.get('user_name')
    user_email = request.session.get('user_email')
    user_id = request.session.get('user_id')

    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        feedback = request.POST.get('feedback')

        # Fetch the contact number from the Member table
        member = Member.objects.get(id=user_id)
        contact_no = member.contactno

        # Save the feedback to the Feedback table
        Feedback.objects.create(
            gfeedback_username=user_name,
            gfeedback_email=user_email,
            gfeedback_contactno=contact_no,
            gfeedback_eventname=event_name,
            gfeedback=feedback
        )

        messages.success(request, 'Thank you for your feedback!')
        return redirect('/thank_you/')  # Redirect to a thank you page or any other page

    # Pass user details to the form
    context = {
        'user_name': user_name,
        'user_email': user_email,
        'user_contact': Member.objects.get(id=user_id).contactno,  # Retrieve contact number from the Member table
        'event_name': request.GET.get('event_name'),  # Pass event name from URL parameter
    }
    return render(request, 'Members/members_generalfeedback.html', context)


def trainingspayment_pageview(request):
    return render(request, 'Members/payment_page.html')



def payment_pageview(request):
    if request.method == 'POST':
        email = request.session.get('user_email')
        cardholder_name = request.session.get('user_name')
        amount = 800  # Hardcoded or dynamic based on your logic

        # Debug: Print statements
        print(f"Email: {email}")
        print(f"Cardholder Name: {cardholder_name}")
        print(f"Amount: {amount}")

        # Check if a payment record already exists for the given email
        if Payment.objects.filter(email=email).exists():
            messages.error(request, 'Payment has already been made with this email address.')
            return redirect('/payment_page/')  # Redirect back to the payment form

        # Create a new payment record with status 'Pending'
        try:
            payment = Payment.objects.create(
                member_id=request.session.get('user_id'),
                email=email,
                cardholder_name=cardholder_name,
                amount=amount,
                payment_status='Pending'
            )
            # For simplicity, we assume the payment is successful and update the status
            payment.payment_status = 'Completed'
            payment.save()
            messages.success(request, 'Payment completed successfully!')
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, 'An error occurred while processing the payment.')

        return redirect('/payment_page/')  # Redirect back to the payment form or a success page

    context = {
        'user_email': request.session.get('user_email'),
        'user_name': request.session.get('user_name'),
    }
    return render(request, 'Members/trainings_payment_page.html', context)

# -------------------------------------------------------------------------------------------------------------------------------------------------------


# def admin_chat_view(request):
#     members = Member.objects.all()
#     selected_member = None
#     messages = []

#     if request.method == "POST":
#         selected_member_id = request.POST.get('member_id')
#         selected_member = get_object_or_404(Member, id=selected_member_id)
#         messages = Message.objects.filter(
#             chatroom__in=ChatRoom.objects.filter(
#                 members__in=[selected_member, request.user]
#             )
#         ).order_by('timestamp')

#     context = {
#         'members': members,
#         'messages': messages,
#         'selected_member': selected_member,
#         'admin_name': request.session.get('admin_name'),
#     }
#     return render(request, 'Admin/admin_chat.html', context)


# def member_chat_view(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('/login/')  # Redirect if user is not logged in
    
#     try:
#         user = Member.objects.get(id=user_id)
#     except Member.DoesNotExist:
#         # Handle the case where the user does not exist
#         return redirect('/login/')  # Redirect if the user does not exist

#     try:
#         admin = Member.objects.get(username='admin')  # Ensure 'admin' exists or replace with actual admin fetching logic
#     except Member.DoesNotExist:
#         # Handle the case where the admin does not exist
#         return render(request, 'Members/member_chat.html', {'error_message': 'Admin not found.'})

#     chatroom = get_object_or_404(ChatRoom, members__in=[user, admin])

#     messages = Message.objects.filter(chatroom=chatroom).order_by('timestamp')

#     context = {
#         'messages': messages,
#         'user_name': request.session.get('user_name'),
#         'admin_name': 'Admin',
#     }
#     return render(request, 'Members/member_chat.html', context)

# def send_message(request):
#     if request.method == 'POST':
#         room_id = request.POST.get('room_id')
#         content = request.POST.get('content')
#         chatroom = get_object_or_404(ChatRoom, id=room_id)
        
#         # Ensure the sender is the logged-in user
#         Message.objects.create(
#             chatroom=chatroom,
#             sender=request.user,
#             content=content
#         )
#     return redirect('chat_view', room_id=room_id)
