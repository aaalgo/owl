import os
import hashlib
import mimetypes
import simplejson as json
import logging
import subprocess
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from annotate.models import *
from annotate import params

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def signature (image, annotation):
    geo = annotation['shapes'][0]['geometry']
    sig = '%s:%s' % (image.id, json.dumps(geo))
    sig = sig[:250]
    print("SIG:%s" % sig)
    return sig

logger = logging.getLogger(__name__)

def image (request, key):
    image = Image.objects.get(pk = int(key))
    path = image.path
    if params.TRANSPOSE:
        path = 'trans/%s.jpg' % hashlib.sha1(image.path).hexdigest()
        if not os.path.exists(path):
            subprocess.check_call('convert %s -transpose %s' % (image.path, path), shell=True)
    mime = mimetypes.guess_type(path)
    data = open(path, 'rb').read()
    return HttpResponse(data, content_type = mime)

def fix_anno (txt):
    x = json.loads(txt)
    del x['context']
    del x['shapes'][0]['style']
    key = x['key']
    #del x['key']
    x['src'] = reverse('image', args=[key])
    return json.dumps(x)

def anno_base (request, images):
    n_total = Image.objects.count()
    if params.VIEWED_AS_DONE:
        n_done = Image.objects.filter(viewed = True).count()
    else:
        n_done = Image.objects.filter(done = True).count()
    annotations = Annotation.objects.filter(deleted = False, image__in = images)
    todo = [x.id for x in images]
    annos = [fix_anno(x.anno) for x in annotations]
    context = {'jobs': list(chunks(todo, params.COLS)),
               'shape': params.SHAPE,
               'total': n_total,
               'done': n_done,
               'todo': n_total - n_done,
               'annos': annos,
               'show_check': params.SHOW_CHECK,
              }
    return render(request, 'annotate/anno.html', context)

def anno (request):
    images = []
    for trial in range(2):
        images = Image.objects.filter(done = False, viewed = False).order_by('id')[:params.BATCH]
        if params.VIEWED_AS_DONE or len(images) > 0 or trial > 0:
            break
        # if we have viewed everything, then restart
        Image.objects.filter(done = False, viewed = True).update(viewed = False)
        pass
    R = anno_base(request, images)
    Image.objects.filter(pk__in = images).update(viewed = True)
    return R

def review (request, key):
    images = Image.objects.filter(pk = int(key))
    return anno_base(request, images)

METHOD_MAP = {key: value for (value, key) in Log.METHOD_CHOICES}

def log (request):
    data = json.loads(request.body)
    method = METHOD_MAP.get(data['method'].upper(), -1)
    assert method >= 0
    anno = data['annotation']
    print(method, anno)
    key = int(anno["key"])
    image = Image.objects.get(pk = key)
    sig = signature(image, anno)
    anno_json = json.dumps(anno)
    log = Log.objects.create(image = image,
                             method = method,
                             anno = anno_json,
                             ip_address = request.META.get('REMOTE_ADDR'))
    if method == Log.CREATE:
        Annotation.objects.create(signature = sig, 
                                  image = image,
                                  anno = anno_json,
                                  log = log)
        image.done = True
        image.save()
    elif method == Log.UPDATE:
        r = Annotation.objects.get(pk = sig)
        r.anno = anno_json
        r.log = log
        r.save()
    elif method == Log.DELETE:
        r = Annotation.objects.get(pk = sig)
        r.delete()
    else:
        assert False
    return HttpResponse(json.dumps({}), content_type="application/json")


