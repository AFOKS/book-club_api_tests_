success_register_user = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "username": {
            "type": "string"
        },
        "firstName": {
            "type": "string"
        },
        "lastName": {
            "type": "string"
        },
        "email": {
            "type": "string"
        },
        "remoteAddr": {
            "type": "string"
        }
    },
    "required": [
        "id",
        "username",
        "firstName",
        "lastName",
        "email",
        "remoteAddr"
    ]
}

register_user_bad_request = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "username": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "password": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": [
        "username",
        "password"
    ]
}

register_user_missing_username = {
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

register_user_missing_password = {
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

register_user_duplicate_username = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "username": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["username"]
}