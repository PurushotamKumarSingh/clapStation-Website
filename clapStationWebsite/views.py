from django.shortcuts import render, HttpResponse, redirect , get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from datetime import datetime
from django.utils.dateparse import parse_date
from .models import *
from django.utils import timezone
from django.core.paginator import PageNotAnInteger, Paginator,EmptyPage
from .forms import *
from clapStationWebsite.filters import *
from django.http import JsonResponse
from django.contrib.auth import get_user_model
# Create your views here.

def starting_page(request):
    try:
        post = posts.objects.all().order_by('-id')
        all_user = Signup.objects.all()

        user = request.user
        page_number = request.GET.get('page', 1)
        paginator = Paginator(post, 3)
        total_pages = paginator.num_pages  # Corrected this line
        try:
            post = paginator.page(page_number)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

    except posts.DoesNotExist:
        post = None

    try:
        advertisement = advertisements.objects.order_by('-id').first()
    except advertisement.DoesNotExist:
        advertisement = None

    try:
        upComingEvent = upComingEvents.objects.all().order_by('-id').first()
    except upComingEvent.DoesNotExist:
        upComingEvent = None

    events = None
    user_profile = None
    if request.method == "POST":
        try:
            postContent = request.POST.get("post-content")
            postImg = request.FILES.get("post-image")

            if request.user.is_authenticated and postImg:
                posts.objects.create(about=postContent, img=postImg, author=request.user)
                return redirect("/")
            else:
                if not request.user.is_authenticated:
                    messages.error(request, 'You need to log in to create a post.')
                elif not postImg:
                    messages.error(request, 'Image upload is mandatory.')
                return redirect("/")
        except Exception as e:
            messages.error(request, f'Error uploading post: {e}')
            import logging
            logging.exception("Error uploading post")

    if user.is_authenticated:
        try:
            user_profile = Signup.objects.get(user=request.user)
        except Signup.DoesNotExist:
            user_profile = None
        try:
            events = Event.objects.all()
        except Event.DoesNotExist:
            events = None

    context = {
        "post": post,
        "lastpage": total_pages,
        "totalpagelist": [n + 1 for n in range(total_pages)],
        'user': user,
        "advertisement": advertisement,
        "upComingEvent": upComingEvent,
        "user_profile": user_profile,
        "events": events,
        "all_user": all_user,
    }

    return render(request, 'index.html', context)

def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = posts.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, post=post_obj)  # Use 'post' instead of 'post_id'

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    referring_page = request.META.get('HTTP_REFERER', '/profile')

    if '/artistiProfile' in referring_page:
        referring_page = '/artistiProfile'
    return redirect(referring_page)


def postedit(request,id):
    post=get_object_or_404(posts, id=id)
    

    context={
        'post':post,
    }
    return render(request,'postedit.html',context)


def postupdate(request, id):
    post = get_object_or_404(posts, id=id)

    if request.method == "POST":
        postContent = request.POST.get("post-content")
        postImg = request.FILES.get("post-image")

        # Update the existing post instance
        post.about = postContent
        post.img = postImg
        post.created_at = timezone.now()  # Set the created_at field

        post.save()
        return redirect('/')

    return redirect('postedit', id=id)

def postdelete(request,id):
    post = posts.objects.get(pk=id)
    post.delete()
    return redirect("starting-page")


def Addcomment(request, post_id):
    post = get_object_or_404(posts, id=post_id)
    all_user=Signup.objects.all()

    if request.method == "POST":
        addcomment = request.POST.get("comment")
        if request.user.is_authenticated:
            if addcomment:
                addcomment_page = BlogComment.objects.create(
                    desc=addcomment,
                    post_date=timezone.now(),  # Use timezone.now() for current date and time
                    author=request.user,
                    post=post
                )
                messages.success(request, 'Comment created successfully.')
            else:
                messages.error(request, 'Comment is required.')
        else:
            messages.error(request, 'User not authenticated.')

    addcomment_page = BlogComment.objects.filter(post=post).order_by('-id')

    context = {
        'addcomment_page': addcomment_page,
        'post': post,
        'all_user':all_user,
        
    }
    return render(request, 'Addcomment.html', context)


def Tutor_view(request):
    try:
        tutorcon = Tutor.objects.all()
    except Tutor.DoesNotExist:
        tutorcon = None

    context ={'tutorcon': tutorcon}    

    return render(request, 'tutor.html',context)

