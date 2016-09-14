import params

def trans_rect (obj):
    x = obj['geometry']['x']
    y = obj['geometry']['y']
    w = obj['geometry']['width']
    h = obj['geometry']['height']
    obj['geometry']['x'] = y
    obj['geometry']['y'] = x
    obj['geometry']['width'] = h
    obj['geometry']['height'] = w
    pass


def fix_transpose (obj):
    if params.TRANSPOSE:
        if obj['type'] == 'rect':
            trans_rect(obj):
        elif obj['type'] == 'polygon':
            trans_poly(obj):
        elif obj['type'] == 'point':
            trans_point(obj):
        else:
            raise Exception("type %s not supported") % obj['type']
    return obj
