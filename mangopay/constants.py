from .utils import Choices

USER_TYPE_CHOICES = Choices(
    ('NATURAL', 'natural', 'Natural user'),
    ('LEGAL', 'legal', 'Legal user')
)

LEGAL_USER_TYPE_CHOICES = Choices(
    ('BUSINESS', 'business', 'Business'),
    ('ORGANIZATION', 'organization', 'Organization'),
    ('SOLETRADER', 'soletrader', 'Soletrader'),
    ('PARTNERSHIP', 'partnership', 'Partnership')
)

STATUS_CHOICES = Choices(
    ('CREATED', 'created', 'Created'),
    ('SUCCEEDED', 'succeeded', 'Succeeded'),
    ('FAILED', 'failed', 'Failed')
)

CARD_TYPE_CHOICES = Choices(
    ('CB_VISA_MASTERCARD', 'cb_visa_mastercard', 'CB VISA MASTERCARD'),
    ('MAESTRO', 'maestro', 'Maestro'),
    ('DINERS', 'diners', 'Diners'),
    ('AMEX', 'amex', 'Amex'),
    ('MASTERPASS', 'masterpass', 'Masterpass'),
    ('P24', 'p24', 'P24'),
    ('IDEAL', 'ideal', 'Ideal'),
    ('PAYLIB', 'paylib', 'Paylib'),
    ('BCMC', 'bcmc', 'Bcmc')

)

PAYMENT_STATUS_CHOICES = Choices(
    ('WAITING', 'waiting', 'Waiting'),
    ('CANCELED', 'canceled', 'Canceled'),
    ('EXPIRED', 'expired', 'Expired'),
    ('VALIDATED', 'validated', 'Validated')
)

VALIDITY_CHOICES = Choices(
    ('UNKNOWN', 'unknown', 'Unknown'),
    ('VALID', 'valid', 'Valid'),
    ('INVALID', 'invalid', 'Invalid')
)

TRANSACTION_TYPE_CHOICES = Choices(
    ('PAYIN', 'payin', 'Pay In'),
    ('PAYOUT', 'payout', 'Pay out'),
    ('TRANSFER', 'transfer', 'Transfer'),
    ('CARD_VALIDATION', 'card_validation', 'Card validation')
)

NATURE_CHOICES = Choices(
    ('REGULAR', 'regular', 'Regular'),
    ('REFUND', 'refund', 'Refund'),
    ('REPUDIATION', 'repudiation', 'Repudiation'),
    ('SETTLEMENT', 'settlement', 'Settlement')
)

EXECUTION_TYPE_CHOICES = Choices(
    ('WEB', 'web', 'Web'),
    ('DIRECT', 'direct', 'Direct'),
    ('EXTERNAL_INSTRUCTION', 'external_instruction', 'External instruction')
)

SECURE_MODE_CHOICES = Choices(
    ('DEFAULT', 'default', 'Default'),
    ('FORCE', 'force', 'Force'),
    ('NO_CHOICE', 'no_choice', 'No_Choice')
)

BANK_ACCOUNT_TYPE_CHOICES = Choices(
    ('IBAN', 'iban', 'Iban'),
    ('GB', 'gb', 'GB'),
    ('US', 'us', 'US'),
    ('CA', 'ca', 'CA'),
    ('OTHER', 'other', 'Other')
)

DEPOSIT_CHOICES = Choices(
    ('CHECKING', 'checking', 'Checking'),
    ('SAVINGS', 'savings', 'Savings'),
)

DOCUMENTS_TYPE_CHOICES = Choices(
    ('IDENTITY_PROOF', 'identity_proof', 'Identity proof'),
    ('REGISTRATION_PROOF', 'registration_proof', 'Registration proof'),
    ('ARTICLES_OF_ASSOCIATION', 'articles_of_association', 'Articles of association'),
    ('SHAREHOLDER_DECLARATION', 'shareholder_declaration', 'Shareholder Declaration'),
    ('ADDRESS_PROOF', 'address_proof', 'Address Proof')
)

DOCUMENTS_STATUS_CHOICES = Choices(
    ('CREATED', 'created', 'Created'),
    ('VALIDATION_ASKED', 'validation_asked', 'Validation asked'),
    ('VALIDATED', 'validated', 'Validated'),
    ('REFUSED', 'refused', 'Refused'),
    ('OUT_OF_DATE', 'out_of_date', 'Out of Date')
)

