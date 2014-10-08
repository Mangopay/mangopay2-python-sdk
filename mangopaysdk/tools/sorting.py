

class Sorting:
    """Base sorting object."""

    SortFieldSeparator = "_"
    SortUrlParameterName = "Sort"
    
    _sortFields = {}
    
    def AddField(self, fieldName, sortDirection):
        self._sortFields[fieldName] = sortDirection
    
    def GetSortParameter(self):
        return { self.SortUrlParameterName, self._getFields() }
    
    def _getFields(self):
        sortValues = ""
        for key, val in self._sortFields.items():
            if (sortValues != ''):
                sortValues += self.SortFieldSeparator
     
            sortValues += key + ":" + val
        
        return sortValues