def TutorContact(request, id):
    tutor = get_object_or_404(Tutor, id=id)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        candidate = request.POST['candidate']
        category = request.POST['category']
        address = request.POST['city']

        if request.user.is_authenticated:
            # Create the Eventbooking object and associate it with the specific Event
            tutorContact = Tutorcontact.objects.create(
                name=name,
                email=email,
                phoneNo=phone,
                numOfcandidate=candidate,
                category=category,
                address=address,
                time=timezone.now(),
                tutor=tutor  # Set the foreign key 'event' to the specific Event
            )
            return redirect("Tutor_view")

    return render(request, 'tutorcontact.html', {'tutor': tutor})



# create group

def groups_page(request):
    print(request.user)
    if request.method == "POST":
        try:
            groupname = request.POST.get("Groupname")
            singername = request.POST.get("sname")
            singerprofession = request.POST.get("sprofession")
            singeraddress = request.POST.get("saddress")
            singerimage = request.FILES.get("simage")
            singerlinkedinid = request.POST.get("slinkedin")
            singerinstagramid = request.POST.get("sinstagram")
            singergithubid = request.POST.get("sgithub")
            # musician
            musicianname = request.POST.get("mname")
            musicianprofession = request.POST.get("mprofession")
            musicianaddress = request.POST.get("maddress")
            musicianimage = request.FILES.get("mimage")
            musicianlinkedinid = request.POST.get("mlinkedin")
            musicianinstagramid = request.POST.get("minstagram")
            musiciangithubid = request.POST.get("mgithub")
            # guitarist
            guitaristname = request.POST.get("gname")
            guitaristprofession = request.POST.get("gprofession")
            guitaristaddress = request.POST.get("gaddress")
            guitaristimage = request.FILES.get("gimage")
            guitaristlinkedinid = request.POST.get("glinkedin")
            guitaristinstagramid = request.POST.get("ginstagram")
            guitaristgithubid = request.POST.get("ggithub")
            groupdescription = request.POST.get("Description")

            if request.user.is_authenticated:
                if groupname:
                    group_page = Create_group.objects.create(
                        groupname=groupname,
                        singername=singername,
                        singerprofession=singerprofession,
                        singeraddress=singeraddress,
                        singerimage=singerimage,
                        singerlinkedinid=singerlinkedinid,
                        singerinstagramid=singerinstagramid,
                        singergithubid=singergithubid,
                        musicianname=musicianname,
                        musicianprofession=musicianprofession,
                        musicianaddress=musicianaddress,
                        musicianimage=musicianimage,
                        musicianlinkedinid=musicianlinkedinid,
                        musicianinstagramid=musicianinstagramid,
                        musiciangithubid=musiciangithubid,
                        guitaristname=guitaristname,
                        guitaristprofession=guitaristprofession,
                        guitaristaddress=guitaristaddress,
                        guitaristimage=guitaristimage,
                        guitaristlinkedinid=guitaristlinkedinid,
                        guitaristinstagramid=guitaristinstagramid,
                        guitaristgithubid=guitaristgithubid,
                        groupdescription=groupdescription,
                        author=request.user
                    )
                    group_page.save()
                    messages.success(request, 'Group created successfully.')
                else:
                    messages.error(request, 'Group name is required.')
            else:
                messages.error(request, 'User not authenticated.')
        except Exception as e:
            messages.error(request, f'Error creating group: {e}')
            import logging
            logging.exception("Error creating group")
        return redirect('groups')
    
     
    if request.user.is_authenticated:
        user_info=Signup.objects.get(user_id=request.user.id)
    else:
        user_info=None
    group_page = Create_group.objects.all().order_by('-id')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(group_page, 4)

    try:
        group_page = paginator.page(page_number)
    except PageNotAnInteger:
        group_page = paginator.page(1)
    except EmptyPage:
        group_page = paginator.page(paginator.num_pages)

    total_pages = paginator.num_pages
    
    return render(request, 'groups.html', {'user_info':user_info,'group_page': group_page,'lastpage': total_pages, 'totalpagelist': [n+1 for n in range(total_pages)]})

def groupedit(request,id):
    group_page=Create_group.objects.all()
    

    context={
        'group_page':group_page,
    }
    return render(request,'groups.html',context)


