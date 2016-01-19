from __future__ import unicode_literals

import base64

from django.conf import settings
from django.db import models


class CondensedUrl(models.Model):
    """
    Model that represents a condensed URL.

    TODO Need to look into how MySQL deals with VARCHAR fields and mixed case
    """
    original_url = models.URLField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    #visited_count = models.IntegerField(default=0)

    def condensed_url(self):
        """
        Returns a condensed url.

        :returns: A base64 encoded string that is url-safe
        :rtype: str
        """
        return base64.urlsafe_b64encode(str(self.id))
