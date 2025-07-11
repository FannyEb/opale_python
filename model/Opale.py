from datetime import datetime

class Opale:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return (f"Opale(id={self.id}, name='{self.name}', "
                f"created={self.created}, updated={self.updated}, status='{self.status}')")

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            created=data.get("created"),
            updated=data.get("updated"),
            status=data.get("status")
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "status": self.status
        }