EVENT_TYPE_CHOICES = Choices(
    ('KYC_CREATED', 'kyc_created', 'KYC Created'),
    ('KYC_SUCCEEDED', 'kyc_succeeded', 'KYC succeeded'),
    ('KYC_FAILED', 'kyc_failed', 'KYC failed'),
    ('KYC_VALIDATION_ASKED', 'kyc_validation_asked', 'KYC Validation asked'),
    ('KYC_OUTDATED', 'kyc_outdated', 'KYC Outdated'),
    ('PAYIN_NORMAL_CREATED', 'payin_normal_created', 'Payin normal created'),
    ('PAYIN_NORMAL_SUCCEEDED', 'payin_normal_succeeded', 'Payin normal succeeded'),
    ('PAYIN_NORMAL_FAILED', 'payin_normal_failed', 'Payin normal failed'),
    ('PAYOUT_NORMAL_CREATED', 'payout_normal_created', 'Payout normal created'),
    ('PAYOUT_NORMAL_SUCCEEDED', 'payout_normal_succeeded', 'Payout normal succeeded'),
    ('PAYOUT_NORMAL_FAILED', 'payout_normal_failed', 'Payout normal failed'),
    ('TRANSFER_NORMAL_CREATED', 'transfer_normal_created', 'Transfer normal created'),
    ('TRANSFER_NORMAL_SUCCEEDED', 'transfer_normal_succeeded', 'Transfer normal succeeded'),
    ('TRANSFER_NORMAL_FAILED', 'transfer_normal_failed', 'Transfer normal failed'),
    ('PAYIN_REFUND_CREATED', 'payin_refund_created', 'Payin refund created'),
    ('PAYIN_REFUND_SUCCEEDED', 'payin_refund_succeeded', 'Payin refund succeeded'),
    ('PAYIN_REFUND_FAILED', 'payin_refund_failed', 'Payin refund failed'),
    ('PAYOUT_REFUND_CREATED', 'payout_refund_created', 'Payout refund created'),
    ('PAYOUT_REFUND_SUCCEEDED', 'payout_refund_succeeded', 'Payout refund succeeded'),
    ('PAYOUT_REFUND_FAILED', 'payout_refund_failed', 'Payout refund failed'),
    ('TRANSFER_REFUND_CREATED', 'transfer_refund_created', 'Transfer refund created'),
    ('TRANSFER_REFUND_SUCCEEDED', 'transfer_refund_succeeded', 'Transfer refund succeeded'),
    ('TRANSFER_REFUND_FAILED', 'transfer_refund_failed', 'Transfer refund failed'),
    ('MANDATE_CREATED', 'mandate_created', 'Mandate created'),
    ('MANDATE_FAILED', 'mandate_failed', 'Mandate failed'),
    ('MANDATE_ACTIVATED', 'mandate_activated', 'Mandate activated'),
    ('MANDATE_SUBMITTED', 'mandate_submitted', 'Mandate submitted'),
    ('MANDATE_EXPIRED', 'mandate_expired', 'Mandate expired'),
    ('USER_KYC_REGULAR', 'user_kyc_regular', 'User kyc regular'),
    ('USER_INFLOWS_BLOCKED', 'user_inflows_blocked', 'User inflows blocked'),
    ('USER_INFLOWS_UNBLOCKED', 'user_inflows_unblocked', 'User inflows unblocked'),
    ('USER_OUTFLOWS_BLOCKED', 'user_outflows_blocked', 'User outflows blocked'),
    ('USER_OUTFLOWS_UNBLOCKED', 'user_outflows_unblocked', 'User outflows unblocked'),
    ('PREAUTHORIZATION_CREATED', 'preauthorization_created', 'PreAuthorization created'),
    ('PREAUTHORIZATION_SUCCEEDED', 'preauthorization_succeeded', 'PreAuthorization succeeded'),
    ('PREAUTHORIZATION_FAILED', 'preauthorization_failed', 'PreAuthorization failed'),
    ('INSTANT_PAYOUT_SUCCEEDED', 'instant_payout_succeeded', 'Instant Payout Succeeded'),
    ('INSTANT_PAYOUT_FALLBACKED', 'instant_payout_fallbacked', 'Instant Payout Fallbacked'),
    ('INSTANT_PAYOUT_FAILED', 'instant_payout_failed', 'Instant Payout Failed'),
    ('RECURRING_REGISTRATION_CREATED', 'recurring_registration_created', 'Recurring Registration Created'),
    ('RECURRING_REGISTRATION_AUTH_NEEDED', 'recurring_registration_auth_needed', 'Recurring Auth Needed'),
    ('RECURRING_REGISTRATION_IN_PROGRESS', 'recurring_registration_in_progress', 'Recurring In Progress'),
    ('RECURRING_REGISTRATION_ENDED', 'recurring_registration_ended', 'Recurring Ended'),
    ('COUNTRY_AUTHORIZATION_UPDATED', 'country_authorization_updated', 'Country Authorization Updated'),
    ('DISPUTE_ACTION_REQUIRED', 'dispute_action_required', 'Dispute Action Required'),
    ('DISPUTE_CLOSED', 'dispute_closed', 'Dispute Closed'),
    ('DISPUTE_CREATED', 'dispute_created', 'Dispute Created'),
    ('DISPUTE_DOCUMENT_CREATED', 'dispute_document_created', 'Dispute Document Created'),
    ('DISPUTE_DOCUMENT_VALIDATION_ASKED', 'dispute_document_validation_asked', 'Dispute Document Validation Asked'),
    ('DISPUTE_DOCUMENT_SUCCEEDED', 'dispute_document_succeeded', 'Dispute Document Succeeded'),
    ('DISPUTE_DOCUMENT_FAILED', 'dispute_document_failed', 'Dispute Document Failed'),
    ('DISPUTE_FURTHER_ACTION_REQUIRED', 'dispute_further_action_required', 'Dispute Further Action Required'),
    ('DISPUTE_SENT_TO_BANK', 'dispute_sent_to_bank', 'Dispute Sent To Bank'),
    ('DISPUTE_SUBMITTED', 'dispute_submitted', 'Dispute Submitted'),
    ('PAYIN_REPUDIATION_CREATED', 'payin_repudiation_created', 'Payin Repudiation Created'),
    ('PAYIN_REPUDIATION_SUCCEEDED', 'payin_repudiation_succeeded', 'Payin Repudiation Succeeded'),
    ('PAYIN_REPUDIATION_FAILED', 'payin_repudiation_failed', 'Payin Repudiation Failed'),
    ('PREAUTHORIZATION_PAYMENT_WAITING', 'preauthorization_payment_waiting', 'Preauthorization Payment Waiting'),
    ('PREAUTHORIZATION_PAYMENT_EXPIRED', 'preauthorization_payment_expired', 'Preauthorization Payment Expired'),
    ('PREAUTHORIZATION_PAYMENT_CANCELED', 'preauthorization_payment_canceled', 'Preauthorization Payment Canceled'),
    ('PREAUTHORIZATION_PAYMENT_VALIDATED', 'preauthorization_payment_validated', 'Preauthorization Payment Validated'),
    ('TRANSFER_SETTLEMENT_CREATED', 'transfer_settlement_created', 'Transfer Settlement Created'),
    ('TRANSFER_SETTLEMENT_SUCCEEDED', 'transfer_settlement_succeeded', 'Transfer Settlement Succeeded'),
    ('TRANSFER_SETTLEMENT_FAILED', 'transfer_settlement_failed', 'Transfer Settlement Failed'),
    ('UBO_DECLARATION_CREATED', 'ubo_declaration_created', 'Ubo Declaration Created'),
    ('UBO_DECLARATION_VALIDATION_ASKED', 'ubo_declaration_validation_asked', 'Ubo Declaration Validation Asked'),
    ('UBO_DECLARATION_REFUSED', 'ubo_declaration_refused', 'Ubo Declaration Refused'),
    ('UBO_DECLARATION_VALIDATED', 'ubo_declaration_validated', 'Ubo Declaration Validated'),
    ('UBO_DECLARATION_INCOMPLETE', 'ubo_declaration_incomplete', 'Ubo Declaration Incomplete'),
    ('USER_KYC_LIGHT', 'user_kyc_light', 'User Kyc Light'),

    ('VIRTUAL_ACCOUNT_ACTIVE', 'virtual_account_active', 'Virtual Account Active'),
    ('VIRTUAL_ACCOUNT_BLOCKED', 'virtual_account_blocked', 'Virtual Account Blocked'),
    ('VIRTUAL_ACCOUNT_CLOSED', 'virtual_account_closed', 'Virtual Account Closed'),
    ('VIRTUAL_ACCOUNT_FAILED', 'virtual_account_failed', 'Virtual Account Failed'),

    ('DEPOSIT_PREAUTHORIZATION_CREATED', 'deposit_preauthorization_created', 'Deposit Preauthorization Created'),
    ('DEPOSIT_PREAUTHORIZATION_FAILED', 'deposit_preauthorization_failed', 'Deposit Preauthorization Failed'),
    ('DEPOSIT_PREAUTHORIZATION_PAYMENT_WAITING', 'deposit_preauthorization_payment_waiting',
     'Deposit Preauthorization Payment Waiting'),
    ('DEPOSIT_PREAUTHORIZATION_PAYMENT_EXPIRED', 'deposit_preauthorization_payment_expired',
     'Deposit Preauthorization Payment Expired'),
    ('DEPOSIT_PREAUTHORIZATION_PAYMENT_CANCEL_REQUESTED', 'deposit_preauthorization_payment_cancel_requested',
     'Deposit Preauthorization Payment Cancel Requested'),
    ('DEPOSIT_PREAUTHORIZATION_PAYMENT_CANCELED', 'deposit_preauthorization_payment_canceled',
     'Deposit Preauthorization Payment Canceled'),
    ('DEPOSIT_PREAUTHORIZATION_PAYMENT_VALIDATED', 'deposit_preauthorization_payment_validated',
     'Deposit Preauthorization Payment Validated'),

    ('CARD_VALIDATION_CREATED', 'card_validation_created', 'Card Validation Created'),
    ('CARD_VALIDATION_FAILED', 'card_validation_failed', 'Card Validation Failed'),
    ('CARD_VALIDATION_SUCCEEDED', 'card_validation_succeeded', 'Card Validation Succeeded'),

    ('IDENTITY_VERIFICATION_VALIDATED', 'identity_verification_validated', 'Identity Verification Validated'),
    ('IDENTITY_VERIFICATION_FAILED', 'identity_verification_failed', 'Identity Verification Failed'),
    ('IDENTITY_VERIFICATION_INCONCLUSIVE', 'identity_verification_inconclusive', 'Identity Verification Inconclusive'),
    ('IDENTITY_VERIFICATION_OUTDATED', 'identity_verification_outdated', 'Identity Verification Outdated'),
    ('IDENTITY_VERIFICATION_TIMEOUT', 'identity_verification_timeout', 'Identity Verification Timeout')
)

