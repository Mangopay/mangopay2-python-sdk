from mangopaysdk.types.pagination import Pagination
from mangopaysdk.entities.entitybase import EntityBase
from mangopaysdk.types.dto import Dto 
from mangopaysdk.types.money import Money
import json, inspect
from mangopaysdk.tools.resttool import RestTool
from mangopaysdk.entities.event import Event
from mangopaysdk.entities.kycdocument import KycDocument
from mangopaysdk.entities.kycpage import KycPage
from mangopaysdk.entities.payin import PayIn
from mangopaysdk.entities.payout import PayOut
from mangopaysdk.entities.bankaccount import BankAccount
from mangopaysdk.entities.wallet import Wallet
from mangopaysdk.entities.userlegal import UserLegal
from mangopaysdk.entities.usernatural import UserNatural
from mangopaysdk.entities.transfer import Transfer
from mangopaysdk.entities.transaction import Transaction
from mangopaysdk.entities.transfer import Transfer
from mangopaysdk.entities.client import Client
from mangopaysdk.entities.card import Card
from mangopaysdk.entities.refund import Refund
from mangopaysdk.entities.cardregistration import CardRegistration
from mangopaysdk.entities.cardpreauthorization import CardPreAuthorization
from mangopaysdk.entities.hook import Hook
from mangopaysdk.types.payinexecutiondetails import PayInExecutionDetails
from mangopaysdk.types.payinexecutiondetailsweb import PayInExecutionDetailsWeb
from mangopaysdk.types.payinpaymentdetails import PayInPaymentDetails
from mangopaysdk.types.payinpaymentdetailspreauthorized import PayInPaymentDetailsPreAuthorized
from mangopaysdk.types.payinpaymentdetailsbankwire import PayInPaymentDetailsBankWire
from mangopaysdk.types.payinpaymentdetailscard import PayInPaymentDetailsCard
from mangopaysdk.types.payoutpaymentdetails import PayOutPaymentDetails
from mangopaysdk.types.payinexecutiondetailsdirect import PayInExecutionDetailsDirect
from mangopaysdk.types.payoutpaymentdetailsbankwire import PayOutPaymentDetailsBankWire
from mangopaysdk.types.bankaccountdetailsiban import BankAccountDetailsIBAN
from mangopaysdk.types.bankaccountdetailsgb import BankAccountDetailsGB
from mangopaysdk.types.bankaccountdetailsus import BankAccountDetailsUS
from mangopaysdk.types.bankaccountdetailsca import BankAccountDetailsCA
from mangopaysdk.types.bankaccountdetailsother import BankAccountDetailsOTHER


