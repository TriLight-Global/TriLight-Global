"""
This module defines custom user models and related entities for a property management system using Django.
It includes role permissions, user preferences, login history, profile details, and two-factor authentication settings.
These models facilitate user management, access control, and secure authentication within the application.

Key Components:
- RolePermission: Defines roles with associated permissions.
- User: Extends Django's AbstractUser to include role permissions and additional fields.
- Profile: Stores extra profile information linked to users.
- LoginHistory: Tracks user login activities for security auditing.
- UserPreferences: Manages user-specific notification and localization settings.
- TwoFactorAuth: Handles two-factor authentication for enhanced account security.
- UserActivity: Contains details specific to property agents, including their assigned properties.
"""

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


# Role definitions with role name, description, and privilege level
ROLES = (
    ('VISITOR', 'Visitor', 'General visitors with read-only access', 1),
    ('CONTRACTOR', 'Contractor', 'Temporary workers on contract with the company', 2),
    ('AGENT', 'Agent', 'Field officers who mediate as property marketers', 2),
    ('STAFF', 'Staff', 'Full-time employees of the company', 3),
    ('BUYER', 'Property Buyer', 'Individuals who have purchased property', 2),
    ('TENANT', 'Tenant', 'Individuals residing in properties managed by the company', 3),
    ('SHAREHOLDER', 'Shareholder', 'Company shareholders with restricted access', 3),
    ('BOARD_MEMBER', 'Board Member', 'Board members with high-level access', 4),
    ('ADMIN', 'Admin', 'Full administrative access for managing the platform', 5),
)