NOTIFICATION_STATUS_CHOICES = Choices(
    ('ENABLED', 'enabled', 'Enabled'),
    ('DISABLED', 'disabled', 'Disabled')
)

NOTIFICATION_VALIDITY_CHOICES = Choices(
    ('VALID', 'valid', 'Valid'),
    ('INVALID', 'invalid', 'Invalid')
)

DIRECT_DEBIT_TYPE_CHOICES = Choices(
    ('SOFORT', 'sofort', 'Sofort'),
    ('ELV', 'elv', 'ELV'),
    ('GIROPAY', 'giropay', 'Giropay')
)

DISPUTE_TYPE_CHOICE = Choices(
    ('CONTESTABLE', 'contestable', 'Contestable'),
    ('NOT_CONTESTABLE', 'not_contestable', 'Not Contestable'),
    ('RETRIEVAL', 'retrieval', 'Retrieval')
)

DISPUTES_STATUS_CHOICES = Choices(
    ('CREATED', 'created', 'Created'),
    ('PENDING_CLIENT_ACTION', 'pending_client_action', 'Pending Client Action'),
    ('SUBMITTED', 'submitted', 'Submitted'),
    ('PENDING_BANK_ACTION', 'pending_bank_action', 'Pending Bank Action'),
    ('REOPENED_PENDING_CLIENT_ACTION', 'reopened_pending_client_action', 'Reopened Pending Client Action'),
    ('CLOSED', 'closed', 'Closed')
)

