from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

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