def groupupdate(request, id):
    group_page = get_object_or_404(Create_group, id=id)

    if request.method == "POST":
        groupname = request.POST.get("Groupname")
        singername = request.POST.get("sname")
        singerprofession = request.POST.get("sprofession")
        singeraddress = request.POST.get("saddress")
        singerimage = request.FILES.get("simage")
        singerlinkedinid = request.POST.get("slinkedin")
        singerinstagramid = request.POST.get("sinstagram")
        singergithubid = request.POST.get("sgithub")
        # musician
        musicianname = request.POST.get("mname")
        musicianprofession = request.POST.get("mprofession")
        musicianaddress = request.POST.get("maddress")
        musicianimage = request.FILES.get("mimage")
        musicianlinkedinid = request.POST.get("mlinkedin")
        musicianinstagramid = request.POST.get("minstagram")
        musiciangithubid = request.POST.get("mgithub")
        # guitarist
        guitaristname = request.POST.get("gname")
        guitaristprofession = request.POST.get("gprofession")
        guitaristaddress = request.POST.get("gaddress")
        guitaristimage = request.FILES.get("gimage")
        guitaristlinkedinid = request.POST.get("glinkedin")
        guitaristinstagramid = request.POST.get("ginstagram")
        guitaristgithubid = request.POST.get("ggithub")
        groupdescription = request.POST.get("Description")

        # Update the existing group instance
        group_page.groupname = groupname
        group_page.singername = singername
        group_page.singerprofession = singerprofession
        group_page.singeraddress = singeraddress
        group_page.singerlinkedinid = singerlinkedinid
        group_page.singerinstagramid = singerinstagramid
        group_page.singergithubid = singergithubid
        if singerimage:
                group_page.singerimage = singerimage
                group_page.save()
                
        
        
        
        group_page.musicianname = musicianname
        group_page.musicianprofession = musicianprofession
        group_page.musicianaddress = musicianaddress
        group_page.musicianlinkedinid = musicianlinkedinid
        group_page.musicianinstagramid = musicianinstagramid
        group_page.musiciangithubid = musiciangithubid
        
        if musicianimage:
                group_page.musicianimage = musicianimage
                group_page.save()
        
        
        group_page.guitaristname = guitaristname
        group_page.guitaristprofession = guitaristprofession
        group_page.guitaristaddress = guitaristaddress
        group_page.guitaristlinkedinid = guitaristlinkedinid
        group_page.guitaristinstagramid = guitaristinstagramid
        group_page.guitaristgithubid = guitaristgithubid
        group_page.groupdescription = groupdescription
        group_page.created_at = timezone.now()
        
        if guitaristimage:
                group_page.guitaristimage = guitaristimage
                group_page.save()

        # Set the author field
        group_page.author = request.user

        group_page.save()
        return redirect('groups')
    
    return render(request, 'groups.html', {'group_page': group_page})

def groupdelete(request,id):
    group_page = Create_group.objects.get(pk=id)
    group_page.delete()
    return redirect("groups")


#bandpage
#bandpage
def bands_page(request):
    if request.method == "POST":
        try:
            bandname = request.POST.get("Bandname")
            bandbudget = request.POST.get("Bandbudget")
            bandaddress = request.POST.get("Bandaddress")
            bandimage = request.FILES.get("Bandimage")
            banddescription = request.POST.get("Banddescription")
            if request.user.is_authenticated:
                if bandname:
                    bands_page = Create_bands.objects.create(
                        bandname=bandname,
                        bandbudget=bandbudget,
                        bandaddress=bandaddress,
                        bandimage=bandimage,
                        banddescription=banddescription,
                        author=request.user)
                    bands_page.save()
                    messages.success(request, 'Bands created successfully.')
                else:
                    messages.error(request, 'Bands file is required.')
            else:
                messages.error(request, 'User not authenticated.')
        except Exception as e:
            messages.error(request, f'Error creating bands: {e}')
            import logging
            logging.exception("Error creating bands")

        return redirect('bands')
    
    if request.user.is_authenticated:
        user_info=Signup.objects.get(user_id=request.user.id)
    else:
        user_info=None
        
    bands_page = Create_bands.objects.all().order_by('-id')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(bands_page, 4)

    try:
        bands_page = paginator.page(page_number)
    except PageNotAnInteger:
        bands_page = paginator.page(1)
    except EmptyPage:
        bands_page = paginator.page(paginator.num_pages)

    total_pages = paginator.num_pages
    return render(request, 'bands.html', {"user_info":user_info,"bands_page": bands_page,
    'lastpage': total_pages,
     'totalpagelist': [n+1 for n in range(total_pages)]
     }
     )