DISPUTE_DOCUMENT_TYPE_CHOICES = Choices(
    ('DELIVERY_PROOF', 'delivery_proof', 'Delivery Proof'),
    ('INVOICE', 'invoice', 'Invoice'),
    ('REFUND_PROOF', 'refund_proof', 'Refund Proof'),
    ('USER_CORRESPONDANCE', 'user_correspondance', 'User Correspondance'),
    ('USER_ACCEPTANCE_PROOF', 'user_acceptance_proof', 'User Acceptance Proof'),
    ('PRODUCT_REPLACEMENT_PROOF', 'product_replacement_proof', 'Product Replacement Proof'),
    ('OTHER', 'other', 'Other')
)

REFUSED_REASON_TYPE_CHOICES = Choices(
    ('DOCUMENT_UNREADABLE', 'document_unreadable', 'Document Unreadable'),
    ('DOCUMENT_NOT_ACCEPTED', 'document_not_accepted', 'Document Not Accepted'),
    ('DOCUMENT_HAS_EXPIRED', 'document_has_expired', 'Document Has Expired'),
    ('DOCUMENT_INCOMPLETE', 'document_incomplete', 'Document Incomplete'),
    ('DOCUMENT_MISSING', 'document_missing', 'Document Missing'),
    ('DOCUMENT_DO_NOT_MATCH_USER_DATA', 'document_do_not_match_user_data', 'Document Do Not Match User Data'),
    ('DOCUMENT_DO_NOT_MATCH_ACCOUNT_DATA', 'document_do_not_match_account_data', 'Document Do Not Match Account Data'),
    ('SPECIFIC_CASE', 'specific_case', 'Specific Case'),
    ('DOCUMENT_FALSIFIED', 'document_falsified', 'Document Falsified'),
    ('UNDERAGE_PERSON', 'underage_person', 'Underage Person'),
    ('COUNTERFEIT_PRODUCT', 'counterfeit_product', 'Counterfeit Product'),
    ('OTHER', 'other', 'Other')
)

