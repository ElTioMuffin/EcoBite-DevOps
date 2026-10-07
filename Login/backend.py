from django.contrib.auth.backends import BaseBackend
from .models import Users
import logging

logger = logging.getLogger(__name__)

class UsersEmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by email instead of username.
        Returns User object if credentials are valid, None otherwise.
        """
        if username is None or password is None:
            return None
            
        try:
            user = Users.objects.get(email=username.lower())
            if user.check_password(password):
                return user
            else:
                # Password is incorrect
                logger.warning(f"Failed login attempt for email: {username}")
                return None
                
        except Users.DoesNotExist:
            # User does not exist
            logger.warning(f"Login attempt for non-existent email: {username}")
            return None
        except Exception as e:
            # Catch any other unexpected errors
            logger.error(f"Unexpected error during authentication: {str(e)}")
            return None
    
    def get_user(self, user_id):
        """
        Get user by primary key.
        Returns User object if found, None otherwise.
        """
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            logger.warning(f"User with id {user_id} does not exist")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting user: {str(e)}")
            return None