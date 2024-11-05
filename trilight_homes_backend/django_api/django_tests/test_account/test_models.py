from django.test import TestCase
from django.contrib.auth import get_user_model

from trilight_homes_backend.django_api.account.models import RolePermission, User, Profile, LoginHistory, UserPreferences, TwoFactorAuth, ActivityLog

User = get_user_model()

class RolePermissionTestCase(TestCase):
    def test_role_permission_creation(self):
        role = RolePermission.objects.create(
            name="ADMIN",
            description="Full administrative access for managing the platform",
            privilege_level=5
        )
        self.assertEqual(role.name, "ADMIN")
        self.assertEqual(role.description, "Full administrative access for managing the platform")
        self.assertEqual(role.privilege_level, 5)

    def test_role_permission_get_permissions(self):
        role = RolePermission.objects.create(
            name="STAFF",
            description="Full-time employees of the company",
            privilege_level=3
        )
        permissions = role.get_permissions()
        self.assertEqual(permissions, ["view_basic", "view_advanced", "edit"])

class UserTestCase(TestCase):
    def test_user_creation(self):
        role = RolePermission.objects.create(
            name="AGENT",
            description="Field officers who mediate as property marketers",
            privilege_level=2
        )
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            role_permission=role,
            phone_number="+1234567890"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role_permission, role)
        self.assertEqual(user.phone_number, "+1234567890")

    def test_user_get_permissions(self):
        role = RolePermission.objects.create(
            name="BUYER",
            description="Individuals who have purchased property",
            privilege_level=2
        )
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            role_permission=role
        )
        permissions = user.get_user_permissions()
        self.assertEqual(permissions, ["view_basic", "view_advanced"])

class ProfileTestCase(TestCase):
    def test_profile_creation(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        profile = Profile.objects.create(
            user=user,
            bio="This is a test bio",
            email="test@example.com"
        )
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.bio, "This is a test bio")
        self.assertEqual(profile.email, "test@example.com")

class LoginHistoryTestCase(TestCase):
    def test_login_history_creation(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        login_history = LoginHistory.objects.create(
            user=user,
            ip_address="127.0.0.1",
            user_agent="TestUserAgent"
        )
        self.assertEqual(login_history.user, user)
        self.assertEqual(login_history.ip_address, "127.0.0.1")
        self.assertEqual(login_history.user_agent, "TestUserAgent")

class UserPreferencesTestCase(TestCase):
    def test_user_preferences_creation(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        preferences = UserPreferences.objects.create(
            user=user,
            email_notifications=True,
            localized_settings="en-US"
        )
        self.assertEqual(preferences.user, user)
        self.assertTrue(preferences.email_notifications)
        self.assertEqual(preferences.localized_settings, "en-US")

class TwoFactorAuthTestCase(TestCase):
    def test_two_factor_auth_creation(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        two_factor_auth = TwoFactorAuth.objects.create(
            user=user,
            is_enabled=True,
            secret_key="abcd1234",
            backup_codes="123456,789012"
        )
        self.assertEqual(two_factor_auth.user, user)
        self.assertTrue(two_factor_auth.is_enabled)
        self.assertEqual(two_factor_auth.secret_key, "abcd1234")
        self.assertEqual(two_factor_auth.backup_codes, "123456,789012")

class ActivityLogTestCase(TestCase):
    def test_activity_log_creation(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        activity_log = ActivityLog.objects.create(
            user=user,
            activity="Logged in to the system",
            created_by=user
        )
        self.assertEqual(activity_log.user, user)
        self.assertEqual(activity_log.activity, "Logged in to the system")
        self.assertEqual(activity_log.created_by, user)