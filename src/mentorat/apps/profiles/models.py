from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    
    # General information
    firstname = models.CharField(max_length=30, blank=False, verbose_name=_('first name'))
    surname = models.CharField(max_length=30, blank=False, verbose_name=_('surname'))
    previous_surname = models.CharField(max_length=30, blank=True, verbose_name=_('surname before marriage'))
    CNP = models.CharField(max_length=13, blank=False, verbose_name=_('CNP'))
    age = models.IntegerField(blank=True, null=True, verbose_name=_('age'))
    email = models.CharField(max_length=50, blank=False, verbose_name=_('email'))
    telephone = models.CharField(max_length=20, blank=False, verbose_name=_('telephone'))
    address = models.CharField(max_length=100, blank=False, verbose_name=_('address'))
    
    # Academic and professional information
    home_town = models.CharField(max_length=50, blank=False, verbose_name=_('home town'))
    graduated_college = models.CharField(max_length=100, blank=False, verbose_name=_('graduated college'))
    # volunteer = models.ManyToOneRel(VolunteerOrganization)    
    # fields_of_interest = models.ManyToManyField(FieldOfInterest, related_name='profiles', null=True, blank=False)
    
    # Additional information
    hobbies = models.TextField(blank=True, verbose_name=_('hobbies'))
    self_evaluation = models.TextField(blank=False, verbose_name=_('self evaluation as colleague'))
    # communication_ratings
    extra_info = models.TextField(blank=True, verbose_name=_('additional information'))

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return ('profile_detail', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        
    def as_student(self):
        studs = StudentProfile.objects.filter(pk=self.pk)
        if len(studs):
            return studs[0]
        return None
    
    def as_mentor(self):
        mentors = MentorProfile.objects.filter(pk=self.pk)
        if len(mentors):
            return mentors[0]
        return None
        
        
class StudentProfile(Profile):
    """Additional profile information for students"""
    # Specific general informations
    birthplace = models.CharField(max_length=50, blank=False, verbose_name=_('place of birth'))    
    faculty = models.CharField(max_length=100, blank=False, verbose_name=_('current faculty'))
    year_of_study = models.IntegerField(default=1, blank=False, verbose_name=_('year of study'))    
    major = models.CharField(max_length=100, blank=False, verbose_name=_('major'))    
    town_of_study = models.CharField(max_length=50, blank=False, verbose_name=_('city of study'))
    
    # Employment informations
    employer_name = models.CharField(max_length=50, blank=True, verbose_name=_('name of current employer'))
    employer_address = models.CharField(max_length=100, blank=True, verbose_name=_('address of current employer'))
    employee_position = models.CharField(max_length=100, blank=True, verbose_name=_('position help in current employment'))
    employee_duties = models.TextField(blank=True, verbose_name=_('duties at current work place'))
    
    # Specific Academic and professional information
    #work_experience
    #research
    future_plans = models.TextField(blank=True, verbose_name=_('plans the following year'))
    how_mentor_can_help = models.TextField(blank=False, verbose_name=_('how can a mentor help'))
        
    mentor_expectations = models.TextField(blank=False, verbose_name=_('what are your expectation for a mentor'))
    
    class Meta():
        verbose_name = _('student profile')
        
    def as_student(self):
        return self
    
    def as_mentor(self):
        return None
    
    def __unicode__(self):
        return 'Student(' + self.user.username + ')'
    
    
class MentorProfile(Profile):
    """Additional profile information for mentors"""    
    # Specific general informations
    graduated_faculty = models.CharField(max_length=100, blank=False, verbose_name=_('graduated faculty'))
    graduated_major = models.CharField(max_length=100, blank=False, verbose_name=_('graduated major'))
    graduation_date = models.DateField(blank=False, verbose_name=_('graduation date'))    
    employer_name = models.CharField(max_length=50, blank=False, verbose_name=_('employer name'))
    employer_address = models.CharField(max_length=100, blank=False, verbose_name=_('employer address'))
    employee_position = models.CharField(max_length=100, blank=False, verbose_name=_('position held in current emplyment'))
    employee_duties = models.TextField(blank=False, verbose_name=_('duties at current work place'))    
    mentorship_place = models.TextField(blank=False, verbose_name=_('city and country for mentorship'))
    
    post_bachelors_studies = models.TextField(blank=True, verbose_name=_('post bachelor\'s studies'))
    professional_experience = models.TextField(blank=False, verbose_name=_('professional experience'))
    #mentorship_activities
    other_mentorship_activities = models.TextField(blank=True, verbose_name=_('other mentorship activities'))
    
    class Meta():
        verbose_name = _('mentor profile')
        
    def as_mentor(self):
        return self
    
    def as_student(self):
        return None
    
    def __unicode__(self):
        return 'Mentor(' + self.user.username + ')'
    
    
class FieldOfInterest(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('field name'))
    
    def __unicode__(self):
        return self.name
    
    
class FieldOfInterest_Profile(models.Model):
    profile = models.ForeignKey(Profile, related_name='fields_of_interest')
    field = models.ForeignKey(FieldOfInterest, related_name='profile')
    
    def __unicode__(self):
        return self.field.name + ' ' + self.profile.user.username
       

class VolunteerOrganization(models.Model):
    profile = models.ForeignKey(Profile, related_name='volunteer', null=True, verbose_name=_('profile'))
    name = models.CharField(max_length=50, blank=False, verbose_name=_('organization name'))
    field = models.CharField(max_length=100, blank=True, verbose_name=_('working field'))
    
    def __unicode__(self):
        return self.name


class StudentEmployment(models.Model):
    student = models.ForeignKey(StudentProfile, related_name='work_experience', verbose_name=_('student'))
    internship = models.BooleanField(default=False, null=False, verbose_name=_('was internship'))
    employer_name = models.CharField(max_length=50, blank=False, verbose_name=_('employer name'))
    position = models.CharField(max_length=100, blank=False, verbose_name=_('pos    ition held'))
    duties = models.TextField(blank=True, verbose_name=_('duties'))
    start_date = models.DateField(verbose_name=_('starting date'))
    end_date = models.DateField(verbose_name=_('ending date'))
    
    def __unicode__(self):
        return self.employer_name


class StudentResearch(models.Model):
    student = models.ForeignKey(StudentProfile, related_name='research')
    field = models.CharField(max_length=100, blank=False, verbose_name=_('field of research'))
    duties = models.TextField(blank=False, verbose_name=_('duties'))
    
    def __unicode__(self):
        return self.field


class MentorshipActivities(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name=_('mentorship activities'))
    description = models.TextField(blank=True, verbose_name=_('activity description'))
    
    def __unicode__(self):
        return self.name


class MentorshipActivities_Mentor(models.Model):
    mentor = models.ForeignKey(MentorProfile, related_name='mentorship_activities')
    activity = models.ForeignKey(MentorshipActivities, related_name='mentor')
    
    
class CommunicationMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    
    def __unicode__(self):
        return self.name
    

class CommunicationRating(models.Model):
    profile = models.ForeignKey(Profile, related_name='communication_ratings')
    ratting = models.IntegerField(default=0, verbose_name=_('ratting'))
    method = models.ForeignKey(CommunicationMethod, related_name='ratings')
    
    def __unicode__(self):
        return self.method.name + '(' + str(self.ratting) + ')' 


def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(create_profile, sender=User)
