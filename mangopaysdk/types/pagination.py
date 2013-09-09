class Pagination():
    """Class represents pagination information."""

    """Array with links to navigation.
    All values optional. Format:
    (
         first => http url
         prev => http url
         next => http url
         last => http url
    )
    """
    Links = ()


    def __init__(self, page = 1, itemsPerPage = 10):
        """Constructor.
        param int page Number of page
        param int itemsPerPage Number of items on one page
        """
        self.Page = page
        self.ItemsPerPage = itemsPerPage
        self.TotalPages = None
        self.TotalItems = None

