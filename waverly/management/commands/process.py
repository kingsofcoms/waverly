from django.core.management.base import BaseCommand, CommandError
from waverly.models import Podcast, User, Event
import time

class Command(BaseCommand):
    help = 'Processes a url to get article content and details, and converting text to speech'
    # self.stdout.write("👾  executing Command (process.py)")
    print ("💻  executing Command (process.py)")

    # def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # for poll_id in options['poll_id']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()
        print ('🌈  processing podcast 1/3 [this process should have happened in the background]')
        time.sleep(2)
        print ('🌈  processing podcast 2/3 [this process should have happened in the background]')
        time.sleep(2)
        print ('🌈  processing podcast 3/3 [this process should have happened in the background]')

        self.stdout.write(self.style.SUCCESS('🌈  🌈  🌈  Successfully executed command'))
