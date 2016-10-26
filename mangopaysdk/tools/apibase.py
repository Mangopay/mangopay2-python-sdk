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
from mangopaysdk.entities.settlement import Settlement
from mangopaysdk.entities.client import Client
from mangopaysdk.entities.card import Card
from mangopaysdk.entities.refund import Refund
from mangopaysdk.entities.cardregistration import CardRegistration
from mangopaysdk.entities.cardpreauthorization import CardPreAuthorization
from mangopaysdk.entities.hook import Hook
from mangopaysdk.entities.dispute import Dispute
from mangopaysdk.entities.disputedocument import DisputeDocument
from mangopaysdk.entities.disputepage import DisputePage
from mangopaysdk.entities.repudiation import Repudiation
from mangopaysdk.entities.mandate import Mandate
from mangopaysdk.types.payinexecutiondetails import PayInExecutionDetails
from mangopaysdk.types.payinexecutiondetailsweb import PayInExecutionDetailsWeb
from mangopaysdk.types.payinpaymentdetails import PayInPaymentDetails
from mangopaysdk.types.payinpaymentdetailspreauthorized import PayInPaymentDetailsPreAuthorized
from mangopaysdk.types.payinpaymentdetailsbankwire import PayInPaymentDetailsBankWire
from mangopaysdk.types.payinpaymentdetailspaypal import PayInPaymentDetailsPayPal
from mangopaysdk.types.payinpaymentdetailscard import PayInPaymentDetailsCard
from mangopaysdk.types.payinpaymentdetailsdirectdebit import PayInPaymentDetailsDirectDebit
from mangopaysdk.types.payoutpaymentdetails import PayOutPaymentDetails
from mangopaysdk.types.payinexecutiondetailsdirect import PayInExecutionDetailsDirect
from mangopaysdk.types.payoutpaymentdetailsbankwire import PayOutPaymentDetailsBankWire
from mangopaysdk.types.bankaccountdetailsiban import BankAccountDetailsIBAN
from mangopaysdk.types.bankaccountdetailsgb import BankAccountDetailsGB
from mangopaysdk.types.bankaccountdetailsus import BankAccountDetailsUS
from mangopaysdk.types.bankaccountdetailsca import BankAccountDetailsCA
from mangopaysdk.types.bankaccountdetailsother import BankAccountDetailsOTHER
from mangopaysdk.types.refundreason import RefundReason
from mangopaysdk.types.address import Address
from mangopaysdk.entities.temporarypaymentcard import TemporaryPaymentCard
from mangopaysdk.entities.temporaryimmediatepayin import TemporaryImmediatePayIn