MANDATE_STATUS_CHOICES = Choices(
    ('CREATED', 'created', 'Created'),
    ('SUBMITTED', 'submitted', 'Submitted'),
    ('ACTIVE', 'active', 'Active'),
    ('FAILED', 'failed', 'Failed'),
    ('EXPIRED', 'expired', 'Expired')
)

MANDATE_TYPE_CHOICES = Choices(
    ('DIRECT_DEBIT', 'direct_debit', 'Direct Debit')
)

MANDATE_SCHEME_CHOICES = Choices(
    ('SEPA', 'sepa', 'Sepa'),
    ('BACS', 'bacs', 'Bacs')
)

PAYOUT_PAYMENT_TYPE = Choices(
    ('BANK_WIRE', 'bank_wire', 'Bank Wire')
)

KYC_LEVEL = Choices(
    ('LIGHT', 'light', 'Light'),
    ('REGULAR', 'regular', 'Regular')
)

PLATFORM_TYPE = Choices(
    ('MARKETPLACE', 'marketplace', 'Marketplace'),
    ('P2P_PAYMENT', 'p2p_payment', 'P2p Payment'),
    ('CROWDFUNDING_DONATION', 'crowdfunding_donation', 'Crowdfunding Donation'),
    ('CROWDFUNDING_REWARD', 'crowdfunding_reward', 'Crowdfunding Reward'),
    ('CROWDFUNDING_EQUITY', 'crowdfunding_equity', 'Crowdfunding Equity'),
    ('CROWDFUNDING_LOAN', 'crowdfunding_loan', 'Crowdfunding Loan'),
    ('OTHER', 'other', 'Other')
)

DOWNLOAD_FORMAT = Choices(
    ('CSV', 'csv', 'Csv')
)

REPORT_TYPE = Choices(
    ('TRANSACTIONS', 'transactions', 'Transactions'),
    ('WALLETS', 'wallets', 'Wallets')
)

