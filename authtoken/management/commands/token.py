from authtoken.models import Authtoken

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = 'Generates a new token for authenticating client requests.'

    def get_version(self):
        return '1.0.0'

    def handle(self, *args, **options):

        try:

            print('Generating new authtoken...', end=' ')

            try:
                old_token: Authtoken = Authtoken.objects.filter(valid=True)[0]
                key: str = old_token.gensen_new_token()
            except IndexError:
                try:
                    user: User = User.objects.filter(is_superuser=True)[0]
                    key: str = Authtoken.gen_key(user)
                    Authtoken.objects.create(key=key, user=user)
                except ObjectDoesNotExist:
                    raise CommandError('Create a superuser first.')

            print('done. Write this down somewhere safe -> ')

            self.stdout.write(self.style.SUCCESS(f'Key: {key}'))

        except Exception as e:
            raise CommandError(str(e))
