import urllib.parse
from collections import namedtuple

Attachment = namedtuple('Attachment', ['title', 'url'])


class Proclamation:
    def __init__(self, columns, base_url):
        self._base_url = base_url
        self._parse(columns)

    def _safe_assign(self, columns, left_str, right_str):
        try:
            exec("{} = {}".format(left_str, right_str))
        except Exception as e:
            exec("{} = ''".format(left_str))

    def _parse(self, columns):
        parts = [
            ("self._proclamation_number", "columns[0].contents[0].text"),
            ("self._proclamation_date", "str(columns[0].contents[2]) if len(columns[0].contents) == 7 else ''"),
            ("self._publication_date", "str(columns[0].contents[6]) if len(columns[0].contents) == 7 else str(columns[0].contents[4])"),
            ("self._title", "str(columns[1].contents[0])"),
            ("self._amount", "columns[1].contents[2].text.split(': ')[1]"),
            ("self._type", "columns[2].text"),
            ("self._location", "columns[3].text"),
            ("self._department", "columns[4].text"),
            ("self._competition_date", "columns[5].text"),
            ("self._submission_deadline", "columns[6].text"),
            ("self._inquiry_deadline", "columns[7].text")
        ]

        for p in parts:
            self._safe_assign(columns, p[0], p[1])

        self._attachments = []
        for a in columns[8].find_all('a'):
            full_url = urllib.parse.urljoin(self._base_url, a.attrs['href'])
            self._attachments.append(Attachment(a.attrs['title'], full_url))

    def __repr__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())

    @property
    def proclamation_number(self):
        return self._proclamation_number

    @property
    def proclamation_date(self):
        return self._proclamation_date

    @property
    def publication_date(self):
        return self._publication_date

    @property
    def title(self):
        return self._title

    @property
    def amount(self):
        return self._amount

    @property
    def type(self):
        return self._type

    @property
    def location(self):
        return self._location

    @property
    def department(self):
        return self._department

    @property
    def competition_date(self):
        return self._competition_date

    @property
    def submission_deadline(self):
        return self._submission_deadline

    @property
    def inquiry_deadline(self):
        return self._inquiry_deadline

    @property
    def attachments(self):
        return self._attachments
