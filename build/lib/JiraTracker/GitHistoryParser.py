import re
import HistoryLine
from HistoryEvent import HistoryEvent
from Exceptions import ParseException
from datetime import datetime
from Project import Project


class GitHistoryParser(object):
    date_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, project):
        assert (isinstance(project, Project))
        self.project = project

    def parse_line(self, line):
        assert (isinstance(line, str))
        try:
            parts = line.split('|')
            match = re.search(self.project.get_name() + '-\d+', parts[1])

            if match:
                return HistoryLine.HistoryTicketLine(datetime.strptime(parts[0], self.date_format), parts[1], match.group(0))

            return HistoryLine.HistoryNonTicketLine(datetime.strptime(parts[0], self.date_format), parts[1])
        except Exception:
            raise ParseException('Could not parse line \'' + line + '\' in project ' + self.project.get_name())

    def parse_history(self, history_lines):
        events = []
        for line_number in range(len(history_lines)):
            line = self.parse_line(history_lines[line_number])
            try:
                next_line = self.parse_line(history_lines[line_number + 1])
                if next_line.get_time() < line.get_time():
                    raise ParseException('Branch ' + next_line.get_branch() + ' was checked out at ' + next_line.get_time().strftime(self.date_format) + ' which is not possible as previous line was checked out later')
            except IndexError:
                return events
            finally:
                events.append(HistoryEvent(line, next_line, self.project))

