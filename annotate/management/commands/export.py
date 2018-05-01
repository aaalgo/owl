import os
import sys
import simplejson as json
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from annotate.models import *
from annotate.utils import fix_transpose
import picpac
print(picpac.__file__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('output', nargs=1, help='')
        parser.add_argument('--all', action='store_true', help='foo help')
        pass

    @transaction.atomic
    def handle(self, *args, **options):
        #hours = options['hours'] + 24 * options['days']
        #check_and_import(hours, not options['run'], options['check'])
        output = options['output'][0]
        all = {}
        if options['all']:
            for image in Image.objects.filter(viewed=True):
                all[image] =  {"shapes":[]}
                pass
        for anno in Annotation.objects.all():
            shapes = all.setdefault(anno.image, {"shapes":[]})["shapes"].append(fix_transpose(json.loads(anno.anno)["shapes"][0]))
            pass
        if os.path.exists(output):
            os.remove(output)
        pp = picpac.Writer(output, picpac.OVERWRITE)
        for image, anno in all.items():
            with open(image.path, 'rb') as f:
                buf = f.read()
            pp.append(0, buf, json.dumps(anno).encode('ascii'))
            print(anno)
        pass

