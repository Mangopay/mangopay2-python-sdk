

class Sorting(object):
    """Base sorting object."""

    SortFieldSeparator = "_"
    SortUrlParameterName = "Sort"
    
    _sortFields = []

    def __init__(self):
        self._sortFields = []
    
    def AddField(self, fieldName, sortDirection):
        self._sortFields.append([fieldName, sortDirection])
    
    def GetSortParameter(self):
        return [self.SortUrlParameterName, self._getFields()]
    
    def _getFields(self):
        sortValues = ""
        for val in self._sortFields:
            if (sortValues != ''):
                sortValues += self.SortFieldSeparator
     
            sortValues += val[0] + ":" + val[1]
        
        return sortValues