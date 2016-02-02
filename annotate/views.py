from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import simplejson as json
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def index (request):
    template = loader.get_template('annotate/test.html')
    context = {}
    return render(request, 'annotate/test.html', context)

def log (request):
    data = json.loads(request.body)
    method = data['method']
    anno = data['annotation']
    print method, anno
    return HttpResponse(json.dumps({}), content_type="application/json")

