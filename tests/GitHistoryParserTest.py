import unittest
import datetime
from context import GitHistoryParser, HistoryLine, Exceptions, Project, HistoryEvent


class GitHistoryParserTestSuite(unittest.TestCase):
    def testParsesTicketLine(self):
        test_data = {
            '2018-02-12 22:20:00|feature/ABC-123': [datetime.datetime(2018, 2, 12, 22, 20, 00), 'ABC-123', 'ABC'],
            '1970-01-01 00:00:00|ABC-0': [datetime.datetime(1970, 1, 1, 0, 0, 0), 'ABC-0', 'ABC'],
        }
        for line in test_data.keys():
            parser = GitHistoryParser.GitHistoryParser(Project.Project('ABC', '/tmp', '', '', ''))
            parsed_line = parser.parse_line(line)

            self.assertIsInstance(parsed_line, HistoryLine.HistoryTicketLine)
            self.assertEqual(parsed_line.get_time(), test_data[line][0])
            self.assertEqual(parsed_line.get_branch(), line.split('|')[1])
            self.assertEqual(parsed_line.get_ticket(), test_data[line][1])

    def testParsesNonTicketLine(self):
        test_data = {
            '2018-02-12 22:20:00|master': [datetime.datetime(2018, 2, 12, 22, 20, 00), 'ABC'],
            '1970-01-01 00:00:00|integration': [datetime.datetime(1970, 1, 1, 0, 0, 0), 'Z'],
            '1970-01-01 00:00:00|ABC-123': [datetime.datetime(1970, 1, 1, 0, 0, 0), 'Z'],
        }
        for line in test_data.keys():
            parser = GitHistoryParser.GitHistoryParser(Project.Project('test', '/tmp', '', '', ''))
            parsed_line = parser.parse_line(line)

            self.assertIsInstance(parsed_line, HistoryLine.HistoryNonTicketLine)
            self.assertEqual(parsed_line.get_time(), test_data[line][0])
            self.assertEqual(parsed_line.get_branch(), line.split('|')[1])

    def testThrowsExceptionWhenNotParsable(self):
        test_data = ['', '1970-01-00 00:00:00|integration' '1970-01-01 00:00:00|']
        for line in range(len(test_data)):
            parser = GitHistoryParser.GitHistoryParser(Project.Project('ABC', '/tmp', '', '', ''))
            with self.assertRaises(Exceptions.ParseException) as e:
                parser.parse_line(test_data[line])
            self.assertEqual('Could not parse line \'' + test_data[line] + '\' in project ABC',
                             e.exception.message)

    def testParsesHistoryCorrectly(self):
        project = Project.Project('ABC', '/tmp', '', '', '')
        lines = [
            '2018-02-12 22:20:00|feature/ABC-123',
            '2018-02-12 22:30:00|feature/ABC-124',
            '2018-02-12 22:40:00|feature/ABC-125',
            '2018-02-12 22:50:00|master',
            '2018-02-12 22:59:00|feature/ABC-125',
            '2018-02-13 22:50:00|integration',
            '2018-02-14 10:00:00|feature/ABC-124',
            '2018-02-16 10:00:00|feature/ABC-123',

        ]
        parsed_lines = [
            HistoryLine.HistoryTicketLine(datetime.datetime(2018, 2, 12, 22, 20, 00), 'feature/ABC-123', 'ABC-123'),
            HistoryLine.HistoryTicketLine(datetime.datetime(2018, 2, 12, 22, 30, 00), 'feature/ABC-124', 'ABC-124'),
            HistoryLine.HistoryTicketLine(datetime.datetime(2018, 2, 12, 22, 40, 00), 'feature/ABC-125', 'ABC-125'),
            HistoryLine.HistoryNonTicketLine(datetime.datetime(2018, 2, 12, 22, 50, 00), 'master'),
            HistoryLine.HistoryTicketLine(datetime.datetime(2018, 2, 12, 22, 59, 00), 'feature/ABC-125', 'ABC-125'),
            HistoryLine.HistoryNonTicketLine(datetime.datetime(2018, 2, 13, 22, 50, 00), 'integration'),
            HistoryLine.HistoryTicketLine(datetime.datetime(2018, 2, 14, 10, 00, 00), 'feature/ABC-124', 'ABC-124'),
            HistoryLine.HistoryTicketLine(datetime.datetime(2018, 2, 16, 10, 00, 00), 'feature/ABC-123', 'ABC-123'),
            ]

        expected_events = [
            HistoryEvent.HistoryEvent(parsed_lines[0], parsed_lines[1], project),
            HistoryEvent.HistoryEvent(parsed_lines[1], parsed_lines[2], project),
            HistoryEvent.HistoryEvent(parsed_lines[2], parsed_lines[3], project),
            HistoryEvent.HistoryEvent(parsed_lines[3], parsed_lines[4], project),
            HistoryEvent.HistoryEvent(parsed_lines[4], parsed_lines[5], project),
            HistoryEvent.HistoryEvent(parsed_lines[5], parsed_lines[6], project),
            HistoryEvent.HistoryEvent(parsed_lines[6], parsed_lines[7], project),
        ]

        parser = GitHistoryParser.GitHistoryParser(project)
        result_events = parser.parse_history(lines)

        for e in range(len(expected_events)):
            self.assertEqual(expected_events[e], result_events[e])

    def testDetectsWrongDatesOrder(self):
        project = Project.Project('test', '/tmp', '', '', '')
        lines = [
            '2018-02-12 22:20:00|feature/ABC-123',
            '2018-02-12 22:19:00|feature/ABC-124',
        ]

        parser = GitHistoryParser.GitHistoryParser(project)
        with self.assertRaises(Exceptions.ParseException) as e:
            parser.parse_history(lines)

        self.assertEqual(
            e.exception.message,
            'Branch feature/ABC-124 was checked out at 2018-02-12 22:19:00 which is not possible as previous line was checked out later'
        )


if __name__ == '__main__':
    unittest.main()
