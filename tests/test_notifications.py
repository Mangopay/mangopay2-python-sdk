# -*- coding: utf-8 -*-

from datetime import datetime
import json
import pytz

from tests import settings
from tests.resources import Notification, Event
from tests.test_base import BaseTest

import responses


class NotificationsTest(BaseTest):
    @responses.activate
    def test_create_notifications(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/hooks',
                'body': {
                    "Url": "http://wwww.mynotificationurl.com",
                    "Status": "DISABLED",
                    "Validity": "VALID",
                    "EventType": "PAYIN_NORMAL_SUCCEEDED",
                    "Id": "1248727",
                    "Tag": "custom tag",
                    "CreationDate": 1392808584
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/hooks/1248727',
                'body': {
                    "Url": "http://wwww.mynotificationurl.com",
                    "Status": "DISABLED",
                    "Validity": "VALID",
                    "EventType": "PAYIN_NORMAL_SUCCEEDED",
                    "Id": "1248727",
                    "Tag": "custom tag",
                    "CreationDate": 1392808584
                },
                'status': 200
            },
            {
                'method': responses.PUT,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/hooks/1248727',
                'body': {
                    "Url": "http://wwww.mynotificationurl.com",
                    "Status": "ENABLED",
                    "Validity": "VALID",
                    "EventType": "PAYIN_NORMAL_SUCCEEDED",
                    "Id": "1248727",
                    "Tag": "custom tag",
                    "CreationDate": 1392808584
                },
                'status': 200
            }])

        params = {
            "url": "http://wwww.mynotificationurl.com",
            "event_type": "PAYIN_NORMAL_SUCCEEDED",
            "tag": "custom tag"
        }
        notification = Notification(**params)
        notification.save()

        for key, value in params.items():
            self.assertEqual(getattr(notification, key), value)

        self.assertIsNotNone(notification.get_pk())

        previous_pk = notification.get_pk()

        notification.status = 'ENABLED'
        notification.save()

        self.assertEqual(previous_pk, notification.get_pk())

        self.assertEqual(notification.status, 'ENABLED')

    @responses.activate
    def test_retrieve_notification(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/hooks',
                'body': {
                    "Url": "http://wwww.mynotificationurl.com",
                    "Status": "DISABLED",
                    "Validity": "VALID",
                    "EventType": "PAYIN_NORMAL_SUCCEEDED",
                    "Id": "1248727",
                    "Tag": "custom tag",
                    "CreationDate": 1392808584
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/hooks/1248727',
                'body': {
                    "Url": "http://wwww.mynotificationurl.com",
                    "Status": "DISABLED",
                    "Validity": "VALID",
                    "EventType": "PAYIN_NORMAL_FAILED",
                    "Id": "1248727",
                    "Tag": "custom tag",
                    "CreationDate": 1392808584
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/hooks/1248728',
                'body': {"errors": []},
                'status': 404
            }])

        params = {
            "url": "http://wwww.mynotificationurl.com",
            "event_type": "PAYIN_NORMAL_FAILED",
            "tag": "custom tag"
        }
        notification = Notification(**params)
        notification.save()

        self.assertRaises(Notification.DoesNotExist, Notification.get, int(notification.get_pk()) + 1)

        self.assertIsNotNone(notification.get_pk())

        notification = Notification.get(notification.get_pk())

        self.assertIsNotNone(notification.get_pk())

        for key, value in params.items():
            self.assertEqual(getattr(notification, key), value)

    @responses.activate
    def test_retrieve_all_notifications(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/hooks',
                'body': {
                    "Url": "http://wwww.mynotificationurl.com",
                    "Status": "DISABLED",
                    "Validity": "VALID",
                    "EventType": "PAYIN_NORMAL_SUCCEEDED",
                    "Id": "1248727",
                    "Tag": "custom tag",
                    "CreationDate": 1392808584
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/hooks',
                'body': [
                    {
                        "Url": "http://requestb.in/s6koy4s6ZLKJZLEKAJZE",
                        "Status": "ENABLED",
                        "Validity": "INVALID",
                        "EventType": "PAYIN_NORMAL_CREATED",
                        "Id": "1234996",
                        "Tag": "custom tag",
                        "CreationDate": 1392132200
                    },
                    {
                        "Url": "http://requestb.in/1fkbk9b1",
                        "Status": "ENABLED",
                        "Validity": "VALID",
                        "EventType": "PAYIN_NORMAL_FAILED",
                        "Id": "1234997",
                        "Tag": "custom tag",
                        "CreationDate": 1392132216
                    },
                    {
                        "Url": "http://requestb.in/1fkbk9b1",
                        "Status": "ENABLED",
                        "Validity": "VALID",
                        "EventType": "PAYIN_NORMAL_SUCCEEDED",
                        "Id": "1235015",
                        "Tag": "custom tag",
                        "CreationDate": 1392133969
                    }
                ],
                'status': 200
            }])

        params = {
            "url": "http://wwww.mynotificationurl.com",
            "event_type": "PAYOUT_NORMAL_SUCCEEDED",
            "tag": "custom tag"
        }
        notification = Notification(**params)
        notification.save()

        notifications_page = Notification.all()

        self.assertIsInstance(notifications_page.data, list)

        for notification in notifications_page:
            self.assertIsInstance(notification, Notification)

    @responses.activate
    def test_retrieve_all_events(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/hooks',
                'body': {
                    "Url": "http://wwww.mynotificationurl.com",
                    "Status": "DISABLED",
                    "Validity": "VALID",
                    "EventType": "PAYIN_NORMAL_SUCCEEDED",
                    "Id": "1248727",
                    "Tag": "custom tag",
                    "CreationDate": 1392808584
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/events',
                'body': [
                    {
                        "RessourceId": "88263",
                        "EventType": "PAYIN_NORMAL_CREATED",
                        "Date": 1383066833
                    },
                    {
                        "RessourceId": "88265",
                        "EventType": "PAYIN_NORMAL_CREATED",
                        "Date": 1383067144
                    }
                ],
                'status': 200
            }])

        params = {
            "url": "http://wwww.mynotificationurl.com",
            "event_type": "TRANSFER_NORMAL_SUCCEEDED",
            "tag": "custom tag"
        }
        notification = Notification(**params)
        notification.save()

        events_page = Event.all()

        self.assertIsInstance(events_page.data, list)

        for event in events_page:
            self.assertIsInstance(event, Event)

    @responses.activate
    def test_event_timestamp_from_timezone_aware_date(self):
        """
        Creating an event with a timezone aware date should not break
        and should generate the correct timestamp.
        """
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/events',
                'body': {
                    "RessourceId": "88263",
                    "EventType": "PAYIN_NORMAL_CREATED",
                    "Date": 1383066833
                },
                'status': 200
            }])
        event = Event(date=datetime(2016, 1, 1, 10).replace(tzinfo=pytz.utc))
        event.save()
        content = json.loads(responses.calls[0].request.body)
        self.assertEqual(content['Date'], 1451642400)
