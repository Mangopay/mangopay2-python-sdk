from .utils import Choices


USER_TYPE_CHOICES = Choices(
    ('NATURAL', 'natural', 'Natural user'),
    ('LEGAL', 'legal', 'Legal user')
)

LEGAL_USER_TYPE_CHOICES = Choices(
    ('BUSINESS', 'business', 'Business'),
    ('ORGANIZATION', 'organization', 'Organization'),
    ('SOLETRADER', 'soletrader', 'Soletrader')
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
    ('TRANSFER', 'transfer', 'Transfer')
)

NATURE_CHOICES = Choices(
    ('REGULAR', 'regular', 'Regular'),
    ('REFUND', 'refund', 'Refund'),
    ('REPUDIATION', 'repudiation', 'Repudiation'),
    ('SETTLEMENT', 'settlement', 'Settlement')
)

EXECUTION_TYPE_CHOICES = Choices(
    ('WEB', 'web', 'Web'),
    ('DIRECT', 'direct', 'Direct')
)

SECURE_MODE_CHOICES = Choices(
    ('DEFAULT', 'default', 'Default'),
    ('FORCE', 'force', 'Force')
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
    ('REFUSED', 'refused', 'Refused')
)

EVENT_TYPE_CHOICES = Choices(
    ('KYC_CREATED', 'kyc_created', 'KYC Created'),
    ('KYC_SUCCEEDED', 'kyc_succeeded', 'KYC succeeded'),
    ('KYC_FAILED', 'kyc_failed', 'KYC failed'),
    ('KYC_VALIDATION_ASKED', 'kyc_validation_asked', 'KYC Validation asked'),
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
    ('TRANSFER_REFUND_FAILED', 'transfer_refund_failed', 'Transfer refund failed')
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
    ('OTHER', 'other', 'Other')
)

MANDATE_STATUS_CHOICES = Choices(
    ('CREATED', 'created', 'Created'),
    ('SUBMITTED', 'submitted', 'Submitted'),
    ('ACTIVE', 'active', 'Active'),
    ('FAILED', 'failed', 'Failed')
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
    ('TRANSACTIONS', 'transactions', 'Transactions')
)

PAYIN_PAYMENT_TYPE = Choices(
    ("CARD", "card", "Card"),
    ("DIRECT_DEBIT", "direct_debit", "Direct Debit"),
    ("PREAUTHORIZED", "preauthorized", "Preauthorized"),
    ("BANK_WIRE", "bank_wire", "Bank Wire")
)

CARD_STATUS_CHOICES = Choices(
    ("CREATED", "created", "Created"),
    ("VALIDATED", "validated", "Validated"),
    ("ERROR", "error", "Error")
)
