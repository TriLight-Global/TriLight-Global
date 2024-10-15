from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# # Create your models here.
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True)
#     preferred_contact_method = models.CharField(_("Preferred Contact Method"), max_length=20)
#     saved_searches = models.JSONField(_("Saved Searches"), default=list)
#     notifications = models.JSONField(_("Notifications"), default=list)

#     def __str__(self):
#         return f"Profile for {self.user.username}"



# Users:
# Visitors - unregistered users/anonymous
# Superusers - admins
# Registered users: 
# Staff (recruited members)
# Engineers & contractors
# Marketers
# Agents
# Agency
# Tenants
# Partners

class User(AbstractUser):
    ROLES = (
        ('VISITOR', 'Visitor'),
        ('REGISTERED', 'Registered User'),
        ('AGENT', 'Agent'),
        ('OWNER', 'Property Owner'),
        ('DEVELOPER', 'Developer'),
        ('ADMIN', 'Admin')
    )
    role = models.CharField(max_length=20, choices=ROLES, default='VISITOR')
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(_("Bio"), blank=True)
    profile_picture = models.ImageField(_("Profile Picture"), upload_to='agent_profiles/', blank=True)
    agency = models.ForeignKey('Agency', on_delete=models.SET_NULL, null=True, blank=True, related_name='agents')
    ratings = models.SmallIntegerField(null=True)
    verification_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()

class Agency(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    logo = models.ImageField(_("Logo"), upload_to='agency_logos/', blank=True)
    website = models.URLField(_("Website"), blank=True)

    def __str__(self):
        return self.name

# class Task(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     status = models.CharField(max_length=20)
#     due_date = models.DateField()

