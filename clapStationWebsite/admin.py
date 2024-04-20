from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(advertisements)
admin.site.register(upComingEvents)

class PostAdmin(admin.ModelAdmin):
  list_display = ("author", "about", "img",)
admin.site.register(posts,PostAdmin)

admin.site.register(Like)

class CommentAdmin(admin.ModelAdmin):
  list_display = ("author", "desc", "post")
admin.site.register(BlogComment,CommentAdmin)

class TutorAdmin(admin.ModelAdmin):
  list_display = ("name", "Profession_title", "Status")
admin.site.register(Tutor,TutorAdmin)

class TutorcontactAdmin(admin.ModelAdmin):
  list_display = ("get_name","name", "email", "phoneNo")
  def get_name(self, obj):
      return obj.tutor.name
  get_name.short_description = 'Tutor name'
admin.site.register(Tutorcontact,TutorcontactAdmin)

class EventAdmin(admin.ModelAdmin):
  list_display = ("event_author", "event_title", "category",)
admin.site.register(Event,EventAdmin)

class EventImageAdmin(admin.ModelAdmin):
  list_display = ["image", "get_event_title"]
  def get_event_title(self, obj):
      return obj.event.event_title
  get_event_title.short_description = 'event Title'
admin.site.register(EventImage,EventImageAdmin)


class EventbookingAdmin(admin.ModelAdmin):
  list_display = ("get_event_title","name", "email", "phoneNo",)
  def get_event_title(self, obj):
      return obj.event.event_title
  get_event_title.short_description = 'event Title'
admin.site.register(Eventbooking,EventbookingAdmin)



class Create_groupAdmin(admin.ModelAdmin):
  list_display = ("groupname",)
admin.site.register(Create_group,Create_groupAdmin)


class Create_bandsAdmin(admin.ModelAdmin):
  list_display = ("bandname", "bandaddress", "author",)
admin.site.register(Create_bands,Create_bandsAdmin)

class BandbookingAdmin(admin.ModelAdmin):
  list_display = ("get_bandname","name", "email", "phoneNo",)
  def get_bandname(self, obj):
      return obj.bands.bandname
  get_bandname.short_description = 'Band name'
admin.site.register(Bandbooking,BandbookingAdmin)


class SignupAdmin(admin.ModelAdmin):
  list_display = ("First_name", "Last_name", "mobile_email",)
admin.site.register(Signup,SignupAdmin)

class Contact_usAdmin(admin.ModelAdmin):
  list_display = ("First_N", "mobileno", "emailid",)
admin.site.register(Contact_us,Contact_usAdmin)

class Contact_infoAdmin(admin.ModelAdmin):
  list_display = ("address", "email", "mobile",)
admin.site.register(Contact_info,Contact_infoAdmin)



class ProfilephotoAdmin(admin.ModelAdmin):
  list_display = ("author","image")
admin.site.register(Profilephoto,ProfilephotoAdmin)

class ProfilevideoAdmin(admin.ModelAdmin):
  list_display = ("author", "title", "video",)
admin.site.register(Profilevideo,ProfilevideoAdmin)

class About_pageAdmin(admin.ModelAdmin):
  list_display = ("title",)
admin.site.register(About_page,About_pageAdmin)

class About_service_pageAdmin(admin.ModelAdmin):
  list_display = ("title",)
admin.site.register(About_service_page,About_service_pageAdmin)

class About_team_pageAdmin(admin.ModelAdmin):
  list_display = ("member", "occuption")
admin.site.register(About_team_page,About_team_pageAdmin)

class About_our_missionAdmin(admin.ModelAdmin):
  list_display = ("title",)
admin.site.register(About_our_mission,About_our_missionAdmin)




class Academic_ImageAdmin(admin.StackedInline):
    model = Academic_Image

class Academic_feestructureAdmin(admin.StackedInline):
    model = Academic_feestructure

class Academic_MentorAdmin(admin.StackedInline):
    model = Academic_Mentor

@admin.register(Academic_page)
class Academic_pageAdmin(admin.ModelAdmin):
    list_display = ("academic_title", "venue")
    inlines = [Academic_ImageAdmin, Academic_feestructureAdmin, Academic_MentorAdmin]

 
    # other admin options for Academic_page model
@admin.register(Academic_Image)
class Academic_ImageModelAdmin(admin.ModelAdmin):
    list_display = ["image", "get_academic_title"]

    def get_academic_title(self, obj):
        return obj.academic.academic_title

    get_academic_title.short_description = 'Academic Title'


@admin.register(Academic_feestructure)
class Academic_feestructureModelAdmin(admin.ModelAdmin):
    list_display = ["price", "get_academic_title"]

    def get_academic_title(self, obj):
        return obj.academic.academic_title

    get_academic_title.short_description = 'Academic Title'

@admin.register(Academic_Mentor)
class Academic_MentorModelAdmin(admin.ModelAdmin):
    list_display = ["mentor_name","mentor_profession", "get_academic_title"]

    def get_academic_title(self, obj):
        return obj.academic.academic_title

    get_academic_title.short_description = 'Academic Title'




class jammingimageAdmin(admin.StackedInline):
    model = jammingimage

class jammingcontactAdmin(admin.StackedInline):
    model = jammingcontact

@admin.register(Jamming)
class JammingAdmin(admin.ModelAdmin):
    list_display = ("title", "location","charges","number_of_grounds")
    inlines = [jammingimageAdmin, jammingcontactAdmin]
    

@admin.register(jammingimage)
class jammingimageModelAdmin(admin.ModelAdmin):
    list_display = ["get_title", "image"]

    def get_title(self, obj):
        return obj.jamming.title

    get_title.short_description = 'jamming Title'

@admin.register(jammingcontact)
class jammingcontactModelAdmin(admin.ModelAdmin):
    list_display = ["get_title", "whatsapp","facebook","instagram","contact_no",]

    def get_title(self, obj):
        return obj.jamming.title

    get_title.short_description = 'jamming Title'