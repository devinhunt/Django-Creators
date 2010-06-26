import sys, urllib, json
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from creators.models import Status, Room

class Command(BaseCommand):
    args = ''
    help = 'Grabs the latest statuses from the mobile server'

    def handle(self, *args, **options):
        latest_status = Status.objects.all().order_by("-pk")[0]
        time_string = latest_status.created.strftime('%Y-%m-%d %H:%M:%S')
        status_url = "http://at.thecreatorsproject.com/party/interface.php?type=list_all_users&by_time=" + time_string
        print status_url
        status_ref = urllib.urlopen(status_url)
        status_objs = json.load(status_ref)
        
        
        
        if status_objs:
            for s_obj in status_objs:
                if s_obj['status']:
                    status = Status(status = s_obj['status'], created = datetime.today(), user = s_obj['username'], room = Room.objects.all()[0])
                    print status
                    status.save()