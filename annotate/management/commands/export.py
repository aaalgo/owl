import os
import sys
import simplejson as json
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from annotate.models import *
import picpac

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('output', nargs=1, help='')
        pass

    @transaction.atomic
    def handle(self, *args, **options):
        #hours = options['hours'] + 24 * options['days']
        #check_and_import(hours, not options['run'], options['check'])
        output = options['output'][0]
        all = {}
        for anno in Annotation.objects.all():
            shapes = all.setdefault(anno.image, {"shapes":[]})["shapes"].append(json.loads(anno.anno)["shapes"][0])
            pass
        if os.path.exists(output):
            os.remove(output)
        pp = picpac.Writer(output)
        for image, anno in all.iteritems():
            with open(image.path, 'r') as f:
                buf = f.read()
            pp.append(buf, json.dumps(anno))
            print anno
        pass