PAYIN_PAYMENT_TYPE = Choices(
    ("CARD", "card", "Card"),
    ("DIRECT_DEBIT", "direct_debit", "Direct Debit"),
    ("PREAUTHORIZED", "preauthorized", "Preauthorized"),
    ("BANK_WIRE", "bank_wire", "Bank Wire"),
    ("APPLEPAY", "applepay", "Applepay"),
    ("GOOGLEPAY", "googlepay", "Googlepay"),
    ("GOOGLE_PAY", "google_pay", "Google Pay"),
    ("MBWAY", "mbway", "Mbway"),
    ("PAYPAL", "paypal", "PayPal"),
    ("MULTIBANCO", "multibanco", "Multibanco"),
    ("SATISPAY", "satispay", "Satispay"),
    ("BLIK", "blik", "Blik"),
    ("IDEAL", "ideal", "Ideal"),
    ("GIROPAY", "giropay", "Giropay"),
    ("BCMC", "bancontact", "Bancontact"),
    ("SWISH", "swish", "Swish")
)

CARD_STATUS_CHOICES = Choices(
    ("CREATED", "created", "Created"),
    ("VALIDATED", "validated", "Validated"),
    ("ERROR", "error", "Error")
)

UBO_DECLARATION_STATUS_CHOICES = Choices(
    ("CREATED", "created", "Created"),
    ("VALIDATION_ASKED", "validation_asked", "Validation Asked"),
    ("VALIDATED", "validated", "Validated"),
    ("REFUSED", "refused", "Refused"),
    ("INCOMPLETE", "incomplete", "Incomplete")
)

UBO_DECLARATION_REFUSED_REASON_CHOICES = Choices(
    ("MISSING_UBO", "missing_ubo", "Missing UBO"),
    ("DECLARATION_DO_NOT_MATCH_UBO_INFORMATION", "declaration_do_not_match_ubo_information", "Declaration Do Not "
                                                                                             "Match UBO Information")
)

DECLARED_UBO_STATUS_CHOICES = Choices(
    ("CREATED", "created", "Created"),
    ("VALIDATED", "validated", "Validated"),
    ("REFUSED", "refused", "Refused")
)

DECLARED_UBO_REFUSED_REASON_CHOICES = Choices(
    ("INVALID_DECLARED_UBO", "invalid_declared_ubo", "Invalid Declared UBO"),
    ("INVALID_UBO_DETAILS", "invalid_ubo_details", "Invalid UBO Details")
)

NATURAL_USER_CAPACITY_CHOICES = Choices(
    ("NORMAL", "normal", "Normal"),
    ("DECLARATIVE", "declarative", "Declarative")
)

AVS_RESULT_CHOICES = Choices(
    ("FULL_MATCH", "full_match", "Full Match"),
    ("ADDRESS_MATCH_ONLY", "address_match_only", "Address Match Only"),
    ("POSTAL_CODE_MATCH_ONLY", "postal_code_match_only", "Postal Code Match Only"),
    ("NO_MATCH", "no_match", "No Match"),
    ("NO_CHECK", "no_check", "No Check")
)

DEPOSIT_STATUS_CHOICES = Choices(
    ('CREATED', 'created', 'Created'),
    ('SUCCEEDED', 'succeeded', 'Succeeded'),
    ('FAILED', 'failed', 'Failed')
)

SHIPPING_PREFERENCE_CHOICES = Choices(
    ('SET_PROVIDED_ADDRESS', 'set_provided_address', 'Set Provided Address'),
    ('GET_FROM_FILE', 'get_from_file', 'Get From File'),
    ('NO_SHIPPING', 'no_shipping', 'No Shipping')
)

BIC_CHOICES = Choices(
    ('RABONL2U'),
    ('ABNANL2A'),
    ('FVLBNL22'),
    ('TRIONL2U'),
    ('INGBNL2A'),
    ('SNSBNL2A'),
    ('ASNBNL21'),
    ('RBRBNL21'),
    ('KNABNL2H'),
    ('BUNQNL2A'),
    ('REVOLT21'),
    ('BITSNL2A')
)

BANK_NAME_CHOICES = Choices(
    ('Rabobank'),
    ('ABN AMRO'),
    ('Van Lanschot Baniers'),
    ('Triodos Bank'),
    ('ING Bank'),
    ('SNS Bank'),
    ('ASN'),
    ('RegioBank'),
    ('Knab'),
    ('Bunq'),
    ('Revolut'),
    ('Yoursafe')
)