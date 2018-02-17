import unittest
from datetime import datetime
from context import HistoryLine, GitHistoryParser, Project, HistoryEvent, Tracker


class HistoryEventTestSuite(unittest.TestCase):
    def setUp(self):
        self.project = Project.Project('test', '/tmp', '', '', '');
        self.tracker = Tracker.SimpleTracker(self.project)
        self.three_days_ago = datetime.strptime('2018-02-14 10:00:00', GitHistoryParser.GitHistoryParser.date_format)
        self.two_days_ago = datetime.strptime('2018-02-15 12:44:00', GitHistoryParser.GitHistoryParser.date_format)
        self.yesteraday = datetime.strptime('2018-02-16 12:44:00', GitHistoryParser.GitHistoryParser.date_format)
        self.today = datetime.strptime('2018-02-17 12:44:00', GitHistoryParser.GitHistoryParser.date_format)

    def testSimpleTrackerTracksCorrectly(self):
        # nothing was checked out today => we were working on one branch without checking out anything else
        event = HistoryEvent.HistoryEvent(
            HistoryEvent.HistoryLine(self.three_days_ago, 'integration'),
            HistoryEvent.HistoryTicketLine(self.three_days_ago, 'ABC-1', 'ABC-1'),
            self.project
        )
        self.tracker.events = [event]

        events = self.tracker.get_to_track(self.today.date())
        self.assertEqual(events[0], event)

    def testSimpleTrackerTracksSameDay(self):
        self.tracker.events = [
            HistoryEvent.HistoryEvent(
                HistoryEvent.HistoryLine(self.today, 'integration'),
                HistoryEvent.HistoryTicketLine(self.today, 'ABC-1', 'ABC-1'),
                self.project
            ),
            HistoryEvent.HistoryEvent(
                HistoryEvent.HistoryTicketLine(self.today, 'ABC-1', 'ABC-1'),
                HistoryEvent.HistoryTicketLine(self.today, 'ABC-2', 'ABC-2'),
                self.project
            ),
            HistoryEvent.HistoryEvent(
                HistoryEvent.HistoryTicketLine(self.today, 'ABC-2', 'ABC-2'),
                HistoryEvent.HistoryLine(self.today, 'integration'),
                self.project
            ),
            HistoryEvent.HistoryEvent(
                HistoryEvent.HistoryLine(self.today, 'integration'),
                HistoryEvent.HistoryTicketLine(self.today, 'ABC-2', 'ABC-2'),
                self.project
            ),
            HistoryEvent.HistoryEvent(
                HistoryEvent.HistoryTicketLine(self.today, 'ABC-2', 'ABC-2'),
                HistoryEvent.HistoryLine(self.today, 'integration'),
                self.project
            ),
            HistoryEvent.HistoryEvent(
                HistoryEvent.HistoryLine(self.today, 'integration'),
                HistoryEvent.HistoryLine(self.today, 'master'),
                self.project
            ),
        ]

        events = self.tracker.get_to_track(self.today.date())
        self.assertEqual(3, len(events))
        self.assertEqual('ABC-1', events[0].get_ticket())
        self.assertEqual('ABC-2', events[1].get_ticket())
        self.assertEqual('ABC-2', events[2].get_ticket())

    def testTracksAlreadyCheckedOutTicketInTheMorning(self):
        self.tracker.events = [
            HistoryEvent.HistoryEvent(
                HistoryEvent.HistoryTicketLine(self.today, 'ABC-1', 'ABC-1'),
                HistoryEvent.HistoryTicketLine(self.today, 'ABC-2', 'ABC-2'),
                self.project
            ),
            HistoryEvent.HistoryEvent(
                HistoryEvent.HistoryTicketLine(self.today, 'ABC-2', 'ABC-2'),
                HistoryEvent.HistoryLine(self.today, 'integration'),
                self.project
            ),
        ]

        events = self.tracker.get_to_track(self.today.date())
        self.assertEqual(2, len(events))
        self.assertEqual('ABC-1', events[0].get_ticket())
        self.assertEqual('ABC-2', events[1].get_ticket())
