success_auth = {
    "type": "object",
    "properties": {
        "access": {"type": "string"},
        "refresh": {"type": "string"}
    },
    "required": ["access", "refresh"]
}

missing_username_auth = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "username": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["username"]
}

missing_password_auth = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "password": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["password"]
}

wrong_credentials_auth = {
    "type": "object",
    "properties": {
        "detail": {"type": "string"}
    },
    "required": ["detail"]
}

unsupported_media_type = {
    "type": "object",
    "properties": {
        "detail": {"type": "string"}
    },
    "required": ["detail"]
}