from .models import MyUser


class InstagramBackend():
    def authenticate(self, instagram_id, extra_fields):

        print('extra_fields:{}'.format(extra_fields))

        defaults = {
            'username': extra_fields.get('username', ''),
        }
        print('defaults:{}'.format(defaults))

        user, user_created = MyUser.objects.get_or_create(
            username=instagram_id,
            defaults=defaults
        )
        print('user:{} user_created:{}'.format(user, user_created))
        return user

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None
