"""TEMPORARY DEBUG/DEVELOPMENT SCRIPT.
It's here only for our (developers) convenience.
Please ignore it (or take as a simple usage example).
"""

## run some test
import tests.testapiusers
t = tests.testapiusers.Test_ApiUsers()
t.test_Users_CreateNatural()

from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.types.pagination import Pagination

api = MangoPayApi()
# test client credentials
api.Config.ClientID = 'sdk-unit-tests'
api.Config.ClientPassword = 'cqFfFrWfCcb7UadHNxx2C9Lo6Djw8ZduLi7J9USTmu8bhxxpju'

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
