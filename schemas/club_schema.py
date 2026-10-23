success_create_club = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "bookTitle": {
            "type": "string"
        },
        "bookAuthors": {
            "type": "string"
        },
        "publicationYear": {
            "type": "integer"
        },
        "description": {
            "type": "string"
        },
        "telegramChatLink": {
            "type": "string"
        },
        "owner": {
            "type": "integer"
        },
        "members": {
            "type": "array",
            "items": {
                "type": "integer"
            }
        },
        "reviews": {
            "type": "array",
            "items": {
                "type": "object"
            }
        },
        "created": {
            "type": "string"
        },
        "modified": {
            "type": ["string", "null"]
        }
    },
    "required": [
        "id",
        "bookTitle",
        "bookAuthors",
        "publicationYear",
        "description",
        "telegramChatLink",
        "owner",
        "members",
        "reviews",
        "created",
        "modified"
    ]
}