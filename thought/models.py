import typing

from django.db import models


class Thought(models.Model):
    body = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self) -> typing.Dict[str, str]:

        date = self.timestamp.strftime('%b. %d, %Y')
        time = self.timestamp.strftime('%-I:%M')

        am_pm = self.timestamp.strftime('%p').lower()
        am_pm = ''.join(i + '.' for i in am_pm)

        return {
            'pk': self.pk,
            'body': self.body,
            'timestamp': f"{date} at {time} {am_pm}"
        }

    class Meta:
        ordering = ('-timestamp', '-pk')

    def __str__(self):
        return self.timestamp.ctime()
