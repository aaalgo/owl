import sys
import simplejson as json
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from annotate.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        for anno in Annotation.objects.all():
            a = json.loads(anno.anno)["shapes"][0]["geometry"]
            print "%s\t%g\t%g\t%g\t%g" %(anno.image.meta, a["x"], a["y"], a["width"], a["height"])
        #hours = options['hours'] + 24 * options['days']
        #check_and_import(hours, not options['run'], options['check'])

        pass

