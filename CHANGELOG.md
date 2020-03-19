## [Unreleased]

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

 