def bandsedit(request,id):
    bands_page=Create_bands.objects.all()
    

    context={
        'bands_page':bands_page,
    }
    return render(request,'bands.html',context)

def bandsupdate(request, id):
    post = get_object_or_404(Create_bands, id=id)

    if request.method == "POST":
        bandname = request.POST.get("Bandname")
        bandbudget = request.POST.get("Bandbudget")
        bandaddress = request.POST.get("Bandaddress")
        bandimage = request.FILES.get("Bandimage")
        banddescription = request.POST.get("Banddescription")

        # Update the existing post instance
        post.bandname = bandname
        post.bandbudget = bandbudget
        post.bandaddress = bandaddress
        post.bandimage = bandimage
        post.banddescription = banddescription
        post.created_at = timezone.now()

        # Set the author field
        post.author = request.user

        post.save()
        return redirect('bands')
    return render(request, 'bands.html', {'bands_page': post})


def bandsdelete(request,id):
    bands_page = Create_bands.objects.get(pk=id)
    bands_page.delete()
    return redirect("bands")

def bandbooking(request, id):
    bands = get_object_or_404(Create_bands, id=id)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        candidate = request.POST['candidate']
        category = request.POST['category']
        address = request.POST['city']
        hour = request.POST['hour']
        date = request.POST['date']
        address = request.POST['city']

        if request.user.is_authenticated:
            # Create the Eventbooking object and associate it with the specific Event
            bandbooking = Bandbooking.objects.create(
                name=name,
                email=email,
                phoneNo=phone,
                numOfcandidate=candidate,
                category=category,
                address=address,
                hour=hour,
                date=date,
                time=timezone.now(),
                bands = bands  # Set the foreign key 'event' to the specific Event
            )
            return redirect("bands")

    return render(request, 'bandbooking.html', {'bands': bands})



#academies
def academies_page(request):
    academic=Academic_page.objects.all().order_by('-id')
    academicimage=Academic_Image.objects.all()
    academicfee=Academic_feestructure.objects.all()[0:3]
    academicmentor=Academic_Mentor.objects.all()[:3]
    page_number = request.GET.get('page', 1)
    paginator = Paginator(academic, 8)

    try:
        academic = paginator.page(page_number)
    except PageNotAnInteger:
        academic = paginator.page(1)
    except EmptyPage:
        academic = paginator.page(paginator.num_pages)

    total_pages = paginator.num_pages
    
    context={
        "academic":academic,
        "academicimage":academicimage,
        "academicfee":academicfee,
        "academicmentor":academicmentor,
        'lastpage': total_pages,
        'totalpagelist': [n+1 for n in range(total_pages)]
    }
    return render(request, 'academies.html',context)

def academy_detail(request, id):
    academic = get_object_or_404(Academic_page, id=id)
    academicimage = Academic_Image.objects.filter(academic=academic)
    academicfee = Academic_feestructure.objects.filter(academic=academic)[0:3]
    academicmentor = Academic_Mentor.objects.filter(academic=academic)[0:3]
    context = {
        "academic": academic,
        "academicimage": academicimage,
        "academicfee": academicfee,
        "academicmentor": academicmentor
    }
    return render(request, 'academy_detail.html', context)



#event page
def events_page(request):
    events = EventFilter(request.GET, queryset=Event.objects.all().order_by('-id'))
    eventsimage = EventImage.objects.all()

    page_number = request.GET.get('page', 1)
    paginator = Paginator(events.qs, 6)

    try:
        events = paginator.page(page_number)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    total_pages = paginator.num_pages
    context = {
        'events': events,
        'eventsimage': eventsimage,
        'lastpage': total_pages,
        'totalpagelist': [n+1 for n in range(total_pages)]
    }

    return render(request, 'events.html', context)


