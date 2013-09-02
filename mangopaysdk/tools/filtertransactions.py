class FilterTransactions:

    # TransactionStatus {CREATED, SUCCEEDED, FAILED}
    Status = None

    # TransactionType {PAYIN, PAYOUT, TRANSFER}
    Type = None

    #TransactionNature { REGULAR, REFUND, REPUDIATION }
    Nature = None

    # TransactionDirection {DEBIT, CREDIT}
    Direction = None

    # Start date in unix format: return only transactions that have CreationDate BEFORE this date
    BeforeDat = None

    # End date in unix format: return only transactions that have CreationDate AFTER this date
    AfterDate = None