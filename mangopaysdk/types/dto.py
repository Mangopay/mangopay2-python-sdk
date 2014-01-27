class Dto(object):
    """Abstract class for all DTOs (entities and their composites)."""
    
    def GetSubObjects(self):
        """Get array with mapping which property is object and what type of object.
        To be overridden in child class if has any sub objects.
        return array
        """
        return {}

    def GetDependsObjects(self):
        """Get array with mapping which property depends on other property.
        To be overridden in child class if has any dependent objects.
        return array
        """
        return {}
   
    def GetReadOnlyProperties(self):
        """Get array with read only properties - not used in response.
        To be overridden in child class if has any read-only properies.
        return array
        """
        return []
