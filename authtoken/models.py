import struct
import hashlib
import datetime

from django.db import models
from django.contrib.auth.models import User


class Authtoken(models.Model):
    """
    A secret token generated securely only generated
    for the admin's use to help in authenticating
    client side (be it app or website) requests to
    perform CRUD operations.

    At a given time, only one token can be valid
    which is why the uniqueness check is present
    in the `valid` boolean attribute. The last
    generated token should be the valid one.

    To generate a new token, one needs to retrieve
    the last token generated and call the
    `generate_new_token` method. It will automatically
    generate a new secure key, invalidate the
    last authtoken, and make the newly created token
    the de facto valid one. I'm not sure if this
    design is a good one but since it works,
    I won't try to fix it. Improvements might be expected.
    """

    # The key is a 64 character long hexdigest
    # derived from the current timestamp and the
    # timestamp of the User instance when it was
    # created. This number is then passed in as
    # bytes to hashlib's sha256 function to
    # obtain the final digest.
    key = models.CharField(max_length=64, unique=True)

    # A way to derive a new key from the
    # previous timestamp was considered but
    # it doesn't make much sense and this
    # attribute is just to store previous
    # (invalid) Authtoken instances so that
    # if a client requests contains an old
    # key, an helpful error like "this key
    # expired N months ago", would be cool.
    # But that's still in progress.
    timestamp = models.DateTimeField(auto_now_add=True)

    # Only one Authtoken instance at a time
    # can be valid - the last one created.
    valid = models.BooleanField(default=True)

    # Kind of a stupid attribute but necessary
    # nevertheless since it's a good way to
    # check if the superuser is logged in the
    # website and accessing the token that way -
    #   {% if request.user.is_superuser %}
    #       localStorage.setItem('key', {{ request.user.authtoken.key }})
    #   {% else %}
    #       localStorage.clear()
    #   {% endif %}
    # And it also helps in the gensen_new_token
    # function to access the User without making
    # an queries to the database to get the superuser.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authtoken')

    @staticmethod
    def gen_key(user: User) -> str:
        # generate a 'random'-ish number
        delta = datetime.datetime.now().timestamp() + user.date_joined.timestamp()

        # convert the float from datetimes' timestamp to bytes and get its sha256 digest
        b = struct.pack('f', delta)
        key = hashlib.sha256(b).hexdigest()

        return key

    def __str__(self):
        return self.timestamp.ctime() + ' : ' + ('VALID' if self.valid else 'INVALID')

    def gensen_new_token(self) -> str:
        """
        Generates and sets new token. Key is derived
        from internal static method _gen_key method.
        Any previous token is made invalid and a new
        default auth token is set with valid as True.
        """

        # get token
        key = self.gen_key(self.user)

        # make this (self and second last) token invalid
        self.valid = False
        self.save()

        # create new valid authtoken model
        Authtoken.objects.create(key=key, user=self.user)

        return key
