from datetime import datetime

class Task:
    def __init__(self, id, title, date, linkJira, linkSpec, opale, endDate):
        self.id = id
        self.title = title
        self.date = datetime.fromisoformat(date) if date else None
        self.linkJira = linkJira
        self.linkSpec = linkSpec
        self.opale = opale
        self.endDate = datetime.fromisoformat(endDate) if endDate else None

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', date={self.date}, endDate={self.endDate})"

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            date=data.get("date"),
            linkJira=data.get("linkJira"),
            linkSpec=data.get("linkSpec"),
            opale=data.get("opale"),
            endDate=data.get("endDate")
        )
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date.isoformat() if isinstance(self.date, datetime) else self.date,
            "linkJira": self.linkJira,
            "linkSpec": self.linkSpec,
            "opale": self.opale,
            "endDate": self.endDate.isoformat() if isinstance(self.endDate, datetime) else self.endDate,
        }


