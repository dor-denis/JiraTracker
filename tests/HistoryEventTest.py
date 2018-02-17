import unittest
import datetime
from context import HistoryLine, GitHistoryParser, Project, HistoryEvent


class HistoryEventTestSuite(unittest.TestCase):
    def testCalculatesSameDayTicketBranchSwitch(self):
        line1 = HistoryLine.HistoryTicketLine(
            datetime.datetime.strptime('2018-02-17 12:52:25', GitHistoryParser.GitHistoryParser.date_format),
            'feature/ABC-1',
            'ABC-1'
        )
        line2 = HistoryLine.HistoryTicketLine(
            datetime.datetime.strptime('2018-02-17 14:52:25', GitHistoryParser.GitHistoryParser.date_format),
            'feature/ABC-2',
            'ABC-2'
        )
        history_event = HistoryEvent.HistoryEvent(line1, line2, Project.Project('test', '/tmp', '', '', ''))

        expected_time_diff = datetime.timedelta(hours=2)
        self.assertEqual(history_event.get_time_diff(), expected_time_diff)