class ApiBase(object):
    """Base class for all Api* classes (managers)."""

    # Root/parent MangoPayApi instance that holds the OAuthToken and Configuration instance
    _root = None

    # Array with REST url and request type
    _methods = {
        'authentication_base' : ('/api/clients/', 'POST'),
        'authentication_oauth' : ('/api/oauth/token', 'POST'),

        'cardregistration_create': ('/cardregistrations', 'POST'),
        'cardregistration_save': ('/cardregistrations/%s', 'PUT'),
        'cardregistration_get': ('/cardregistrations/%s', 'GET'),

        'card_get': ('/cards/%s', 'GET'),
       
        'crosscurrencytransfers_create' : ('/transfers/%s', 'POST'),
        'crosscurrencytransfers_get' : ('/transfers/%s', 'GET'),

        'events_all' : ('/events', 'GET'),
        'events_gethookcallbacks' : ('/events/%s/hook-callbacks', 'GET'),

        'hooks_create' : ('/hooks', 'POST'),
        'hooks_all' : ('/hooks', 'GET'),
        'hooks_get' : ('/hooks/%s', 'GET'),
        'hooks_save' : ('/hooks/%s', 'PUT'),

        'info_get' : ('/info', 'GET'),
        'info_getfeewallets' : ('/info/fee-wallets', 'GET'),
        'info_getmeansofpayment' : ('/info/means-of-payment', 'GET'),

        'paymentcardregistration_create' : ('/payment-card-registration', 'POST'),
        'paymentcardregistration_get' : ('/payment-card-registration/%s', 'GET'),

        'payins_card-web_create' : ('/payins/card/web/', 'POST'),
        'payins_card-direct_create' : ('/payins/card/direct/', 'POST'),
        'payins_card-preauthorized_create' : ('/payins/card/preauthorized/', 'POST'),
        'payins_card-recurrentexecution_create' : ('/payins/card/recurrent-pay-in-execution/', 'POST'),

        'payins_registeredcard-web_create' : ('/payins/registered-card/web/', 'POST'),
        'payins_registeredcard-direct_create' : ('/payins/registered-card/direct/', 'POST'),
        'payins_registeredcard-preauthorized_create' : ('/payins/registered-card/preauthorized/', 'POST'),
        'payins_registeredcard-recurrentexecution_create' : ('/payins/registered-card/recurrent-pay-in-execution/', 'POST'),

        'payins_bankwire-web_create' : ('/payins/bankwire/web/', 'POST'),
        'payins_bankwire-direct_create' : ('/payins/bankwire/direct/', 'POST'),
        'payins_bankwire-preauthorized_create' : ('/payins/bankwire/preauthorized/', 'POST'),
        'payins_bankwire-recurrentexecution_create' : ('/payins/bankwire/recurrent-pay-in-execution/', 'POST'),

        'payins_preauthorized-direct_create' : ('/payins/preauthorized/direct/', 'POST'),

        'payins_directcredit-web_create' : ('/payins/direct-credit/web/', 'POST'),
        'payins_directcredit-direct_create' : ('/payins/direct-credit/direct/', 'POST'),
        'payins_directcredit-preauthorized_create' : ('/payins/direct-credit/preauthorized/', 'POST'),
        'payins_directcredit-recurrentexecution_create' : ('/payins/direct-credit/recurrent-pay-in-execution/', 'POST'),
        'payins_get' : ('/payins/%s', 'GET'),
        'payins_getrefunds' : ('/payins/%s/refunds', 'GET'),
        'payins_createrefunds' : ('/payins/%s/refunds', 'POST'),

        'payouts_bankwire_create' : ('/payouts/bankwire/', 'POST'),
        'payouts_merchantexpense_create' : ('/payouts/merchant-expense/', 'POST'),
        'payouts_amazongiftcard_create' : ('/payouts/amazon-giftcard/', 'POST'),
        'payouts_get' : ('/payouts/%s', 'GET'),
        'payouts_createrefunds' : ('/payouts/%s/refunds', 'POST'),
        'payouts_getrefunds' : ('/payouts/%s/refunds', 'GET'),
        'preauthorizations_create' : ('/preauthorizations/card/direct', 'POST'),
        'preauthorizations_save' : ('/preauthorizations/%s', 'PUT'),
        'preauthorizations_get' : ('/preauthorizations/%s', 'GET'),

        'reccurringpayinorders_create' : ('/reccurring-pay-in-orders', 'POST'),
        'reccurringpayinorders_get' : ('/reccurring-pay-in-orders/%s', 'GET'),
        'reccurringpayinorders_gettransactions' : ('/reccurring-pay-in-orders/%s/transactions', 'GET'),

        'refunds_get' : ('/refunds/%s', 'GET'),

        'repudiations_get' : ('/repudiations/%s', 'GET'),

        'transfers_create' : ('/transfers', 'POST'),
        'transfers_get' : ('/transfers/%s', 'GET'),
        'transfers_getrefunds' : ('/transfers/%s/refunds', 'GET'),
        'transfers_createrefunds' : ('/transfers/%s/refunds', 'POST'),

        'users_createnaturals' : ('/users/natural', 'POST'),
        'users_createlegals' : ('/users/legal', 'POST'),
        'users_createkycrequest' : ('/users/%s/KYC/requests', 'POST'),
        
        'users_createkycpage' : ('/users/%s/KYC/documents/%s/pages', 'POST'),
        'users_createkycdocument' : ('/users/%s/KYC/documents/', 'POST'),
        'users_getkycdocument' : ('/users/%s/KYC/documents/%s', 'GET'),
        'users_savekycdocument' : ('/users/%s/KYC/documents/%s', 'PUT'),

        'users_createbankaccounts_iban': ('/users/%s/bankaccounts/iban', 'POST'),
        'users_createbankaccounts_gb': ('/users/%s/bankaccounts/gb', 'POST'),
        'users_createbankaccounts_us': ('/users/%s/bankaccounts/us', 'POST'),
        'users_createbankaccounts_ca': ('/users/%s/bankaccounts/ca', 'POST'),
        'users_createbankaccounts_other': ('/users/%s/bankaccounts/other', 'POST'),

        'users_all' : ('/users', 'GET'),
        'users_allkyc' : ('/users/%s/KYC', 'GET'),
        'users_allkycrequests' : ('/users/%s/KYC/requests', 'GET'),
        'users_allwallets' : ('/users/%s/wallets', 'GET'),
        'users_allbankaccount' : ('/users/%s/bankaccounts', 'GET'),
        'users_allpaymentcards' : ('/users/%s/payment-cards', 'GET'),
        'users_get' : ('/users/%s', 'GET'),
        'users_getnaturals' : ('/users/natural/%s', 'GET'),
        'users_getlegals' : ('/users/legal/%s', 'GET'),
        'users_getkycrequest' : ('/users/%s/KYC/requests/%s', 'GET'),
        'users_getproofofidentity' : ('/users/%s/ProofOfIdentity', 'GET'),
        'users_getproofofaddress' : ('/users/%s/ProofOfAddress', 'GET'),
        'users_getproofofregistration' : ('/users/%s/ProofOfRegistration', 'GET'),
        'users_getshareholderdeclaration' : ('/users/%s/ShareholderDeclaration', 'GET'),
        'users_getbankaccount' : ('/users/%s/bankaccounts/%s', 'GET'),
        'users_getcards' : ('/users/%s/cards', 'GET'),
        'users_transactions' : ('/users/%s/transactions', 'GET'),
        'users_getpaymentcard' : ('/users/%s/payment-cards/%s', 'GET'),
        'users_savenaturals' : ('/users/natural/%s', 'PUT'),
        'users_savelegals' : ('/users/legal/%s', 'PUT'),

        'wallets_create' : ('/wallets', 'POST'),
        'wallets_allrecurringpayinorders' : ('/wallets/%s/recurring-pay-in-orders', 'GET'),
        'wallets_alltransactions' : ('/wallets/%s/transactions', 'GET'),
        'wallets_get' : ('/wallets/%s', 'GET'),
        'wallets_save' : ('/wallets/%s', 'PUT')
    }


    def __init__ (self, root):
       """Constructor.
       param MangoPayApi Root/parent instance that holds the OAuthToken and Configuration instance
       """
       self._root = root

    def _getRequestUrl (self, key):
        """Get URL for REST Mango Pay API.
        param string key with data
        """
        try:
            return self._methods[key][0]
        except:
            return False

    def _getRequestType (self, key):
        """Get request type for REST Mango Pay API.
        param string key with data
        """
        try:
            return self._methods[key][1]
        except:
            return False

    def _buildUrl (self, methodKey, param1 = None, param2 = None):
        """Build url from method name and params value.
        param string methodKey Key with request data
        param param1 string / int
        param param2 string / int
        return object Response data
        """
        urlMethod = self._getRequestUrl(methodKey)
        if urlMethod.count('%') == 1 and param1 != None:
            return urlMethod % param1
        if urlMethod.count('%') == 2 and param1 != None and param2 != None :
            return urlMethod % (param1, param2)
        return urlMethod

    def _createObject (self, methodKey, entity, responseClassName = None, entityId = None, secondEntityId = None):
        """Create object in API.
        param string methodKey Key with request data
        param object entity Entity object
        param object responseClassName Name of entity class from response
        param int entityId Entity identifier
        param int secondEntityId Releated entity identifier
        return dictionary Response data
        """
        urlMethod = self._buildUrl(methodKey, entityId, secondEntityId)

        if entity != None:
            requestData = self._buildRequestData(entity)

        rest = RestTool(self._root, True)
        response = rest.Request(urlMethod, self._getRequestType(methodKey), requestData)

        if responseClassName != None:
            return self._castResponseToEntity(response, responseClassName)
        return response

    def _getObject (self, methodKey, entityId, responseClassName = None, secondEntityId = None):
        """Get entity object from API.
        param string methodKey Key with request data
        param int entityId Entity identifier
        param object responseClassName Name of entity class from response
        param int secondEntityId Entity identifier for second entity
        return object Response data
        """
        urlMethod = self._buildUrl(methodKey, entityId, secondEntityId)

        rest = RestTool(self._root, True)
        response = rest.Request(urlMethod, self._getRequestType(methodKey))

        if responseClassName != None:
            return self._castResponseToEntity(response, responseClassName)
        return response

    def _getList (self, methodKey, pagination, responseClassName = None, entityId = None, filter = None):
        """Get list with entities object from API.
        param string methodKey Key with request data
        param pagination Pagination object
        param object responseClassName Name of entity class from response
        param int entityId Entity identifier
        param object filter Object to filter data
        return object Response data
        """
        urlMethod = self._buildUrl(methodKey, entityId)

        if pagination == None:
            pagination = Pagination()

        rest = RestTool(self._root, True)
        response = rest.Request(urlMethod, self._getRequestType(methodKey), None, pagination, filter)

        if responseClassName != None:
            return self._castResponseToEntity(response, responseClassName)
        return response

    def _saveObject (self, methodKey, entity, responseClassName = None, entityId = None, secondEntityId = None):
        """Save object in API.
        param string methodKey Key with request data
        param object entity Entity object to save
        param object responseClassName Name of entity class from response
        return object Response data
        """
        if (entityId == None):
            entityId = entity.Id
        urlMethod = self._buildUrl(methodKey, entityId, secondEntityId)
        requestData = self._buildRequestData(entity)

        rest = RestTool(self._root, True)
        response = rest.Request(urlMethod, self._getRequestType(methodKey), requestData)

        if responseClassName != None:
            return self._castResponseToEntity(response, responseClassName)
        return response


    def _castResponseToEntity(self, response, entityClassName, asDependentObject = False):
        """Cast response object to entity object.
        param object response Object from API response
        param string entityClassName Name of entity class to cast
        @returnentityClassName Return entity object
        """

        if isinstance(response, (list, tuple)):
            objList = []
            for reponseObject in response:
                objList.append(self._castResponseToEntity(reponseObject, entityClassName))
            return objList

        if len(entityClassName) > 0 and entityClassName == "Transaction" and response['Type'] != None:
            if response['Type'] == "PAYIN":
                entityClassName = "PayIn"
            if response['Type'] == "PAYOUT":
                entityClassName = "PayOut"
            if response['Type'] == "REFUND":
                entityClassName = "Refund"
            if response['Type'] == "TRANSFER":
                entityClassName = "Transfer"
            entity = globals()[entityClassName]()
        elif len(entityClassName) > 0 :
            entity = globals()[entityClassName]()
        else:
            raise Exception ('Cannot cast response to entity object. Wrong entity class name')

        subObjects = entity.GetSubObjects()
        dependsObjects = entity.GetDependsObjects()

        for name, value in response.items():
            
            if hasattr(entity, name):
                # is sub object?
                if subObjects.get(name) != None and value != None:
                    object = self._castResponseToEntity(value, subObjects[name])
                    setattr(entity, name, object)
                else:
                    setattr(entity, name, value)

                # has dependent object?
                if dependsObjects.get(name) != None:
                    dependsObject = dependsObjects[name]
                    entityDependProperty = dependsObject['_property_name']
                    setattr(entity, entityDependProperty, self._castResponseToEntity(response, dependsObject[value], True))

        return entity


    def _buildRequestData (self, entity):
        """Get dict with request data.
        param object Entity object to send as request data
        return dictionary
        """
        # no recursive calls - only one level
        entityProperies = entity.__dict__
        blackList = entity.GetReadOnlyProperties()
        requestData = {}

        for k,v in entityProperies.items():
            if blackList.count(k) > 0 or v == None:
                continue;

            if self._canReadSubRequestData(entity, k):
                subRequestData = self._buildRequestData(v)
                requestData.update(subRequestData)
            elif isinstance(v, Dto):
                requestData[k] = v.__dict__
            else:
                requestData[k] = v

        return requestData


    def _canReadSubRequestData (self, entity, propertyName):
        """Get array with request data.
        param object Entity object to send as request data
        return array
        """
        if isinstance(entity, PayIn) and (propertyName == 'PaymentDetails' or propertyName == 'ExecutionDetails'):
            return True
        if isinstance(entity, PayOut) and propertyName == 'MeanOfPaymentDetails':
            return True
        if isinstance(entity, BankAccount) and propertyName == 'Details':
            return True
        return False
