## [3.50.0] - 2025-10-01
### Added
- [Verification of Payee (VOP)](https://docs.mangopay.com/guides/vop/recipients-payouts) API response fields (`RecipientVerificationOfPayee` and sub-properties) on the endpoints [GET View a Recipient](https://docs.mangopay.com/api-reference/recipients/view-recipient), [POST Create a Recipient](https://docs.mangopay.com/api-reference/recipients/create-recipient), [POST Create a Payout](https://docs.mangopay.com/api-reference/payouts/create-payout) ([API release note](https://docs.mangopay.com/release-notes/api/2025-09-30), #445)
- Support for the [POST Cancel an Intent](https://docs.mangopay.com/api-reference/intents/cancel-intent) endpoint for [Echo](https://docs.mangopay.com/guides/echo), Mangopay's solution for platforms working with another third-party PSP for funds acquisition (#453) 
- Support for [POST Submit data for a PayPal PayIn](https://docs.mangopay.com/api-reference/paypal/submit-data-paypal-payin) endpoint (#450)

## [3.49.4] - 2025-09-23
### Added
- Webhook event types for [Echo](https://docs.mangopay.com/guides/echo), Mangopay's solution for third-party PSP integrations: `INTENT_AUTHORIZED`,`INTENT_CAPTURED`,`INTENT_REFUNDED`,`INTENT_REFUND_REVERSED`,`INTENT_DISPUTE_CREATED`,`INTENT_DISPUTE_DEFENDED`,`INTENT_DISPUTE_WON`,`INTENT_DISPUTE_LOST`,`INTENT_SETTLED_NOT_PAID`,`INTENT_PAID`,`SPLIT_CREATED`,`SPLIT_PENDING_FUNDS_RECEPTION`,`SPLIT_AVAILABLE`,`SPLIT_REJECTED`,`SPLIT_REVERSED` #448  
- Support for `VirtualAccountPurpose` on Banking Alias object #451 

## [3.49.3] - 2025-09-08
### Added
- Support for `ProfilingAttemptReference` on all payment methods

## [3.49.2] - 2025-09-03
### Added
- Support for missing fields on TransferRefund #444 (thank you @obarahona10 #377) 

### Changed
- Casing of 3 fields to harmonise on snake_case #443 ⚠️ **Breaking change** for Conversion `quote_Id`, Document(KYC) `processed_date`, and Ubo `is_active` (thanks @samitnuk #268) 
- OAuth token refresh buffer before expiry updated to 30s #446 
- Updated testing library to pynose (thank you @nandoks #441)

### Fixed
- Tests

## [3.49.1] - 2025-08-14
### Added
- Support for [POST Create a Quoted Conversion between Client Wallets](https://docs.mangopay.com/api-reference/conversions/create-quoted-conversion-client-wallets) and [POST Create an Instant Conversion between Client Wallets](https://docs.mangopay.com/api-reference/conversions/create-instant-conversion-client-wallets) #437 
- Support for [POST Create a Bank Wire to the Repudiation Wallet](https://docs.mangopay.com/api-reference/dispute-settlement/create-bank-wire-payin-to-repudiation-wallet) #438 
- Support for [GET List Disputes pending settlement](https://docs.mangopay.com/api-reference/disputes/list-disputes-settlement) #439 

## [3.49.0] - 2025-08-07
### Added
Support for new Splits endpoints for Echo (#434, [API release note](https://docs.mangopay.com/release-notes/api/2025-07-16)):
- [PUT Update a Split of an Intent](https://docs.mangopay.com/api-reference/intents/update-intent-split)
- [POST Execute a Split of an Intent](https://docs.mangopay.com/api-reference/intents/execute-intent-split)
- [POST Reverse the Split of an Intent](https://docs.mangopay.com/api-reference/intents/reverse-intent-split)
- [GET View a Split of an Intent](https://docs.mangopay.com/api-reference/intents/view-intent-split)

New `ReportTypes` for Echo (#435, [API release note](https://docs.mangopay.com/release-notes/api/2025-08-06))):
- `ECHO_INTENT`
- `ECHO_INTENT_ACTION`
- `ECHO_SETTLEMENT`
- `ECHO_SPLIT`

## [3.48.1] - 2025-07-28
### Added
- `Sku` parameter on LineItem, for [Klarna PayIns](https://docs.mangopay.com/api-reference/klarna/create-klarna-payin)
- handle new endpoint [View supported banks for Pay by Bank](https://docs.mangopay.com/api-reference/pay-by-bank/view-supported-banks-pay-by-bank), to enable presentation of banks to user before Pay by Bank payment request

## [3.48.0] - 2025-07-18
### Added
Endpoints for [Mangopay Echo](https://docs.mangopay.com/guides/echo), a solution for platforms working with another third-party PSP for funds acquisition (including via the Mirakl Connector) #429 : 
- [POST Create an Intent](https://docs.mangopay.com/api-reference/intents/create-intent)
- [GET View an Intent](https://docs.mangopay.com/api-reference/intents/view-intent)
- [POST Create a Capture for an Intent](https://docs.mangopay.com/api-reference/intents/create-intent-capture)
- [POST Create a Settlement](https://docs.mangopay.com/api-reference/settlements/create-settlement)
- [PUT Update a Settlement](https://docs.mangopay.com/api-reference/settlements/update-settlement)
- [GET View a Settlement](https://docs.mangopay.com/api-reference/settlements/view-settlement)
- [POST Create a Split of an Intent](https://docs.mangopay.com/api-reference/intents/create-intent-split)

## [3.47.0] - 2025-07-02
### Added
- New endpoint [POST Create a Bizum PayIn](https://docs.mangopay.com/api-reference/bizum/create-bizum-payin)
- New webhook event types for SCA enrollment ([API release note](https://docs.mangopay.com/release-notes/api/2025-06-23)), note that these are triggered on enrollment not authentication:
  - `SCA_ENROLLMENT_SUCCEEDED`
  - `SCA_ENROLLMENT_FAILED`
  - `SCA_ENROLLMENT_EXPIRED`
- New webhook event types for `UserCategory` change ([API release note](https://docs.mangopay.com/release-notes/api/2025-06-23) ):
  - `USER_CATEGORY_UPDATED_TO_OWNER`
  - `USER_CATEGORY_UPDATED_TO_PAYER`
  - `USER_CATEGORY_UPDATED_TO_PLATFORM`
- Support for `PLATFORM` value to `UserCategory` enum
- Support for [GET List Transactions for a Card Fingerprint](https://docs.mangopay.com/api-reference/transactions/list-transactions-card-fingerprint)
- Support for [GET List Transactions for a Dispute](https://docs.mangopay.com/api-reference/transactions/list-transactions-dispute)

## [3.46.1] - 2025-06-16

### Added
- [US and CA virtual accounts](https://docs.mangopay.com/release-notes/api/2025-06-12) for local pay-in collection 

## [3.46.0] - 2025-06-10
### Added 

Endpoints for [new Reporting Service](https://docs.mangopay.com/release-notes/api/2025-06-05) feature: 
- [POST Create a Report](https://docs.mangopay.com/api-reference/reporting/create-report)
- [GET View a Report](https://docs.mangopay.com/api-reference/reporting/view-report)
- [GET List all Reports](https://docs.mangopay.com/api-reference/reporting/list-reports)

Webhook [event types](url) for new Reporting Service:
- `REPORT_GENERATED`
- `REPORT_FAILED`

Support for [GET List Disputes for a PayIn](https://docs.mangopay.com/api-reference/disputes/list-disputes-payin) endpoint.

## [3.45.1] - 2025-06-06
### Added
- Support for `RecipientScope` query parameter on [GET List Recipients for a User](https://docs.mangopay.com/api-reference/recipients/list-recipients-user)
- [POST Validate the format of User data](https://docs.mangopay.com/api-reference/user-data-format/validate-user-data-format)

### Fixed 
- `Status` enum value on Identity Verification object changed from `OUTDATED` to `OUT_OF_DATE`

## [3.45.0] - 2025-05-23
### Added 

Event types for [user account webhooks](https://docs.mangopay.com//webhooks/event-types#user-account), relevant to [SCA enrollment in user endpoints](https://docs.mangopay.com/guides/sca/users#user-status) and account closure:  
- `USER_ACCOUNT_VALIDATION_ASKED`
- `USER_ACCOUNT_ACTIVATED`
- `USER_ACCOUNT_CLOSED`

Event types for [instant and quoted FX conversions](https://docs.mangopay.com//webhooks/event-types#fx-conversions): 
- `INSTANT_CONVERSION_CREATED`
- `INSTANT_CONVERSION_SUCCEEDED`
- `INSTANT_CONVERSION_FAILED`
- `QUOTED_CONVERSION_CREATED`
- `QUOTED_CONVERSION_SUCCEEDED`
- `QUOTED_CONVERSION_FAILED`

Support for [30-day deposit preauthorization](https://docs.mangopay.com/guides/payment-methods/card/deposit-preauthorization) features:
- [POST Create a Deposit Preauthorized PayIn prior to complement](https://docs.mangopay.com/api-reference/deposit-preauthorizations/create-deposit-preauthorized-payin-prior-to-complement)
- [POST Create a Deposit Preauthorized PayIn complement](https://docs.mangopay.com/api-reference/deposit-preauthorizations/create-deposit-preauthorized-payin-complement)
- `NO_SHOW_REQUESTED` on `updateDeposit` method for [PUT Cancel a Deposit Preauthorization or request a no-show](https://docs.mangopay.com/api-reference/deposit-preauthorizations/cancel-deposit-preauthorization-request-no-show)
- [GET View a PayIn (Deposit Preauthorized Card](https://docs.mangopay.com/api-reference/deposit-preauthorizations/view-payin-deposit-preauthorized)
- [GET List Transactions for a Deposit Preauthorization](https://docs.mangopay.com/api-reference/transactions/list-transactions-deposit-preauthorization)

### Fixed 

- Regression on User-Agent header SDK version number

## [3.44.0] - 2025-05-14
### Added and refined

#### Hosted KYC/KYB endpoints

The following endpoints have been refined following the beta phase, and are now generally available: 
- [POST Create an IDV Session](https://docs.mangopay.com/api-reference/idv-sessions/create-idv-session) (no changes)
- [GET View an IDV Session](https://docs.mangopay.com/api-reference/idv-sessions/view-idv-session) (includes `Checks` in response)
- [GET List IDV Sessions for a User](https://docs.mangopay.com/api-reference/idv-sessions/list-idv-sessions-user) (new endpoint)

The previously available endpoint GET View Checks for an IDV Session has been removed (as Checks were integrated into the GET by ID). 

See the [guide](https://docs.mangopay.com/guides/users/verification/hosted) for more details.

#### Recipients

The `Country` property has been added to [Recipients](https://docs.mangopay.com/guides/sca/recipients), as a required query parameter on [GET View the schema for a Recipient](https://docs.mangopay.com/api-reference/recipients/view-recipient-schema) and as a required body parameter on [POST Validate data for a Recipient](https://docs.mangopay.com/api-reference/recipients/validate-recipient-data) and [POST Create a Recipient](https://docs.mangopay.com/api-reference/recipients/create-recipient).

### Added 

- [GET List Deposit Preauthorizations for a Card](https://docs.mangopay.com/api-reference/deposit-preauthorizations/list-deposit-preauthorizations-card)
- [GET List Deposit Preauthorizations for a User](https://docs.mangopay.com/api-reference/deposit-preauthorizations/list-deposit-preauthorizations-user)

## [3.43.0] - 2025-04-29
### Added

#### SCA on wallet access endpoints
`ScaContext` query parameter added on wallet access endpoints for the [introduction of SCA](https://docs.mangopay.com/guides/sca/wallets):

- [GET View a Wallet](https://docs.mangopay.com/api-reference/wallets/view-wallet)
- [GET List Wallets for a User](https://docs.mangopay.com/api-reference/wallets/list-wallets-user)
- [GET List Transactions for a User](https://docs.mangopay.com/api-reference/transactions/list-transactions-user)
- [GET List Transactions for a Wallet](https://docs.mangopay.com/api-reference/transactions/list-transactions-wallet)

If SCA is required, Mangopay responds with a 401 response code. The `PendingUserAction` `RedirectUrl` is in the dedicated `WWW-Authenticate` response header.

See the tests for examples on handling this error.

#### BLIK with code
Support for [BLIK with code endpoint](https://docs.mangopay.com/api-reference/blik/create-blik-payin-with-code)

## [3.42.0] - 2025-04-24
### Added 

#### Recipients
- [GET View payout methods](/api-reference/recipients/view-payout-methods)
- [GET View the schema for a Recipient](/api-reference/recipients/view-recipient-schema)
- [POST Validate data for a Recipient](/api-reference/recipients/validate-recipient-data)
- [POST Create a Recipient](/api-reference/recipients/create-recipient)
- [GET View a Recipient](/api-reference/recipients/view-recipient)
- [GET List Recipients for a user](/api-reference/recipients/list-recipients-user)
- [PUT Deactivate a Recipient](/api-reference/recipients/deactivate-recipient)
- Webhook event types:
  - `RECIPIENT_ACTIVE`
  - `RECIPIENT_CANCELED`
  - `RECIPIENT_DEACTIVATED`

#### SCA on Owner-initiated transfers
- On [POST Create a Transfer](/api-reference/transfers/create-transfer)
  - `ScaContext` body parameter 
  - `PendingUserAction` response field containing `RedirectUrl`

#### Endpoints to close a user account
- [DELETE Close a Natural User](/api-reference/users/close-natural-user)
- [DELETE Close a Legal User](/api-reference/users/close-legal-user)

## [3.41.0] - 2025-04-24
### Changed
- ⚠️ **Caution – Minimum language requirement changed to Python 3.9** ⚠️ 

The SDK has been upgraded to require Python 3.9 as a minimum version. This is due to dependencies in the SDK's deployment pipeline on GitHub Actions and Ubuntu runners, which no longer support lower than Python 3.9. Older versions of Python reached end-of-life in 2024 or before.

Failure to upgrade your Python language version to 3.9 before updating to this version of the SDK will result in errors. For more information on the differences between Python 3.9 and earlier, see the [Python docs](https://docs.python.org/3/whatsnew/3.9.html).

The SDK supports Python 3.9, 3.10, 3.11, and 3.12.


#### Added
- [POST Create a TWINT PayIn](https://docs.mangopay.com/api-reference/twint/create-twint-payin)
- [POST Create a Pay by Bank PayIn](https://docs.mangopay.com/api-reference/pay-by-bank/create-pay-by-bank-payin), including related `PAYIN_NORMAL_PROCESSING_STATUS_PENDING_SUCCEEDED` webhook event type
- PayPal recurring payments, thanks to the `PaymentType` value `PAYPAL` on [Recurring PayIn Registrations](https://docs.mangopay.com/api-reference/recurring-payin-registrations/create-recurring-payin-registration-paypal) and new endpoints ([POST Create a Recurring PayPal PayIn (CIT)](https://docs.mangopay.com/api-reference/paypal/create-recurring-paypal-payin-cit) and [POST Create a Recurring PayPal PayIn (MIT)](https://docs.mangopay.com/api-reference/paypal/create-recurring-paypal-payin-mit)

## [3.40.1] - 2025-04-02
### Changed
- User-Agent Header value standardized on format: User-Agent: Mangopay-SDK/`SDKVersion` (`Language`/`LanguageVersion`)

### Fixed
- Fixed tests for categorize SCA users endpoint

## [3.40.0] - 2025-03-19
### Added

New endpoints for [strong customer authentication (SCA)](https://docs.mangopay.com/guides/users/sca) on Owner users:
- [POST Create a Natural User (SCA)](https://docs.mangopay.com/api-reference/users/create-natural-user-sca)
- [PUT Update a Natural User (SCA)](https://docs.mangopay.com/api-reference/users/update-natural-user-sca)
- [POST Create a Legal User (SCA)](https://docs.mangopay.com/api-reference/users/create-legal-user-sca)
- [PUT Update a Legal User (SCA)](https://docs.mangopay.com/api-reference/users/update-legal-user-sca)
- [PUT Categorize a Natural User (SCA)](https://docs.mangopay.com/api-reference/users/categorize-natural-user)
- [PUT Categorize a Legal User (SCA)](https://docs.mangopay.com/api-reference/users/categorize-legal-user)
- [POST Enroll a User in SCA](https://docs.mangopay.com/api-reference/users/enroll-user)

### Added 

New endpoint for Payconiq:
- [POST Create a Payconiq PayIn](https://docs.mangopay.com/api-reference/payconiq/create-payconiq-payin)

## [3.39.1] - 2025-02-28
### Fixed

Rate limiting headers interpreted dynamically based on `X-RateLimit-Reset` time and for a variable number of bucket values.

## [3.39.0] - 2025-02-25
### Added

Endpoints and webhooks for [hosted KYC/B solution](https://docs.mangopay.com/guides/users/verification/hosted) (in beta)

- Endpoints
  - [Create an IDV Session](https://docs.mangopay.com/api-reference/idv-sessions/create-idv-session)
  - [View an IDV Session](https://docs.mangopay.com/api-reference/idv-sessions/view-idv-session)
  - [View Checks for an IDV Session](https://mangopay-idv.mintlify.app/api-reference/idv-sessions/view-idv-session-checks)

- Event types 
  - `IDENTITY_VERIFICATION_VALIDATED`
  - `IDENTITY_VERIFICATION_FAILED`
  - `IDENTITY_VERIFICATION_INCONCLUSIVE`
  - `IDENTITY_VERIFICATION_OUTDATED`

`CardInfo` added for [Apple Pay](https://docs.mangopay.com/api-reference/apple-pay/create-apple-pay-payin) and [Google Pay](https://docs.mangopay.com/api-reference/google-pay/create-google-pay-payin)

### Fixed

Test for KYC documents test_GetKycDocuments

Updating the UBO should not require the full object

Get User EMoney wrong output

## [3.38.0] - 2025-02-14
### Added

New endpoint for the [Swish PayIn](https://docs.mangopay.com/api-reference/swish/swish-payin-object) object:

-  [Create a Swish PayIn](https://docs.mangopay.com/api-reference/swish/create-swish-payin)
-  [View a PayIn (Swish)](https://docs.mangopay.com/api-reference/swish/view-payin-swish)

## [3.37.2] - 2025-02-05
### Updated

Revised tests to improve reliability and address any outdated tests.

## [3.37.1] - 2025-02-03
### Fixed

Added missing `debited_funds` and `fees` parameters to the `BankWirePayInExternalInstruction` class.

## [3.37.0] - 2024-12-13
### Added

- New `PaymentRef` parameter for [Payouts](https://docs.mangopay.com/api-reference/payouts/payout-object#the-payout-object).

## [3.36.1] - 2024-11-28
### Updated

Added all relevant `EVENT_TYPE_CHOICES` for virtual accounts:
- `VIRTUAL_ACCOUNT_ACTIVE`
- `VIRTUAL_ACCOUNT_BLOCKED`
- `VIRTUAL_ACCOUNT_CLOSED`
- `VIRTUAL_ACCOUNT_FAILED`

## [3.36.0] - 2024-11-22
### Added

New endpoints for The Virtual Account object:

- Create a Virtual Account
- Deactivate a Virtual Account
- View a Virtual Account
- List Virtual Accounts for a Wallet
- View Client Availabilities

## [3.35.1] - 2024-09-03
### Fixed

- Add `PreferredCardNetwork` parameter to Direct Card PayIn object. (thank you @pmourlanne) 

## [3.35.0] - 2024-08-13
### Added
- New endpoint: [Create a Bancontact PayIn](https://mangopay.com/docs/endpoints/bancontact#create-bancontact-payin)

## [3.34.3] - 2024-08-09
### Fixed

- Disable `truncatechars` function that would truncate data if it's over 255 characters.

## [3.34.2] - 2024-07-25
### Added
- New parameter SecureModeRedirectURL for [Google Pay PayIn](https://mangopay.com/docs/endpoints/google-pay#google-pay-payin-object)
- New parameters StatementDescriptor for [Refund](https://mangopay.com/docs/endpoints/refunds#refund-object)

## [3.34.1] - 2024-06-12
### Added

- New endpoint [List Transactions for a Client Wallet](https://mangopay.com/docs/endpoints/wallets#list-transactions-client-wallet)

## [3.34.0] - 2024-05-31
### Fixed 

- Usage of filters with `ReportTransactions` and the `create()` method
- BIC is not required for iDeal 

### Added

- New endpoint [Add tracking to Paypal payin](https://mangopay.com/docs/endpoints/paypal#add-tracking-paypal-payin)
- New parameter `SecureMode` for [Create card validation](https://mangopay.com/docs/endpoints/card-validations#create-card-validation)
- New parameters for Paypal mean of payment : `CancelURL` & `Category` (sub-parameter of `LineItems`). And management of `PaypalPayerID`, `BuyerCountry`, `BuyerFirstname`, `BuyerLastname`, `BuyerPhone`, `PaypalOrderID` in the response.
- New parameter `PaymentCategory` for [Create card validation](https://mangopay.com/docs/endpoints/card-validations#create-card-validation) and two additional endpoints [More info](https://mangopay.com/docs/release-notes/kivu)

## [3.33.2] - 2024-05-24
### Added

- New parameter `CardHolderName` for [Update Card registration](https://mangopay.com/docs/endpoints/card-validations#update-card-registration) 

## [3.33.1] - 2024-04-30
### Fixed

- Updated the implementation for [Look up metadata for a payment method](https://mangopay.com/docs/endpoints/payment-method-metadata#lookup-payment-method-metadata). The `CommercialIndicator` and `CardType` fields have been moved to the `BinData` object in the API response.

## [3.33.0] - 2024-03-08
### Fixed

- Fixed incorrect spelling of the `Subtype` key in the `BinData` parameter.
- Conversions endpoint spelling

### Added

- The optional Fees parameter is now available on instant conversions, allowing platforms to charge users for FX services. More information [here](https://mangopay.com/docs/release-notes/millefeuille).
- Platforms can now use a quote to secure the rate for a conversion between two currencies for a set amount of time. More information [here](https://mangopay.com/docs/release-notes/millefeuille).
- Introduced the `uk_header_flag` boolean configuration key. Platforms partnered with Mangopay's UK entity should set this key to true for proper configuration.

## [3.32.0] - 2024-02-12
### Added

- New endpoint to look up metadata from BIN or Google Pay token. More information [here](https://mangopay.com/docs/release-notes/kisale)
- [Get a card validation endpoint](https://mangopay.com/docs/endpoints/card-validations#view-card-validation)

### Fixed

- Resolved an issue in our Python SDK where certain events were unable to process string-based IDs

## [3.31.0] - 2023-12-22
### Added

- New `CardInfo` parameter returned on card transactions. More information [here](https://mangopay.com/docs/release-notes/chilka).
- The IDEAL legacy implementation has been enhanced. You can now pass the `Bic`., and if provided, the API response will include the `BankName` parameter. More information [here](https://mangopay.com/docs/endpoints/web-card-payins#create-web-card-payin).

## [3.30.1] - 2023-11-09
### Added

It's now possible to specify an amount for DebitedFunds and Fees when you create a refund with `PayInRefund()`.

## [3.30.0] - 2023-11-02
### Updated
- Giropay and Ideal integrations with Mangopay have been improved.
- Klarna param "MerchantOrderId" has been renamed to "Reference"

### Added
- New Reference parameter for the new Paypal implementation. 

## [3.29.0] - 2023-09-29
### Added
- Instantly convert funds between 2 wallets of different currencies owned by the same user with the new SPOT FX endpoints

## [3.28.0] - 2023-09-18
### Added

- Multibanco, Satispay, Blik, Klarna are now available as a payment method with Mangopay. This payment method is in private beta. Please contact support if you have any questions.
- Card validation endpoint is now available (Private beta)

### Updated

- Google Pay integration & Paypal with Mangopay have been improved. These payment methods are in private beta. Please contact support if you have any questions.

### Fixed

- MBWay & PayPal are now using Web Execution Type.

## [3.27.2] - 2023-07-28
### Fixed

CIT/MIT should not set secure_mode #332 

## [3.27.1] - 2023-06-21
### Fixed

- `Phone` parameter instead of `PhoneNumber` for MBWay

## [3.27.0] - 2023-06-21
### Added

- MB WAY is now available as a payment method with Mangopay. This payment method is in private beta. Please contact support if you have any questions.

## [3.26.0] - 2023-03-17
### Added

Knowing when a dispute was closed is now possible thanks to the new ClosedDate parameter for the Dispute object.

The following endpoints have been updated accordingly:

[Vew a Dispute](ttps://docs.mangopay.com/endpoints/v2.01/disputes#e240_view-a-dispute)

[List Disputes for a User](https://docs.mangopay.com/endpoints/v2.01/disputes#e817_list-a-users-disputes)

[List Disputes for a Wallet](https://docs.mangopay.com/endpoints/v2.01/disputes#e816_list-a-wallets-disputes)

[List all Disputes](https://docs.mangopay.com/endpoints/v2.01/disputes#e241_list-all-disputes)

[List Disputes that need settling](https://docs.mangopay.com/endpoints/v2.01/disputes#e980_list-disputes-that-need-settling)

Please note that the new ClosedDate field will only display values for the Disputes closed after this release. Otherwise, a null value will be returned.

## [3.25.0] - 2023-01-12
### Added

Verifying some specific legal structures is now more efficient thanks to a new legal entity type: `PARTNERSHIP`.

The Legal User LegalPersonType parameter now includes the `PARTNERSHIP` value. The following endpoints have been updated accordingly:

[Create a Legal User (Payer)](https://docs.mangopay.com/endpoints/v2.01/users#e259_create-a-legal-user)

[Create a Legal User (Owner)](https://docs.mangopay.com/endpoints/v2.01/users#e1060_create-a-legal-user-owner)

[Update a Legal User](https://docs.mangopay.com/endpoints/v2.01/users#e261_update-a-legal-user)

Please note that changing the LegalPersonType to `PARTNERSHIP` for an existing user will automatically result in:

- A KYC downgrade to Light (default) verification
- The REGISTRATION_PROOF document being flagged as OUT_OF_DATE.

With this new LegalPersonType, the MANGOPAY team can better handle specific legal structures and speed up the validation process.



## [3.24.0] - 2022-12-22
### Added

#### New 30-day preauthorization feature

Preauthorizations can now hold funds for up to 30 days, therefore ensuring the solvency of a registered card for the same amount of time.

- The **Deposit** resource has been added with methods for creating, fetching and canceling a deposit
- The **CardPreAuthorizedDepositPayIn** resource has been added with methods for creating and fetching a CardPreAuthorizedDepositPayIn

Thanks to 30-day preauthorizations, MANGOPAY can provide a simpler and more flexible payment experience for a wide range of use cases, especially for rentals.

## [3.23.3] - 2022-12-06
### Fixed

- Removed the default value for `LEGAL_USER_TYPE_CHOICES` in order to prevent mistake on user update

## [3.23.2] - 2022-11-08
### Fixed 

- RecurringPayInRegistration total_amount type; 

### Added

- Missing event types

## [3.23.1] - 2022-10-26
### Fixed

- Tests after API update
- 313 Issue with fields for User (not mandatory for some cases)
- 310 fix for negative timestamp value fields in windows 

## [3.23.0] - 2022-09-14
### Added
**New country authorizations endpoints**

Country authorizations can now be viewed by using one of the following endpoints:

<a href="https://docs.mangopay.com/endpoints/v2.01/regulatory#e1061_the-country-authorizations-object">View a country's authorizations</a> <br>
<a href="https://docs.mangopay.com/endpoints/v2.01/regulatory#e1061_the-country-authorizations-object">View all countries' authorizations</a>

With these calls, it is possible to check which countries have:

- Blocked user creation
- Blocked bank account creation
- Blocked payout creation

Please refer to the <a href="https://docs.mangopay.com/guide/restrictions-by-country">Restrictions by country</a>
article for more information.

## [3.22.0] - 2022-06-29
## Added
**Recurring: €0 deadlines for CIT**

Setting free recurring payment deadlines is now possible for CIT (customer-initiated transactions) with the **FreeCycles** parameter.

The **FreeCycles** parameter allows platforms to define the number of consecutive deadlines that will be free. The following endpoints have been updated to take into account this new parameter:

<a href="https://docs.mangopay.com/endpoints/v2.01/payins#e1051_create-a-recurring-payin-registration">Create a Recurring PayIn Registration</a><br>
<a href="https://docs.mangopay.com/endpoints/v2.01/payins#e1056_view-a-recurring-payin-registration">View a Recurring PayIn Registration</a><br>

This feature provides new automation capabilities for platforms with offers such as “Get the first month free” or “free trial” subscriptions.

Please refer to the <a href="https://docs.mangopay.com/guide/recurring-payments-introduction">Recurring payments overview</a> documentation for more information.

## 3.21.0 - 2022.05.24
### Added 

#### UserCategory management

Users can now be differentiated depending on their MANGOPAY usage.

This is possible with the new UserCategory parameter, whose value can be set to:

- Payer – For users who are only using MANGOPAY to give money to other users (i.e., only pay).
- Owner – For users who are using MANGOPAY to receive funds (and who are therefore required to accept MANGOPAY’s terms and conditions).

Please note that the following parameters become required as soon as the UserCategory is set to “Owner”: 
- HeadquartersAddress
- CompanyNumber (if the LegalPersonType is “Business”)
- TermsAndConditionsAccepted.

The documentation of user-related endpoints has been updated and reorganised to take into account the new parameter:

[Create a Natural User (Payer)](https://docs.mangopay.com/endpoints/v2.01/users#e255_create-a-natural-user)
[Create a Natural User (Owner)](https://docs.mangopay.com/endpoints/v2.01/users#e1059_create-natural-user-owner)
[Update a Natural User](https://docs.mangopay.com/endpoints/v2.01/users#e260_update-a-natural-user)
[Create a Legal User (Payer)](https://docs.mangopay.com/endpoints/v2.01/users#e259_create-a-legal-user)
[Create a Legal User (Owner)](https://docs.mangopay.com/endpoints/v2.01/users#e1060_create-a-legal-user-owner)
[Update a Legal User](https://docs.mangopay.com/endpoints/v2.01/users#e261_update-a-legal-user)
[View a User](https://docs.mangopay.com/endpoints/v2.01/users#e256_view-a-user)
[List all Users](https://docs.mangopay.com/endpoints/v2.01/users#e257_list-all-users)

Differentiating the platform users results in a smoother user experience for “Payers” as they will have less declarative data to provide.


## 3.20.0 - 2022.05.12
### Added

#### Terms and conditions acceptance parameter

The acceptance of the MANGOPAY terms and conditions by the end user can now be registered via the SDK.

This information can be managed by using the new `TermsAndConditionsAccepted` parameter added to the `User` object.

The following API endpoints have been updated to take into account the new TermsAndConditionsAccepted parameter:

[Create a Natural User](https://docs.mangopay.com/endpoints/v2.01/users#e255_create-a-natural-user)
[Update a Natural User](https://docs.mangopay.com/endpoints/v2.01/users#e260_update-a-natural-user)
[Create a Legal User](https://docs.mangopay.com/endpoints/v2.01/users#e259_create-a-legal-user)
[Update a Legal User](https://docs.mangopay.com/endpoints/v2.01/users#e261_update-a-legal-user)
[View a User](https://docs.mangopay.com/endpoints/v2.01/users#e256_view-a-user)

Please note that:

- Existing users have to be updated to include the terms and conditions acceptance information.
- Once accepted, the terms and conditions cannot be revoked.


## 3.19.0 - 2022.03.31
### Added

#### Instant payment eligibility check

With the function
`PayOutEligibility(params).check_eligibility()`
the destination bank reachability can now be verified prior to making an instant payout. This results in a better user experience, as this preliminary check will allow the platform to propose the instant payout option only to end users whose bank is eligible. 


## 3.18.1 - 2022.02.18
### Fixed

- Refund for MIT/CIT has been fixed
- secure_mode parameter is not set anymore for CIT 


## 3.18.0 - 2021.11.19
## Added

### Instant payouts hooks

We are now providing new hooks for our new feature [Instant payouts](https://docs.mangopay.com/guide/instant-payment-payout) :

- INSTANT_PAYOUT_SUCCEEDED
- INSTANT_PAYOUT_FALLBACKED

It will allow you to trigger an action depends on the Instant Payout treatment.

### GET a RecurringPayIn ID

You can now request the RecurringPayIn ID to check if the status is valid using

## 3.17.0 - 2021.10.20
## Added

You can now change the status to "ENDED" for a recurring payment.

## Fixed

- "Status" is now available in the response when you request a recurring payment registration.

## 3.16.0 - 2021.10.11
## Added

**We provide more information regarding refused KYC documents.** Therefore it will be easier for you to adapt your app behavior and help your end user.

You are now able to see the exact explanation thanks to a new parameter called “Flags”. 

It has been added to 

`$this->_api->KycDocuments->Get($kycDocument->Id);`

It will display one or several error codes that provide the reason(s) why your document validation has failed. These error codes description are available [here](https://docs.mangopay.com/guide/kyc-document).

## 3.15.0 - 2021.09.30
## Added

As requested by numerous clients, we are now providing [Payconiq](https://www.payconiq.be/fr) as a new mean-of-payment. To request access, please contact MANGOPAY.

## Fixed 

+ BillingField & ShippingField are now optionals for RecurringPayIn
+ We have fixed DateTimeField (previously was generating an error due to format) 

## 3.14.1 - 2021.08.05
## Fixed 

- Change `FallbackReason` parameter's type to object in BankWirePayOut  

## 3.14.0 - 2021.08.04
## Added

- You can now update and view a Recurring PayIn Registration object. To know more about this feature, please consult the documentation [here](https://docs.mangopay.com/guide/recurring-payments-introduction). 
- To improve recurring payments, we have added new parameters for CIT : DebitedFunds & Fees. To know more about this feature, please consult the documentation [here](https://docs.mangopay.com/endpoints/v2.01/payins#e1053_create-a-recurring-payin-cit)

## 3.12.0 - 2021.06.10
## Added 

We have added a new feature **[recurring payments](https://docs.mangopay.com/guide/recurring-payments)** dedicated to clients needing to charge a card repeatedly, such as subscriptions or payments installments. 

You can start testing in sandbox, to help you define your workflow. This release provides the first elements of the full feature.

- [Create a Recurring PayIn Registration object](https://docs.mangopay.com/endpoints/v2.01/payins#e1051_create-a-recurring-payin-registration), containing all the information to define the recurring payment
- [Initiate your recurring payment flow](https://docs.mangopay.com/endpoints/v2.01/payins#e1053_create-a-recurring-payin-cit) with an authenticated transaction (CIT) using the Card Recurring PayIn endpoint
- [Continue your recurring payment flow](https://docs.mangopay.com/endpoints/v2.01/payins#e1054_create-a-recurring-payin-mit) with an non-authenticated transaction (MIT) using the Card Recurring PayIn endpoint

This feature is not yet available in production and you need to contact the Support team to request access.

## 3.11.0 - 2021.05.27
## Added 

Mangopay introduces the instant payment mode. It allows payouts (transfer from wallet to user bank account) to be processed within 25 seconds, rather than the 48 hours for a standard payout.

You can now use this new type of payout with the Python SDK.

Example :

```python
get_bank_wire = BankWirePayOut.get_bankwire(payout_id)
# where payout_id is the id of an existing payout
```

Please note that this feature must be authorized and activated by MANGOPAY. More information [here](https://docs.mangopay.com/guide/instant-payment-payout).

## Fixed

Duplicate BIC in resources 

## 3.10.1
## Fixed

## Fixed 

### IBAN for testing purposes

⚠️ **IBAN provided for testing purpose should never be used outside of a testing environement!**

- Fix `BankAccount` IBAN reference for tests

More information about how to test payments, click [here](https://docs.mangopay.com/guide/testing-payments).

### Others

- httplib2 has been updated to the last version
- RemainingFunds was flag wrongly as mandatory for PreAuthorization. It has been fixed.
- ProcessedDate had the type IntegerField instead of DateTimeField. It has been fixed.

## Added 

### New events for PreAuthorization

Some of you use a lot the [PreAuthorization](https://docs.mangopay.com/endpoints/v2.01/preauthorizations#e183_the-preauthorization-object) feature of our API. To make your life easier, we have added three new events :

- PREAUTHORIZATION_CREATED
- PREAUTHORIZATION_SUCCEEDED
- PREAUTHORIZATION_FAILED

The goal is to help you monitor a PreAuthorization with a [webhook](https://docs.mangopay.com/endpoints/v2.01/hooks#e246_the-hook-object).

*Example: If a PreAuthorization is desynchronized, when the status is updated, you will be able to know it.*

### Logging

We have merged @rbarrois pull request. The logging module expects user to provide the string as a first argument, and all interpolation parameters in separate positional or keyword arguments: `logger.debug("trying x=%s", x)`.

This brings two benefits:

- The interpolation is only performed if the logging message is actually
used (debug messages won't even be interpolated if logging is set to
WARNING)

- Monitoring libraries like Sentry can group messages based on their
non-interpolated message, which helps detecting similar issues.


## 3.10.0
## Added

### On demand feature for 3DSv2

> **This on-demand feature is for testing purposes only and will not be available in production**

#### Request

We've added a new parameter `Requested3DSVersion` (not mandatory) that allows you to choose between versions of 3DS protocols (managed by the parameter `SecureMode`). Two values are available: 
* `V1`
* `V2_1`

If nothing is sent, the flow will be 3DS V1. 

The `Requested3DSVersion` may be included on all calls to the following endpoints:
* `/preauthorizations/card/direct`
* `/payins/card/direct`

#### Response

In the API response, the `Requested3DSVersion` will show the value you requested:
* `V1`
* `V2_1`
* `null` – indicates that nothing was requested

The parameter `Applied3DSVersion` shows you the version of the 3DS protocol used. Two values are possible:
* `V1`
* `V2_1`

## 3.9.0
- 3DS2 integration with Shipping and Billing objects, including FirstName and LastName fields
The objects Billing and Shipping may be included on all calls to the following endpoints:
  - /preauthorizations/card/direct
  - /payins/card/direct
  - /payins/card/web
- Enable Instant Payment for payouts by adding a new parameter PayoutModeRequested on the following endpoint /payouts/bankwire
  - The new parameter PayoutModeRequested can take two differents values : "INSTANT_PAYMENT" or "STANDARD" (STANDARD = the way we procede normaly a payout request)
  - This new parameter is not mandatory and if empty or not present, the payout will be "STANDARD" by default
  - Instant Payment is in beta all over Europe - SEPA region
- Changed date to dateTime and fixed tests
- Changed User-Agent
- Fixed typo on IpAddress, FirstName & LastName
## 3.8.4
- Added 'Regulatory' endpoint to allow checks of User Block Status
- Added support for Regulatory -> Blocked Status Hooks
## 3.8.3
- added new methods for client fees wallet bank accounts and payouts
- added new method for PreAuthorization transactions
- fixed handler sandbox false condition
- added headers to APIError
- Improve logging calls. 

## 3.8.2
- Added missing 'creation_date' field to BankWirePayOut
- Handler has been modified in save function
- New RemainingFunds Parameters (Complete feature not fully activated, please listen for product announcements)
- Added CardValidation endpoint  (Complete feature not fully activated, please listen for product announcements)
- New MultiCapture Parameter in Preauthorization object (Complete feature not fully activated, please listen for product announcements)
- Added OUT_OF_DATE status for KYC docs
- Library upgrade httplib2
- "User-agent" format in the headers changed, aligned to other assets 

## [3.8.0]
### Added
- ApplePay Payins support has been added. Feel free to ask our Customer Success / Sales team about conditions and availability.
- GooglePay Payins support has been added. Feel free to ask our Customer Success / Sales team about conditions and availability too
- `GetEmoney` method now supports year and month parameters. More info on our [docs](https://docs.mangopay.com/endpoints/v2.01/user-emoney#e895_view-a-users-emoney)
- New `Dispute` reason type `COUNTERFEIT_PRODUCT` has been added.
- `Culture` parameter has been added for `Payin Direct`
- `Mandate` status `EXPIRED` and related `EventType` `MANDATE_EXPIRED` are now supported.
### Fixed
- `EMoney` amounts for a user are now available by month
- `Dispute` reason type `COUNTERFEIT_PRODUCT` is now available.
- UBOs can now be disactivated thanks to `isActive` property support.
- `Birthday` type is now a `Date` rather than an `Integer`

## [3.7.1] - 2019-09-24
### Fixed
- Fix issue on `UBODeclaration` creation

## [3.7.0] - 2019-07-09
### Added
- new [`UBODelaration`](https://docs.mangopay.com/endpoints/v2.01/ubo-declarations#e1024_the-ubo-declaration-object) submission system
- `CompanyNumber` support for [Legal `Users`](https://docs.mangopay.com/endpoints/v2.01/users#e259_create-a-legal-user)

 