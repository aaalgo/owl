import hashlib
import mimetypes
import simplejson as json
import logging
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from models import *
import params

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def signature (image, annotation):
    return str(image.id)

logger = logging.getLogger(__name__)

def image (request, key):
    image = Image.objects.get(pk = int(key))
    mime = mimetypes.guess_type(image.path)
    data = open(image.path, 'r').read()
    return HttpResponse(data, content_type = mime)

def anno (request):
    template = loader.get_template('annotate/test.html')
    todo = []
    n_total = Image.objects.count()
    n_done = Image.objects.filter(done = True).count()
    for trial in range(2):
        found = Image.objects.filter(done = False, viewed = False).order_by('id')[:params.BATCH]
        todo = [x.id for x in found]
        Image.objects.filter(pk__in = found).update(viewed = True)
        if len(todo) > 0 or trial > 0:
            break
        # if we have viewed everything, then restart
        Image.objects.filter(done = False, viewed = True).update(viewed = False)
        pass
    context = {'jobs': list(chunks(todo, params.COLS)),
               'polygon': params.POLYGON,
               'total': n_total,
               'done': n_done,
               'todo': n_total - n_done
              }
    print todo
    return render(request, 'annotate/test.html', context)

METHOD_MAP = {key: value for (value, key) in Log.METHOD_CHOICES}



def log (request):
    data = json.loads(request.body)
    method = METHOD_MAP.get(data['method'].upper(), -1)
    assert method >= 0
    anno = data['annotation']
    key = int(anno["key"])
    image = Image.objects.get(pk = key)
    sig = signature(image, anno)
    log = Log.objects.create(image = image,
                             method = method,
                             anno = anno,
                             ip_address = request.META.get('REMOTE_ADDR'))
    if method == Log.CREATE:
        Annotation.objects.create(signature = sig, 
                                  image = image,
                                  anno = anno,
                                  log = log)
        image.done = True
        image.save()
    elif method == Log.UPDATE:
        r = Annotation.objects.get(pk = sig)
        r.anno = anno
        r.log = log
        r.save()
    elif method == Log.DELETE:
        r = Annotation.objects.get(pk = sig)
        r.deleted = True
        r.log = log
        r.save()
    else:
        assert False
    print method, anno
    return HttpResponse(json.dumps({}), content_type="application/json")


