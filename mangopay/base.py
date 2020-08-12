import six

from copy import deepcopy

from .fields import PrimaryKeyField, FieldDescriptor, Field, ForeignRelatedObject
from .query import UpdateQuery, InsertQuery, SelectQuery
from .signals import pre_save, post_save
from .utils import force_text, force_str
from . import get_default_handler


class DoesNotExist(Exception):
    pass


class BaseModelOptions(object):
    def __init__(self, model_class, options=None):
        self.rel_fields = {}
        self.fields = {}
        self.api_names = {}
        self.options = options or {}
        self.reverse_relations = {}
        self.defaults = {}

        for k, v in self.options.items():
            setattr(self, k, v)

        self.model_class = model_class

    def get_sorted_fields(self):
        return sorted(self.fields.items(), key=lambda k, v: (k == self.pk_name and 1 or 2, v._order))

    def get_field_names(self):
        return [f[0] for f in self.get_sorted_fields()]

    def get_fields(self):
        return [f[1] for f in self.get_sorted_fields()]

    def get_field_by_name(self, name):
        if name in self.fields:
            return self.fields[name]
        raise AttributeError('Field named %s not found' % name)

    def __contains__(self, k):
        return k in self.options

    def __setitem__(self, k, value):
        self.options[k] = value

    def __delitem__(self, k):
        if k not in self.options:
            raise KeyError('%s does not exists' % k)

        del self.options[k]

    def prepared(self):
        for field in self.fields.values():
            if field.default is None:
                continue

            self.defaults[field] = field.default

    def get_default_dict(self):
        dd = {}
        for field, default in self.defaults.items():
            if callable(default):
                dd[field.name] = default()
            else:
                dd[field.name] = default
        return dd


class ApiObjectBase(type):
    inheritable_options = ['verbose_name', 'verbose_name_plural']

    def __new__(cls, name, bases, attrs):
        super_new = super(ApiObjectBase, cls).__new__
        parents = [b for b in bases if isinstance(b, ApiObjectBase)]

        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)

        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})

        meta_options = {}
        meta = attrs.pop('Meta', None)
        if meta:
            meta_options.update((k, v) for k, v in meta.__dict__.items() if not k.startswith('_'))

        if 'urls' not in meta_options:
            meta_options['urls'] = {}

        orig_primary_key = None

        for b in bases:
            if not hasattr(b, '_meta'):
                continue

            base_meta = getattr(b, '_meta')
            for (k, v) in base_meta.__dict__.items():
                if k in cls.inheritable_options and k not in meta_options:
                    meta_options[k] = v

            for (k, attr) in b.__dict__.items():
                if isinstance(attr, ForeignRelatedObject) and isinstance(getattr(attr, 'old_field'), Field):
                    attrs[k] = deepcopy(getattr(attr, 'old_field'))
                if not isinstance(attr, FieldDescriptor) or attr in attrs:
                    continue

                attrs[k] = deepcopy(attr.field)

                if isinstance(attr.field, PrimaryKeyField) and not orig_primary_key:
                    orig_primary_key = deepcopy(attr.field)

        cls = super(ApiObjectBase, cls).__new__(cls, name, bases, attrs)

        _meta = BaseModelOptions(cls, meta_options)
        cls._meta = _meta
        cls._data = None

        for name, attr in list(cls.__dict__.items()):
            if not isinstance(attr, Field):
                continue

            attr.add_to_class(cls, name)
            _meta.fields[attr.name] = attr
            _meta.api_names[attr.api_name] = attr.name

            if isinstance(attr, PrimaryKeyField):
                orig_primary_key = attr

        if orig_primary_key is not None:
            _meta.pk_name = orig_primary_key.name

        _meta.model_name = new_class.__name__

        exception_class = type('%sDoesNotExist' % _meta.model_name, (DoesNotExist,), {})

        cls.DoesNotExist = exception_class
        cls._meta.prepared()

        return cls

@six.add_metaclass(ApiObjectBase)
class BaseApiModelMethods(object):
    def __init__(self, *args, **kwargs):
        self._data = self._meta.get_default_dict()
        self._handler = kwargs.pop('handler', None)

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def handler(self):
        return self._handler or get_default_handler()

    def __repr__(self):
        try:
            u = six.text_type(self)
        except (UnicodeEncodeError, UnicodeDecodeError):
            u = '[Bad Unicode data]'
        return force_str('<%s: %s>' % (self.__class__.__name__, u))

    def __str__(self):
        if six.PY2 and hasattr(self, '__unicode__'):
            return force_text(self).encode('utf-8')

        return '%s object' % self.__class__.__name__

    def __eq__(self, other):
        return (other.__class__ == self.__class__ and
                self.get_pk() and
                other.get_pk() == self.get_pk())


class BaseApiModel(BaseApiModelMethods):

    def __getattr__(self, name):
        return object.__getattribute__(self, self._meta.api_names.get(name, name))

    def __setattr__(self, name, value):
        super(BaseApiModel, self).__setattr__(self._meta.api_names.get(name, name), value)

    def fixed_kwargs(self):
        return {}

    def save(self, handler=None, cls=None, idempotency_key=None):
        self._handler = handler or self.handler

        field_dict = dict(self._data)
        field_dict.update(self.get_field_dict())
        field_dict.pop(self._meta.pk_name)

        all_fields = self._meta.fields

        if cls is None:
            cls = self.__class__

        created = False

        pre_save.send(cls, instance=self)

        if self.get_pk():
            update = self.update(
                self.get_pk(),
                **field_dict
            )
            result = update.execute(self._handler)
        else:
            for k, v in all_fields.items():
                if v.required is True and field_dict[v.name] is None:
                    raise ValueError('Missing mandatory field: ' + v.name)

            insert = self.insert(idempotency_key=idempotency_key, **field_dict)
            result = insert.execute(self._handler)

            created = True

        post_save.send(cls, instance=self, created=created)

        for key, value in result.items():
            setattr(self, key, value)

        return result

    @classmethod
    def select(cls, *args, **kwargs):
        return SelectQuery(cls, *args, **kwargs)

    @classmethod
    def create(cls, **query):
        handler = query.pop('handler', get_default_handler())
        inst = cls(**query)
        inst.save(handler)
        return inst

    @classmethod
    def update(cls, reference, **query):
        return UpdateQuery(cls, reference, **query)

    @classmethod
    def insert(cls, idempotency_key, **query):
        return InsertQuery(cls, idempotency_key=idempotency_key, **query)

    @classmethod
    def get(cls, *args, **kwargs):
        return cls.select().get(*args, **kwargs)

    def one(self, resource_model):
        return resource_model.select().get(self.get_pk(),
                                           resource_model=self.__class__,
                                           handler=self.handler)

    def list(self, resource_model, **kwargs):
        return resource_model.select().list(self.get_pk(),
                                            self.__class__,
                                            handler=self.handler,
                                            **kwargs)

    @classmethod
    def all(cls, *args, **kwargs):
        return cls.select().all(*args, **kwargs)

    def get_pk(self):
        return getattr(self, self._meta.pk_name, None)

    def get_pk_field(self):
        return self._meta.fields[self._meta.pk_name]

    def get_field_dict(self):
        def get_field_val(field):
            field_value = getattr(self, field.name)
            if not self.get_pk() and field_value is None and field.default is not None:
                if callable(field.default):
                    field_value = field.default()
                else:
                    field_value = field.default
                setattr(self, field.name, field_value)
            return (field.name, field_value)

        pairs = map(get_field_val, self._meta.fields.values())

        return dict(pairs)
