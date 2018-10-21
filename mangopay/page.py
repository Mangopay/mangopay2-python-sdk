class Page:

    def __init__(self, data, **kwargs):
        self.data = data
        self.page = kwargs.get('page', 1)
        self.per_page = kwargs.get('per_page', 10)
        self.total_pages = kwargs.get('total_pages')
        self.total_items = kwargs.get('total_items')

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, item):
        return self.data[item]
