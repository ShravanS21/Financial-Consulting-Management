from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.core.validators import RegexValidator

# Create your models here.

class Member(models.Model):
    username = models.CharField(max_length=150)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    contactno = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/')

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_details = models.TextField()
    meeting_link = models.URLField(max_length=200, blank=True, null=True)
    event_image = models.ImageField(null=True, blank=True, upload_to="images/")
    event_status = models.CharField(max_length=20, default='Upcoming')
    by = models.CharField(max_length=255, validators=[RegexValidator(r'^[A-Za-z\s]*$', 'Only letters and spaces are allowed')])

    def __str__(self):
        return self.event_name   
    
    def check_and_update_status(self):
        event_datetime = timezone.make_aware(datetime.combine(self.event_date, self.event_time))
        if event_datetime <= timezone.now() and self.event_status == 'Upcoming':
            self.event_status = 'Completed'
            self.save()

class Document(models.Model):
    doc_name = models.CharField(max_length=255)
    about_doc = models.CharField(max_length=255)
    admin_doc = models.ImageField(null=True, blank=True, upload_to="image/")
    add_doc = models.FileField(null=True, blank=True, upload_to="media/", max_length=254,)
    
    def __str__(self):
        return self.event_name 

class FlashNews(models.Model):
    admin_flash = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    gfeedback_username = models.TextField()
    gfeedback_email = models.CharField(max_length=50)
    gfeedback_contactno = models.CharField(max_length=10)
    gfeedback_eventname = models.TextField()
    gfeedback = models.TextField()


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Blogs(models.Model):
    blog_date = models.DateField()
    blog_title = models.CharField(max_length=200)
    blog_authorName = models.CharField(max_length=100)
    blog_authorRole = models.CharField(max_length=150)
    blog_author_image = models.ImageField(upload_to='Author/', null=True, blank=True)
    blog_information = models.CharField(max_length=20000, null=True, blank=True)
    blog_sub_heading = models.CharField(max_length=200, null=True, blank=True)
    blog_sub_information = models.CharField(max_length=20000, null=True, blank=True)

    # New fields for likes
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.blog_title
    
class public_eventsregister(models.Model):
    public_eventusername = models.CharField(max_length=255)
    public_eventage = models.CharField(max_length=2)
    public_eventcontactno = models.CharField(max_length=10)
    public_eventgender = models.CharField(max_length=10)
    public_eventemail = models.EmailField(max_length=255)
    public_eventname = models.CharField(max_length=255)

    def __str__(self):
        return self.public_eventusername   
    
class members_eventregister(models.Model):
    username = models.CharField(max_length=100)
    age = models.IntegerField()
    contactno = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=255)
    event_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} - {self.event_name}"    
           
class EventFeedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    feedback = models.TextField()
    
    def __str__(self):
        return f"Feedback for {self.event.event_name}"
    
class Training(models.Model):
    training_title = models.CharField(max_length=255)
    training_description = models.TextField()
    video_file = models.FileField(upload_to='training_video/', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    training_image = models.ImageField(upload_to='training_image/', blank=True, null=True)

class Event_Feedback(models.Model):
    user_email = models.CharField(max_length=50)
    eventname = models.TextField()
    event_feedback = models.TextField()


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    email = models.EmailField()
    cardholder_name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50, default='Pending')  # Default to 'Pending'
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('email',)  # Ensure unique email

    def __str__(self):
        return f"Payment {self.id} - {self.member.username}"