def eventsdata(request, id):
    events = get_object_or_404(Event, id=id)
    eventsimage = EventImage.objects.filter(event=events)
    event_adder=Signup.objects.get(user_id=events.event_author_id)
    return render(request, 'eventsdata.html', {'events': events, 'eventsimage': eventsimage,
    "event_adder":event_adder})


def add_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        duration = request.POST['duration']
        venue = request.POST['venue']
        city = request.POST['city']
        state = request.POST['state']
        date = request.POST['date']
        price = request.POST['price']
        poster = request.FILES.get('poster')
        images = request.FILES.getlist('images')

        if request.user.is_authenticated:
            # Create the Event object
            new_event = Event.objects.create(
                event_title=title,
                description=description,
                category=category,
                duration=duration,
                venue=venue,
                city=city,
                state=state,
                date=date,
                ticket_price=price,
                poster=poster,
                event_author=request.user
            )

            # Associate images with the created event using EventImage
            for image in images:
                EventImage.objects.create(event=new_event, image=image)

            return redirect("events")

    return render(request, 'profile.html')


        
def delete_event(request,id):
    event=Event.objects.get(id=id)
    event.delete()
    return redirect("profile")


def eventsedit(request,id):
    events=Event.objects.all()
    context={
        'events':events,
    }
    return render(request,'profile.html',context)

def eventsupdate(request, id):
    events = get_object_or_404(Event, id=id)

    if request.method == 'POST':
        # Extract values from request.POST
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        duration = request.POST['duration']
        venue = request.POST['venue']
        city = request.POST['city']
        state = request.POST['state']
        date = request.POST['date']
        price = request.POST['price']
        poster = request.FILES.get('poster')
        images = request.FILES.getlist('images')

        # Your existing code...

        # Update the existing event instance
        events.event_title = title
        events.description = description
        events.category = category
        events.duration = duration
        events.venue = venue
        events.city = city
        events.state = state
        events.ticket_price = price
        events.date= date

        # Handle images field separately
        try:
            # Validate and save each image individually
            for img in images:
                events_image = EventImage(event=events, image=img)
                events_image.save()
        except ValidationError as e:
            return render(request, 'profile.html', {'events': events, 'error_message': f'Invalid image: {e}'})
        
        events.poster = poster

        # Set the event_author field if not already set
        if not events.event_author:
            events.event_author = request.user

        events.save()
        return redirect('events')

    return render(request, 'profile.html', {'events': events})



