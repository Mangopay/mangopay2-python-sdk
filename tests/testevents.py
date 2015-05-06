import random, string
from tests.testbase import TestBase
from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.types.pagination import Pagination
from mangopaysdk.tools.sorting import Sorting
from mangopaysdk.tools.filtertransactions import FilterTransactions
from mangopaysdk.types.exceptions.responseexception import ResponseException
from mangopaysdk.entities.userlegal import UserLegal
from mangopaysdk.entities.bankaccount import BankAccount
from mangopaysdk.entities.event import Event
from mangopaysdk.tools.enums import *


class Test_ApiEvents(TestBase):

    def test_Events_GetEvents(self):
        sorting = Sorting()
        sorting.AddField("Date", "desc")
        events = self.sdk.events.Get(None, None, sorting)
        self.assertTrue(events[0].Date > events[len(events) - 1].Date)

        sorting = Sorting()
        sorting.AddField("Date", "asc")
        events = self.sdk.events.Get(None, None, sorting)
        self.assertTrue(events[0].Date < events[len(events) - 1].Date)

        self.assertNotEqual(events[0].ResourceId, None)
        self.assertNotEqual(events[0].ResourceId, '')
        self.assertNotEqual(events[0].EventType, None)
        self.assertNotEqual(events[0].EventType, '')
        self.assertNotEqual(events[0].Date, None)
        self.assertNotEqual(events[0].Date, '')

    def test_Events_GetEvents_Page_Of_Type(self):
        self.pageLength = 3
        pagination = Pagination(1, self.pageLength)
        filter = FilterTransactions()
        self.type = EventType.PAYIN_NORMAL_CREATED
        filter.EventType = self.type

        event = self.sdk.events.Get(pagination, filter)
        self.assertTrue(len(event) <= self.pageLength)
        if (len(event) > 0):
            self.assertEqual(event[0].EventType, self.type)
        if (len(event) > 1):
            self.assertEqual(event[1].EventType, self.type)
        if (len(event) > 2):
            self.assertEqual(event[2].EventType, self.type)
       