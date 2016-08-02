import sys
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from annotate.models import *

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--run', action='store_true', default=False, help='')
        pass

    @transaction.atomic
    def handle(self, *args, **options):
        #hours = options['hours'] + 24 * options['days']
        #check_and_import(hours, not options['run'], options['check'])
        run = options['run']
        for line in sys.stdin:
            fs = line.strip().split('\t')
            if len(fs) == 1:
                path = fs[0]
                meta = path
            elif len(fs) == 2:
                path, meta  = fs
            else:
                raise Exception("bad line: %s" % line)
            if run:
                Image.objects.create(path = path, meta = meta)
            else:
                print path, meta
                pass
            pass
        pass

