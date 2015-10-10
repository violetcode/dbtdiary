#!/usr/bin/python

from django.core.management.base import NoArgsCommand
from dbtdiary.diary.models import *
import datetime
from django.utils import timezone

class Command(NoArgsCommand):
    help = "Run a script to mark users inactive."

    def handle_noargs(self, **options):
        now = timezone.now()
        days_ago = datetime.timedelta(days=30)
        past = now - days_ago
        users = User.objects.all()
        active_count = 0
        inactive_count = 0
        for user in users:
            profile = UserProfile.objects.get_or_create(user=user)[0]
            if user.last_login > past or user.is_staff:
                profile.active = True
                active_count += 1
            else:
                print "User {0} is inactive.".format(user.username)
                profile.active = False
                inactive_count += 1
            profile.save()
        print "Active: {0}".format(active_count)
        print "Inactive: {0}".format(inactive_count)
