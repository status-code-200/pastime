from accounts.models import CustomizedUser


class SettingsBackend(object):
    '''
    Custom implementation of auth backend.
    username field can be as either a username or email
    '''
    def authenticate(self, username=None, password=None):
        '''
        Username field can be as either a username or email.
        Case insensitive comparison of username or email
        :param password:
        :param username:
        '''
        try:
            if '@' in username:
                user = CustomizedUser.objects.get(email__iexact=username)
            else:
                user = CustomizedUser.objects.get(username__iexact=username)

            if user.check_password(password):
                return user

        except CustomizedUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomizedUser.objects.get(pk=user_id)
        except CustomizedUser.DoesNotExist:
            return None
