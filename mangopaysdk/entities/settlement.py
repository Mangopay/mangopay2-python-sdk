from mangopaysdk.entities.transfer import Transfer


class Settlement (Transfer):

    def __init__(self, id = None):
        self.RepudiationId = None
        return super(Settlement, self).__init__(id)