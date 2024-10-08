# This file is placed in the Public Domain.
# pylint: disable=R,W0105


"a clean namespace"


import json


class Object:

    "Object"

    def __contains__(self, key):
        return key in dir(self)

    def __getstate__(self):
        "no pickle."

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __oid__(self):
        return 1

    def __str__(self):
        return str(self.__dict__)


"default"


class Default(Object):

    "Default"

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


"methods"


def construct(obj, *args, **kwargs):
    "construct an object from provided arguments."
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(obj, dict(val))
        elif isinstance(val, dict):
            update(obj, val)
        elif isinstance(val, Object):
            update(obj, vars(val))
    if kwargs:
        update(obj, kwargs)


def edit(obj, setter, skip=False):
    "edit an object from provided dict/dict-like."
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            setattr(obj, key, int(val))
            continue
        except ValueError:
            pass
        try:
            setattr(obj, key, float(val))
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            setattr(obj, key, True)
        elif val in ["False", "false"]:
            setattr(obj, key, False)
        else:
            setattr(obj, key, val)


def fmt(obj, args=None, skip=None, plain=False):
    "format an object to a printable string."
    if args is None:
        args = keys(obj)
    if skip is None:
        skip = []
    txt = ""
    for key in args:
        if key.startswith("__"):
            continue
        if key in skip:
            continue
        value = getattr(obj, key, None)
        if value is None:
            continue
        if plain:
            txt += f"{value} "
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt += f'{key}="{value}" '
        else:
            txt += f"{key}={value} "
    return txt.strip()


def fqn(obj):
    "return full qualified name of an object."
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def items(obj):
    "return the items of an object."
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    "return keys of an object."
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def matchkey(obj, txt):
    "check if object has matching keys."
    for key in keys(obj):
        if txt in key:
            yield key


def match(obj, selector):
    "do an exact match on the selector's values."
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            res = False
            break
        if value == val:
            res = True
        else:
            res = False
            break
    return res


def search(obj, selector):
    "check if object matches provided values."
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            continue
        if str(value).lower() in str(val).lower():
            res = True
        else:
            res = False
            break
    return res


def update(obj, data, empty=True):
    "update an object."
    for key, value in items(data):
        if empty and not value:
            continue
        setattr(obj, key, value)


def values(obj):
    "return values of an object."
    return obj.__dict__.values()


"decoder"


class ObjectDecoder(json.JSONDecoder):

    "ObjectDecoder"

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None):
        "decoding string to object."
        val = json.JSONDecoder.decode(self, s)
        if not val:
            val = {}
        return hook(val)

    def raw_decode(self, s, idx=0):
        "decode partial string to object."
        return json.JSONDecoder.raw_decode(self, s, idx)


def hook(objdict, typ=None):
    "construct object from dict."
    if typ:
        obj = typ()
    else:
        obj = Object()
    construct(obj, objdict)
    return obj


def load(fpt, *args, **kw):
    "load object from file."
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.load(fpt, *args, **kw)


def loads(string, *args, **kw):
    "load object from string."
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


"encoder"


class ObjectEncoder(json.JSONEncoder):

    "ObjectEncoder"

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, o):
        "return stringable value."
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
            return o
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            try:
                return o.__dict__
            except AttributeError:
                return repr(o)

    def encode(self, o) -> str:
        "encode object to string."
        return json.JSONEncoder.encode(self, o)

    def iterencode(self, o, _one_shot=False):
        "loop over object to encode to string."
        return json.JSONEncoder.iterencode(self, o, _one_shot)


def dump(*args, **kw):
    "dump object to file."
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def dumps(*args, **kw):
    "dump object to string."
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


"interface"


def __dir__():
    return (
        'Default',
        'Object',
        'construct',
        'dump',
        'dumps',
        'edit',
        'fmt',
        'fqn',
        'hook',
        'load',
        'loads'
        'items',
        'keys',
        'load',
        'loads',
        'match',
        'matchkey',
        'search',
        'update',
        'values'
    )
