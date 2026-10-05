CLUBS_LIST_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["count", "next", "previous", "results"],
    "properties": {
        "count": {"type": "integer", "minimum": 0},
        "next": {"type": ["string", "null"]},
        "previous": {"type": ["string", "null"]},
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "id", "bookTitle", "bookAuthors", "publicationYear",
                    "description", "telegramChatLink", "owner",
                    "members", "reviews", "created", "modified"
                ],
                "properties": {
                    "id": {"type": "integer"},
                    "bookTitle": {"type": "string"},
                    "bookAuthors": {"type": "string"},
                    "publicationYear": {"type": ["integer", "null"]},
                    "description": {"type": ["string", "null"]},
                    "telegramChatLink": {"type": ["string", "null"]},
                    "owner": {"type": "integer"},
                    "members": {"type": "array", "items": {"type": "integer"}},
                    "reviews": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["id", "club", "user", "review",
                                         "assessment", "readPages", "created", "modified"],
                            "properties": {
                                "id": {"type": "integer"},
                                "club": {"type": "integer"},
                                "user": {
                                    "type": "object",
                                    "required": ["id", "username"],
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "username": {"type": "string"},
                                    },
                                },
                                "review": {"type": ["string", "null"]},
                                "assessment": {"type": ["integer", "null"]},
                                "readPages": {"type": ["integer", "null"]},
                                "created": {"type": "string"},
                                "modified": {"type": ["string", "null"]},
                            },
                        },
                    },
                    "created": {"type": "string"},
                    "modified": {"type": ["string", "null"]},
                },
            },
        },
    },
}
