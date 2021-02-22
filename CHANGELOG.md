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

 