class ApiBase(object):
    """Base class for all Api* classes (managers)."""

    # Root/parent MangoPayApi instance that holds the OAuthToken and Configuration instance
    _root = None

    # Array with REST url and request type
    _methods = {
        'client_get' : ('/clients', 'GET'),
        'client_save' : ('/clients', 'PUT'),
        'client_upload_logo' : ('/clients/logo', 'PUT'),

        'client_get_wallets_default' : ('/clients/wallets', 'GET'),
        'client_get_wallets_fees' : ('/clients/wallets/fees', 'GET'),
        'client_get_wallets_credit' : ('/clients/wallets/credit', 'GET'),
        'client_get_wallets_default_with_currency' : ('/clients/wallets/%s', 'GET'),
        'client_get_wallets_fees_with_currency' : ('/clients/wallets/fees/%s', 'GET'),
        'client_get_wallets_credit_with_currency' : ('/clients/wallets/credit/%s', 'GET'),
        'client_get_wallet_transactions' : ('/clients/wallets/%s/%s/transactions', 'GET'),

        'authentication_base' : ('/clients/', 'POST'),
        'authentication_oauth' : ('/oauth/token', 'POST'),

        'events_all' : ('/events', 'GET'),

        'hooks_create' : ('/hooks', 'POST'),
        'hooks_all' : ('/hooks', 'GET'),
        'hooks_get' : ('/hooks/%s', 'GET'),
        'hooks_save' : ('/hooks/%s', 'PUT'),

        'cardregistration_create': ('/cardregistrations', 'POST'),
        'cardregistration_get': ('/cardregistrations/%s', 'GET'),
        'cardregistration_save': ('/cardregistrations/%s', 'PUT'),

        'preauthorizations_create' : ('/preauthorizations/card/direct', 'POST'),
        'preauthorizations_get' : ('/preauthorizations/%s', 'GET'),
        'preauthorizations_save' : ('/preauthorizations/%s', 'PUT'),

        'card_get': ('/cards/%s', 'GET'),
        'card_save': ('/cards/%s', 'PUT'),

        'payins_card-web_create' : ('/payins/card/web/', 'POST'),
        'payins_card-direct_create' : ('/payins/card/direct/', 'POST'),
        'payins_preauthorized-direct_create' : ('/payins/preauthorized/direct/', 'POST'),

        'payins_bankwire-direct_create' : ('/payins/bankwire/direct/', 'POST'),
        'payins_paypal-web_create' : ('/payins/paypal/web/', 'POST'),
        
        'payins_directdebit-web_create' : ('/payins/directdebit/web', 'POST'),
        'payins_directdebit-direct_create' : ('/payins/directdebit/direct', 'POST'),
        'payins_get' : ('/payins/%s', 'GET'),
        'payins_getrefunds' : ('/payins/%s/refunds', 'GET'),
        'payins_createrefunds' : ('/payins/%s/refunds', 'POST'),

        'payouts_bankwire_create' : ('/payouts/bankwire/', 'POST'),
        
        'payouts_get' : ('/payouts/%s', 'GET'),
        'payouts_createrefunds' : ('/payouts/%s/refunds', 'POST'),
        'payouts_getrefunds' : ('/payouts/%s/refunds', 'GET'),
        
        'refunds_get' : ('/refunds/%s', 'GET'),


        'transfers_create' : ('/transfers', 'POST'),
        'transfers_get' : ('/transfers/%s', 'GET'),
        'transfers_getrefunds' : ('/transfers/%s/refunds', 'GET'),
        'transfers_createrefunds' : ('/transfers/%s/refunds', 'POST'),

        'users_createnaturals' : ('/users/natural', 'POST'),
        'users_createlegals' : ('/users/legal', 'POST'),
        
        'users_createkycpage' : ('/users/%s/KYC/documents/%s/pages', 'POST'),
        'users_createkycdocument' : ('/users/%s/KYC/documents/', 'POST'),
        'users_getkycdocument' : ('/users/%s/KYC/documents/%s', 'GET'),
        'users_savekycdocument' : ('/users/%s/KYC/documents/%s', 'PUT'),

        'users_createbankaccounts_iban': ('/users/%s/bankaccounts/iban', 'POST'),
        'users_createbankaccounts_gb': ('/users/%s/bankaccounts/gb', 'POST'),
        'users_createbankaccounts_us': ('/users/%s/bankaccounts/us', 'POST'),
        'users_createbankaccounts_ca': ('/users/%s/bankaccounts/ca', 'POST'),
        'users_createbankaccounts_other': ('/users/%s/bankaccounts/other', 'POST'),
        'users_updatebankaccount' : ('/users/%s/bankaccounts/%s', 'PUT'),

        'users_all' : ('/users', 'GET'),
        'users_allwallets' : ('/users/%s/wallets', 'GET'),
        'users_allbankaccount' : ('/users/%s/bankaccounts', 'GET'),
        'users_getcards' : ('/users/%s/cards', 'GET'),
        'users_transactions' : ('/users/%s/transactions', 'GET'),
        'users_allkycdocuments' : ('/users/%s/KYC/documents', 'GET'),#new
        'users_get' : ('/users/%s', 'GET'),
        'users_getnaturals' : ('/users/natural/%s', 'GET'),
        'users_getlegals' : ('/users/legal/%s', 'GET'),
        'users_getbankaccount' : ('/users/%s/bankaccounts/%s', 'GET'),
        'users_savenaturals' : ('/users/natural/%s', 'PUT'),
        'users_savelegals' : ('/users/legal/%s', 'PUT'),
        'wallets_create' : ('/wallets', 'POST'),
        'wallets_alltransactions' : ('/wallets/%s/transactions', 'GET'),
        'wallets_get' : ('/wallets/%s', 'GET'),
        'wallets_save' : ('/wallets/%s', 'PUT'),

        'kyc_documents_all' : ('/KYC/documents', 'GET'),
        'kyc_document_get' : ('/KYC/documents/%s', 'GET'),

        'disputes_get' : ('/disputes/%s', 'GET'),
        'disputes_save_tag' : ('/disputes/%s', 'PUT'),
        'disputes_save_contest_funds' : ('/disputes/%s/submit', 'PUT'),
        'disputes_save_close' : ('/disputes/%s/close', 'PUT'),
        'disputes_get_transactions' : ('/disputes/%s/transactions', 'GET'),
        'disputes_get_all' : ('/disputes', 'GET'),
        'disputes_get_for_wallet' : ('/wallets/%s/disputes', 'GET'),
        'disputes_get_for_user' : ('/users/%s/disputes', 'GET'),
        'disputes_document_create' : ('/disputes/%s/documents', 'POST'),
        'disputes_document_page_create' : ('/disputes/%s/documents/%s/pages', 'POST'),
        'disputes_document_submit' : ('/disputes/%s/documents/%s', 'PUT'),
        'disputes_document_get' : ('/dispute-documents/%s', 'GET'),
        'disputes_document_get_for_dispute' : ('/disputes/%s/documents', 'GET'),
        'disputes_document_get_for_client' : ('/dispute-documents', 'GET'),
        'disputes_repudiation_get' : ('/repudiations/%s', 'GET'),
	    'disputes_repudiation_create_settlement' : ('/repudiations/%s/settlementtransfer', 'POST'),
        
        'settlement_get' : ('/settlements/%s', 'GET'),

        'idempotency_response_get' : ('/responses/%s', 'GET'),

        # These are temporary functions and WILL be removed in the future. 
        # Contact support before using these features or if have any queries.
        'temp_paymentcards_create' : ('/temp/paymentcards', 'POST'),
        'temp_paymentcards_get' : ('/temp/paymentcards/%s', 'GET'),
        'temp_immediatepayins_create' : ('/temp/immediate-payins', 'POST'),

        'mandate_create' : ('/mandates/directdebit/web', 'POST'),
        'mandate_cancel' : ('/mandates/%s/cancel', 'PUT'),
        'mandate_get' : ('/mandates/%s', 'GET'),
        'mandates_get_all' : ('/mandates', 'GET'),
        'mandates_get_for_user' : ('/users/%s/mandates', 'GET'),
        'mandates_get_for_bank_account' : ('/users/%s/bankaccounts/%s/mandates', 'GET'),
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
        return self._createObjectIdempotent(None, methodKey, entity, responseClassName, entityId, secondEntityId)

    def _createObjectIdempotent (self, idempotencyKey, methodKey, entity, responseClassName = None, entityId = None, secondEntityId = None):
        """Create object in API.
        param string idempotencyKey Idempotency key for this request
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
        response = rest.RequestIdempotent(idempotencyKey, urlMethod, self._getRequestType(methodKey), requestData)

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

    def _getList (self, methodKey, pagination, responseClassName = None, entityId = None, filter = None, sorting = None, secondEntityId = None):
        """Get list with entities object from API.
        param string methodKey Key with request data
        param pagination Pagination object
        param object responseClassName Name of entity class from response
        param string entityId Entity identifier
        param object filter Object to filter data
        param object sorting Object to sort data
        param string secondEntityId Second entity identifier
        return object Response data
        """
        urlMethod = self._buildUrl(methodKey, entityId, secondEntityId)

        if pagination == None:
            pagination = Pagination()

        rest = RestTool(self._root, True)
        additionalUrlParams = {}
        if (filter != None):
            additionalUrlParams['filter'] = filter
        if (sorting != None):
            additionalUrlParams['sort'] = sorting.GetSortParameter()

        response = rest.Request(urlMethod, self._getRequestType(methodKey), None, pagination, additionalUrlParams)

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
