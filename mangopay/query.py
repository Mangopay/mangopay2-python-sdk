import six

from mangopay.page import Page
from . import get_default_handler


class BaseQuery(object):
    def __init__(self, model, method=None):
        self.model = model
        self.method = method
        self._handler = None

    @property
    def handler(self):
        return self._handler or get_default_handler()

    def parse_result(self, result, model_klass=None):
        pairs = {}
        model_klass = model_klass or self.model

        for api_name, field_name in model_klass._meta.api_names.items():
            field = model_klass._meta.get_field_by_name(field_name)
            if result and api_name in result:
                pairs[field_name] = field.python_value(result[api_name])

        return pairs

    def parse_url(self, meta_url, params=None):
        if isinstance(meta_url, dict):
            url = meta_url.get(self.identifier)
        else:
            url = meta_url

        if params:
            url = url % params

        return url


class SelectQuery(BaseQuery):
    identifier = 'SELECT'

    def __init__(self, model, *args, **kwargs):
        super(SelectQuery, self).__init__(model, 'GET')

    def get(self, reference, handler=None, resource_model=None, without_client_id=False, **kwargs):
        model = resource_model or self.model
        handler = handler or self.handler

        meta_url = self.parse_url(model._meta.url, kwargs)
        if reference != "":
            url = '%s/%s' % (meta_url, reference)
        else:
            url = '%s' % meta_url

        result, data = handler.request(self.method, url, without_client_id=without_client_id)

        if 'errors' in data:
            if result.status_code == 404:
                raise model.DoesNotExist('instance %s matching reference %s does not exist' % (model._meta.model_name,
                                                                                               reference))
            else:
                return handler._create_apierror(result, url)

        cast = getattr(model, 'cast', lambda result: model)
        model_klass = cast(data)

        return model_klass(handler=handler,
                           **dict(self.parse_result(data, model_klass)))

    def list(self, reference, resource_model, handler=None, **kwargs):
        handler = handler or self.handler

        result, data = handler.request(self.method,
                                       '/%s/%s/%s' % (resource_model._meta.verbose_name_plural, reference,
                                                      self.model._meta.verbose_name_plural), **kwargs)

        return [self.model(handler=handler,
                           **dict(self.parse_result(entry))) for entry in data]

    def all(self, handler=None, without_client_id=False, **params):
        handler = handler or self.handler

        url = self.parse_url(self.model._meta.url, params)
        result, data = handler.request(self.method, url, without_client_id=without_client_id, **params)

        if 'errors' in data:
            return handler._create_apierror(result, url)

        results = []
        cast = getattr(self.model, 'cast', lambda result: self.model)
        if type(data) is not list:
            data = [data]
        for entry in data:
            model_klass = cast(entry)
            results.append(model_klass(handler=handler, **dict(self.parse_result(entry, model_klass))))

        total_pages = result.headers.get('x-number-of-pages')
        total_items = result.headers.get('x-number-of-items')
        params.update({'total_items': total_items, 'total_pages': total_pages})
        page = Page(results, **params)
        return page


class InsertQuery(BaseQuery):
    identifier = 'INSERT'

    def __init__(self, model, idempotency_key=None, **kwargs):
        self.insert_query = kwargs
        self.idempotency_key = idempotency_key
        super(InsertQuery, self).__init__(model, 'POST')

    def parse_insert(self):
        pairs = {}
        if hasattr(self.model, "_meta"):
            for k, v in six.iteritems(self.insert_query):
                field = self.model._meta.get_field_by_name(k)

                if field.required or v is not None:
                    pairs[field.api_name] = field.api_value(v)

        return pairs

    def execute(self, handler=None, model_klass=None):
        handler = handler or self.handler

        data = self.parse_insert()

        url = self.parse_url(self.model._meta.url, self.insert_query)

        result, data = handler.request(self.method,
                                       url,
                                       data=data,
                                       idempotency_key=self.idempotency_key)

        return dict(self.parse_result(data, model_klass))


class UpdateQuery(BaseQuery):
    identifier = 'UPDATE'

    def __init__(self, model, reference, **kwargs):
        self.update_query = kwargs
        self.reference = reference
        super(UpdateQuery, self).__init__(model, 'PUT')

    def parse_update(self):
        pairs = {}
        for k, v in six.iteritems(self.update_query):
            field = self.model._meta.get_field_by_name(k)

            if field.required or v is not None:
                pairs[field.api_name] = field.api_value(v)

        return pairs

    def execute(self, handler=None):
        handler = handler or self.handler

        data = self.parse_update()

        meta_url = self.parse_url(self.model._meta.url, self.update_query)
        url = '%s/%s' % (meta_url, self.reference)

        result, data = handler.request(self.method,
                                       url,
                                       data=data)

        return self.parse_result(data)


class ActionQuery(BaseQuery):

    def __init__(self, model, reference, identifier, method='PUT', params=None, **kwargs):
        self.action_query = kwargs
        self.reference = reference
        self.identifier = identifier
        self.params = params
        super(ActionQuery, self).__init__(model, method)

    def execute(self, handler=None):
        handler = handler or self.handler

        data = self.action_query
        url = self.parse_url(self.model._meta.url, self.params)
        url = url % {'id': self.reference}

        result, data = handler.request(self.method,
                                       url,
                                       data=data)
        if isinstance(data, list):
            return [self.parse_result(d) for d in data]
        return self.parse_result(data)
