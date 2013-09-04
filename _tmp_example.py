"""TEMPORARY DEBUG/DEVELOPMENT SCRIPT.
It's here only for our (developers) convenience.
Please ignore it (or take as a simple usage example).
"""

## run some test
#import tests.testapiusers
#t = tests.testapiusers.Test_ApiUsers()
#t.test_Users_GetNatural()

from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.types.pagination import Pagination

api = MangoPayApi()
# test client credentials
api.Config.ClientID = 'example'
api.Config.ClientPassword = 'uyWsmnwMQyTnqKgi8Y35A3eVB7bGhqrebYqA1tL6x2vYNpGPiY'

# optionally reuse token from previous requests (unless expired)
token = api.authenticationManager.CreateToken()
api.OAuthToken = token

# GET USERS LIST: GET /users
pagination = Pagination(1, 8)
users = api.users.GetAll(pagination)

# display result on screen
print(users)

# optionally store token for future requests (unless expires)
print(api.OAuthToken)

input('...')
