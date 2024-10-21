# Account

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(_("Bio"), blank=True)
    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    street_address = models.CharField(_("Street Address"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    state = models.CharField(_("State"), max_length=100, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True)
    country = models.CharField(_("Country"), max_length=100, blank=True)
    secondary_email = models.EmailField(_("Secondary Email"), blank=True)
    alternate_phone_number = models.CharField(_("Alternate Phone Number"), max_length=20, blank=True)
    occupation = models.CharField(_("Occupation"), max_length=100, blank=True)
    company = models.CharField(_("Company Name"), max_length=100, blank=True)
    work_address = models.TextField(_("Work Address"), blank=True)
    linkedin_profile = models.URLField(_("LinkedIn Profile"), blank=True)
    twitter_profile = models.URLField(_("Twitter Profile"), blank=True)
    facebook_profile = models.URLField(_("Facebook Profile"), blank=True)
    emergency_contact_name = models.CharField(_("Emergency Contact Name"), max_length=100, blank=True)
    emergency_contact_relationship = models.CharField(_("Relationship"), max_length=50, blank=True)
    emergency_contact_phone = models.CharField(_("Emergency Contact Phone"), max_length=20, blank=True)

class Role(models.Model):
    name = models.CharField(_("Role Name"), max_length=100, unique=True)
    description = models.TextField(_("Role Description"))

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)

class Permission(models.Model):
    name = models.CharField(_("Permission Name"), max_length=100, unique=True)
    description = models.TextField(_("Permission Description"))

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    login_datetime = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_resets')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')

class TwoFactorAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='two_factor_auth')
    is_enabled = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=100, blank=True)
    backup_codes = models.JSONField(default=list)

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

class SocialAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    provider = models.CharField(max_length=50)
    uid = models.CharField(max_length=100)
    extra_data = models.JSONField(default=dict)

class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_type = models.CharField(max_length=50)
    device_token = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(auto_now=True)

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(_("Bio"), blank=True)
    profile_picture = models.ImageField(_("Profile Picture"), upload_to='agent_profiles/', blank=True)
    agency = models.ForeignKey('Agency', on_delete=models.SET_NULL, null=True, blank=True, related_name='agents')
    ratings = models.SmallIntegerField(null=True)
    verification_status = models.BooleanField(default=False)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)

class Agency(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    logo = models.ImageField(_("Logo"), upload_to='agency_logos/', blank=True)
    website = models.URLField(_("Website"), blank=True)
    description = models.TextField(blank=True)
    year_established = models.PositiveIntegerField(null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True)

class AgentSpecialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class AgentSpecializationAssignment(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='specializations')
    specialization = models.ForeignKey(AgentSpecialization, on_delete=models.CASCADE)