def eventbooking(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        candidate = request.POST['candidate']
        category = request.POST['category']
        address = request.POST['city']

        if request.user.is_authenticated:
            # Create the Eventbooking object and associate it with the specific Event
            eventbooking = Eventbooking.objects.create(
                name=name,
                email=email,
                phoneNo=phone,
                numOfcandidate=candidate,
                category=category,
                address=address,
                time=timezone.now(),
                event=event  # Set the foreign key 'event' to the specific Event
            )
            return redirect("events")

    return render(request, 'eventbooking.html', {'events': event})


#artist page

def artists_page(request):
    signups = Signup.objects.all().order_by('-id')
    artists = [signup for signup in signups if signup.role != 'Individual']  
    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(artists, 8)

    try:
        artists = paginator.page(page_number)
    except PageNotAnInteger:
        artists = paginator.page(1)
    except EmptyPage:
        artists = paginator.page(paginator.num_pages)

    total_pages = paginator.num_pages
    return render(request, 'artists.html', {
    'artists': artists,
    'lastpage': total_pages,
    'totalpagelist': [n+1 for n in range(total_pages)]
    })

def artist_profile(request, pk):
    user_profile = Signup.objects.get(id=pk)           
    # Fetch user's posts
    user_posts = posts.objects.filter(author=user_profile.user).order_by('-id')
    events = Event.objects.filter(event_author=user_profile.user).order_by('-id')[0:3]
    profileadvertisement = advertisements.objects.latest("created_at")
    profileupComingEvent = upComingEvents.objects.all().order_by('-id').first()
    profile_photo_page = Profilephoto.objects.filter(author=user_profile.user)
    profile_video_page=Profilevideo.objects.filter(author=user_profile.user)
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(user_posts, 3)

    try:
        user_posts = paginator.page(page_number)
    except PageNotAnInteger:
        user_posts = paginator.page(1)
    except EmptyPage:
        user_posts = paginator.page(paginator.num_pages)

    total_pages = paginator.num_pages

    return render(
        request,
        'artists_profile.html',
        {'user_profile': user_profile, 
        "profileupComingEvent":profileupComingEvent, 
        "profileadvertisement":profileadvertisement, 
        'user_posts': user_posts, 'lastpage': total_pages, 
        'totalpagelist': [n+1 for n in range(total_pages)], 
        'profile_photo_page': profile_photo_page,
        "events":events,
        "profile_video_page":profile_video_page}
    )


#about page

def about_page(request):
    try:
        aboutpage = About_page.objects.all().order_by('-id').first()
    except aboutpage.DoesNotExist:
        aboutpage=None

    try:
        aboutservicepage = About_service_page.objects.all().order_by('-id')[0:3]
    except aboutservicepage.DoesNotExist:
        aboutservicepage=None
    
    try:
        aboutteampage = About_team_page.objects.all()
    except aboutteampage.DoesNotExist:
        aboutteampage=None

    try:
        aboutaimpage = About_our_mission.objects.all().order_by('-id')[0:3]
    except aboutaimpage.DoesNotExist:
        aboutaimpage=None

    context={
        'aboutpage':aboutpage,
        'aboutservicepage':aboutservicepage,
        'aboutteampage':aboutteampage,
        'aboutaimpage':aboutaimpage
        }
    return render(request, 'about-us.html',context)



def profile_page(request):
    
    if request.method == "POST":
        try:
            postContent = request.POST.get("post-content")
            postImg = request.FILES.get("post-image")

            if request.user.is_authenticated and postImg:
                posts.objects.create(about=postContent, img=postImg, author=request.user)
                return redirect("")
            else:
                if not request.user.is_authenticated:
                    messages.error(request, 'You need to log in to create a post.')
                elif not postImg:
                    messages.error(request, 'Image upload is mandatory.')
                return redirect("")
        except Exception as e:
            import logging
            logging.exception("Error uploading post")

        # For creating a new image
        try:
            image = request.FILES.get("pimage")
            if request.user.is_authenticated:
                if image:
                    profile_photo_page = Profilephoto.objects.create(image=image, author=request.user)
                    profile_photo_page.save()
                    messages.success(request, 'Image created successfully.')
                
            else:
                messages.error(request, 'User not authenticated.')
        except Exception as e:
            messages.error(request, f'Error creating image: {e}')
            import logging
            logging.exception("Error creating image")

        # For creating a new video
        try:
            title = request.POST.get("title")
            video = request.FILES.get("pvideo")
            if request.user.is_authenticated:
                if video:
                    profile_video_page = Profilevideo.objects.create(video=video, title=title, author=request.user)
                    profile_video_page.save()
                    messages.success(request, 'Video created successfully.')
                
            else:
                messages.error(request, 'User not authenticated.')
        except Exception as e:
            messages.error(request, f'Error creating video: {e}')
            import logging
            logging.exception("Error creating video")

        return redirect('profile')

    # TO GET THE PROFILE PAGE DETAIL
    user_profile = get_object_or_404(Signup, user=request.user)
    user_posts = posts.objects.filter(author=request.user).order_by('-id')
    profile_photo_page = Profilephoto.objects.filter(author=request.user)
    profile_video_page=Profilevideo.objects.filter(author=request.user)
    profileadvertisement = advertisements.objects.order_by('-id').first()
    profileupComingEvent = upComingEvents.objects.all().order_by('-id').first()
    events = Event.objects.filter(event_author=request.user).order_by('-id')[0:3]

    page_number = request.GET.get('page', 1)
    paginator = Paginator(user_posts, 3)

    try:
        user_posts = paginator.page(page_number)
    except PageNotAnInteger:
        user_posts = paginator.page(1)
    except EmptyPage:
        user_posts = paginator.page(paginator.num_pages)

    total_pages = paginator.num_pages
    
    context={'user_profile': user_profile, 'user_posts': user_posts, 
        'lastpage': total_pages, 'totalpagelist': [n+1 for n in range(total_pages)],
         'profilephotopage': profile_photo_page,
         'profilevideopage':profile_video_page,
         "profileadvertisement":profileadvertisement,
         "profileupComingEvent":profileupComingEvent,
         'events':events}

    return render(request,'profile.html',context)


def edit_profile(request,id):
    userInfo= Signup.objects.get(user_id=id)
    if request.method=='POST':
        
        try:            
            fname= request.POST['First_name']
            lname = request.POST.get('Last_name')
            day = request.POST.get('birthday_day')
            month = request.POST.get('birthday_month')
            year = request.POST.get('birthday_year')
            role= request.POST.get('role')
            gender = request.POST.get('sex')
            profile_image = request.FILES.get("profile_image")
            
            userInfo.First_name=fname
            userInfo.Last_name=lname
            userInfo.day=day
            userInfo.month=month
            userInfo.year=year
            userInfo.gender=gender
            
            if role=="Individual":
                userInfo.role=role
            else:
                userInfo.role="Individual"
                
            if profile_image:
                userInfo.profile_image = profile_image
                userInfo.save()
                messages.success(request, 'Profile updated successfully.')
                
                
            userInfo.save()
            return redirect('profile')

        except Exception as e:
            messages.error(request, f'Error updating profile: {e}')
            import logging
            logging.exception("Error updating profile")
            
    return render (request,'profile.html')


def deleteVideo(request,id):
    video=Profilevideo.objects.get(id=id)
    video.delete()
    return redirect('profile')

def deletePhoto(request,id):
    pic=Profilephoto.objects.get(id=id)
    pic.delete()
    return redirect('profile')

# jamming station
def jammingstation_page(request):
    articles = Jamming.objects.all().order_by('-id')
    jammingimages = jammingimage.objects.all()
    jammingcontacts = jammingcontact.objects.all()
    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(articles, 4)

    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    total_pages = paginator.num_pages
    context = {
        'articles': articles,
        'jammingimages': jammingimages,
        'jammingcontacts': jammingcontacts,
        'lastpage': total_pages,
    'totalpagelist': [n+1 for n in range(total_pages)]
    }
    return render(request, 'jamming-station.html', context)




def contact_page(request):
    contact_info = Contact_info.objects.all().first()
    
    if request.method == "POST":
        First_N = request.POST.get('First Name', '')
        Last_N = request.POST.get('Last Name', '')
        mobileno = request.POST.get('Mobile Number', '')
        emailid = request.POST.get('Email', '')
        address = request.POST.get('Address', '')
        
        if len(First_N) > 1 and len(Last_N) > 1 and len(mobileno) == 10 and len(emailid) > 10 and len(address) > 10:
            contact_usobj = Contact_us(First_N=First_N, Last_N=Last_N, mobileno=mobileno, emailid=emailid, address=address)
            contact_usobj.save()
            messages.info(request, 'Your contact form has been submitted successfully.')
        else:
            messages.error(request, 'Please fill the form correctly. Ensure all fields are filled and valid.')
            return HttpResponse('Please, fill valid data')
        
    context = {'contact_info': contact_info}
    return render(request, 'contact-us.html', context)

def signup_page(request):
    if request.method == "POST":
        username = request.POST['mobile_email']
        password = request.POST['password']
        
        
        if User.objects.filter(username=username).exists():
            # message for user exisstance
            
            messages.error(request, "User name already exists !")
            return render(request, 'signup.html')
        else:
            # Fetch all data from post request of signup submit
            profile_image = request.FILES.get('profile_image')
            
            First_name = request.POST['First_name']
            Last_name = request.POST['Last_name']
            mobile_email = request.POST['mobile_email']
            day = request.POST['birthday_day']
            month = request.POST['birthday_month']
            year = request.POST['birthday_year']
            role = request.POST['signup']
            gender = request.POST['sex']
            # Correct file field name
            
            user = User.objects.create_user(username=username, password=password, first_name=First_name, last_name=Last_name)
            

            # Assuming your Signup model has the necessary fields
            all_inputs = Signup(user=user, First_name=First_name, Last_name=Last_name, mobile_email=mobile_email,
                          day=day, month=month, year=year, role=role, gender=gender,profile_image=profile_image)
            all_inputs.save()

            return redirect('login')
    else:
        return render(request, 'signup.html')


def login_page(request):
    # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = (authenticate(username=username, password= password))
        if user is not None:
            login(request, user)
            messages.info(request, f'{user.first_name}, You are logged in.')
            return redirect('/')
        else:
            messages.info(request,  'Invalid Username Or Password')
            return render(request,'login.html')
    else:
        
        return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/')