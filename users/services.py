from .dtos import UserDTO
from django.contrib.auth.models import User as AuthUser
from .models import UserQuota
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta, date
from rest_framework.permissions import AllowAny


class UserService:
    permission_classes = [AllowAny]

    def signup(self, email, password, first_name, last_name):

        if not email or not password or not first_name or not last_name:
            raise ValueError("All fields are required")

        # check if email already exists
        if AuthUser.objects.filter(email=email).exists():
            raise ValueError("Email already exists")

        # save user to database
        user = AuthUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.save()

        # return user dto
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )

    def login(self, email, password, is_remembered=False):

        permission_classes = [AllowAny]

        if not email or not password:
            raise ValueError("Email and password are required")

        user = authenticate(username=email, password=password)
        if user is None:
            raise ValueError("Invalid credentials")

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        if is_remembered:
            refresh_token.set_exp(lifetime=timedelta(days=60))
            access_token.set_exp(lifetime=timedelta(days=30))
        else:
            refresh_token.set_exp(lifetime=timedelta(days=10))
            access_token.set_exp(lifetime=timedelta(hours=8))

        return {
            'refresh': str(refresh_token),
            'access': str(access_token),
            'user': UserDTO(
                id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name
            )
        }


class UserQuotaService:

    def __init__(self, user):
        self.user = user

    def create_quota(self, max_minutes=60):
        if not self.user:
            raise ValueError("User is required to create a quota")

        # Check if quota already exists
        if UserQuota.objects.filter(user=self.user).exists():
            raise ValueError("User quota already exists")

        # Create a new quota for the user
        quota = UserQuota.objects.create(
            user=self.user,
            max_minutes=max_minutes,
            used_minutes=0,
            reset_date=date.today()
        )
        return quota

    def get_quota(self):
        try:
            quota = UserQuota.objects.get(user=self.user)
            return quota
        except UserQuota.DoesNotExist:
            return None

    def update_quota(self, used_minutes):
        quota = self.get_quota()
        if not quota:
            raise ValueError("User quota does not exist")

        quota.used_minutes += used_minutes
        if quota.used_minutes > quota.max_minutes:
            raise ValueError("Quota exceeded")

        quota.save()
        return quota

    def reset_quota(self):
        quota = self.get_quota()
        if not quota:
            raise ValueError("User quota does not exist")

        quota.used_minutes = 0
        quota.reset_date = date.today()
        quota.save()
        return quota
