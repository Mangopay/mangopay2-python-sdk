class FilterDisputeDocuments:

    Status = None

    Type = None

    Nature = None

    # Start date in unix format: return only objects that have CreationDate BEFORE this date
    BeforeDate = None

    # End date in unix format: return only objects that have CreationDate AFTER this date
    AfterDate = None
