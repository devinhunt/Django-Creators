import sys, urllib, json
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from creators.models import Status, Room

class Command(BaseCommand):
    args = ''
    help = 'Grabs the latest statuses from the mobile server'

    def handle(self, *args, **options):
        latest_status = Status.objects.all().order_by("-pk")[0]
<<<<<<< HEAD:src/creators/management/commands/grab.py
        print latest_status.pk
	stupid_time = latest_status.created - timedelta(hours = 5)
=======
        print latest_status
>>>>>>> 7fbbcbe2387b2c0fe1760fabbde856e96a645f3c:src/creators/management/commands/grab.py
        time_string = latest_status.created.strftime('%Y-%m-%d %H:%M:%S')
        time_date = stupid_time.strftime('%Y-%m-%d') + '%20' + stupid_time.strftime('%H:%M:%S')
        status_url = "http://at.thecreatorsproject.com/party/interface.php?type=list_all_users&by_time=" + time_date
        print status_url
        status_ref = urllib.urlopen(status_url)
        status_objs = json.load(status_ref)
                
        if status_objs:
            for s_obj in status_objs:
		print s_obj
                if s_obj['status']:
                    status = Status(status = s_obj['status'], created = datetime.utcnow(), user = s_obj['username'], room = Room.objects.all()[0])
                    print status
                    status.save()