class RolePermission(models.Model):
    """Defines a role with a name, description, and privilege level."""
    
    ROLE_CHOICES = [(role[0], role[1]) for role in ROLES]  # Extracts role names as choices

    name = models.CharField(_("Role Name"), max_length=100, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(_("Role Description"))
    privilege_level = models.IntegerField(_("Privilege Level"), choices=[(i, f"Level {i}") for i in range(1, 6)], default=1)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date and time on creation
    created_by = models.ForeignKey(
        get_user_model(),  # Uses the custom User model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_roles',
        verbose_name=_("Created By")
    )

    def __str__(self):
        return f"{self.get_name_display()} (Level {self.privilege_level})"

    @staticmethod
    def initialize_roles():
        """Populates RolePermission with initial roles and privilege levels from ROLES."""
        for code, name, description, level in ROLES:
            RolePermission.objects.get_or_create(
                name=code,
                defaults={'description': description, 'privilege_level': level}
            )

    def get_permissions(self):
        """Returns a list of permissions based on the role's privilege level."""
        PERMISSION_LEVELS = {
            1: ["view_basic"],
            2: ["view_basic", "view_advanced"],
            3: ["view_basic", "view_advanced", "edit"],
            4: ["view_basic", "view_advanced", "edit", "manage"],
            5: ["view_basic", "view_advanced", "edit", "manage", "administer"],
        }
        return PERMISSION_LEVELS.get(self.privilege_level, [])


class User(AbstractUser):
    """Custom User model with a foreign key to RolePermission for role-based access control."""
    
    role_permission = models.ForeignKey(RolePermission, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    phone_number = models.CharField(max_length=20, blank=True, validators=[RegexValidator(r'^\+?1?\d{9,15}$', _('Invalid phone number'))])
    alternate_phone_number = models.CharField(_("Alternate Phone Number"), max_length=20, blank=True, validators=[RegexValidator(r'^\+?1?\d{9,15}$', _('Invalid phone number'))])
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date and time on creation
    created_by = models.ForeignKey(
        get_user_model(),  # Uses the custom User model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users',
        verbose_name=_("Created By")
    )

    def __str__(self):
        return f"{self.username} ({self.role_permission.name if self.role_permission else 'No Role'})"

    def get_user_permissions(self):
        """Retrieve permissions based on user's role."""
        return self.role_permission.get_permissions() if self.role_permission else []


class Profile(models.Model):
    """Model to store additional profile details linked to the User model."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Links additional profile details to the main user account
    bio = models.TextField(_("Bio"), blank=True)  # Bio to provide background information
    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)  # Records date of birth
    email = models.EmailField(_("Email"), blank=True)  # Primary contact email for notifications and account updates
    house_number = models.CharField(_("House Number"), max_length=20, blank=True)  # Location fields for contact and address records
    street = models.CharField(_("Street Name"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    state = models.CharField(_("State"), max_length=100, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True)
    country = models.CharField(_("Country"), max_length=100, blank=True)
    secondary_email = models.EmailField(_("Secondary Email"), blank=True)  # Provides backup email contact
    occupation = models.CharField(_("Occupation"), max_length=100, blank=True)
    company = models.CharField(_("Company Name"), max_length=100, blank=True)
    work_address = models.TextField(_("Work Address"), blank=True)
    linkedin_profile = models.URLField(_("LinkedIn Profile"), blank=True)
    twitter_profile = models.URLField(_("Twitter Profile"), blank=True)
    facebook_profile = models.URLField(_("Facebook Profile"), blank=True)
    emergency_contact_name = models.CharField(_("Emergency Contact Name"), max_length=100, blank=True)
    emergency_contact_relationship = models.CharField(_("Relationship"), max_length=50, blank=True)
    emergency_contact_phone = models.CharField(_("Emergency Contact Phone"), max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date and time on creation
    created_by = models.ForeignKey(
        get_user_model(),  # Uses the custom User model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_profiles',
        verbose_name=_("Created By")
    )

    def __str__(self):
        return f"Profile for {self.user.username}"


class LoginHistory(models.Model):
    """Model to track user login history for security and auditing purposes."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')  # Tracks user login history
    login_datetime = models.DateTimeField(auto_now_add=True)  # Timestamp of login
    ip_address = models.GenericIPAddressField()  # Records IP address
    user_agent = models.TextField()  # Information on user device
    device_type = models.CharField(max_length=50, blank=True)  # Optional device type field
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date and time on creation
    created_by = models.ForeignKey(
        get_user_model(),  # Uses the custom User model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_login_history',
        verbose_name=_("Created By")
    )


class UserPreferences(models.Model):
    """Model to capture user preferences."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')  # User's notification preferences
    email_notifications = models.BooleanField(default=True)  # Email notifications preference
    localized_settings = models.CharField(max_length=50, blank=True)  # User-specific localization settings
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    preferred_locations = models.JSONField()
    preferred_property_types = models.JSONField()
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    min_bedrooms = models.PositiveIntegerField(null=True, blank=True)
    min_bathrooms = models.PositiveIntegerField(null=True, blank=True)
    preferred_amenities = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date and time on creation
    created_by = models.ForeignKey(
        get_user_model(),  # Uses the custom User model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_preferences',
        verbose_name=_("Created By")
    )


class TwoFactorAuth(models.Model):
    """Model to manage two-factor authentication settings for users."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='two_factor_auth')  # Ties two-factor auth settings to the user
    is_enabled = models.BooleanField(default=False)  # Indicates if 2FA is enabled
    secret_key = models.CharField(max_length=64, blank=True)  # Stores the secret key for 2FA
    backup_codes = models.TextField(blank=True)  # Stores backup codes for user access
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date and time on creation
    created_by = models.ForeignKey(
        get_user_model(),  # Uses the custom User model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_two_factor_auth',
        verbose_name=_("Created By")
    )

    def __str__(self):
        return f"2FA settings for {self.user.username}"

class ActivityLog(models.Model):
    """Model to record activities performed by users in the system.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    activity = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_activity_logs',
        verbose_name=_("Created By")
    )

    def __str__(self):
        return f"{self.user.username} - {self.activity} at {self.timestamp}"

