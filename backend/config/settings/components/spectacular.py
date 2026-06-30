from config.settings.env import env

API_TITLE = env("API_TITLE", default="LWNF Backend API")
API_DESCRIPTION = env(
    "API_DESCRIPTION",
    default="REST API for the LWNF platform.",
)
API_VERSION = env("API_VERSION", default="v1")
API_TERMS = env("API_TERMS_URL", default="")
API_CONTACT_NAME = env("API_CONTACT_NAME", default="LWNF")
API_CONTACT_EMAIL = env("API_CONTACT_EMAIL", default="")
API_CONTACT_URL = env("API_CONTACT_URL", default="")
API_LICENSE_NAME = env("API_LICENSE_NAME", default="Proprietary")
API_LICENSE_URL = env("API_LICENSE_URL", default="")
API_SERVER_URL = env("API_SERVER_URL", default="http://localhost:8000")

SPECTACULAR_SETTINGS = {
    "TITLE": API_TITLE,
    "DESCRIPTION": API_DESCRIPTION,
    "VERSION": API_VERSION,
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PUBLIC": True,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_SPLIT_PATCH": True,
    "SORT_OPERATIONS": True,
    "SORT_OPERATION_PARAMETERS": True,
    "CAMELIZE_NAMES": False,
    "ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE": False,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayRequestDuration": True,
        "persistAuthorization": True,
        "filter": True,
        "tryItOutEnabled": True,
    },
    "REDOC_UI_SETTINGS": {
        "hideDownloadButton": False,
    },
    "CONTACT": {
        "name": API_CONTACT_NAME,
        "email": API_CONTACT_EMAIL,
        "url": API_CONTACT_URL,
    },
    "LICENSE": {
        "name": API_LICENSE_NAME,
        "url": API_LICENSE_URL,
    },
    "TERMS_OF_SERVICE": API_TERMS,
    "SERVERS": [
        {
            "url": API_SERVER_URL,
            "description": "Current API Server",
        },
    ],
    "SECURITY": [
        {
            "BearerAuth": [],
        }
    ],
    "SECURITY_SCHEMES": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    },
    "TAGS": [
        {"name": "Authentication"},
        {"name": "Users"},
        {"name": "Children"},
        {"name": "Sponsors"},
        {"name": "Projects"},
        {"name": "Events"},
        {"name": "Blog"},
        {"name": "Donations"},
        {"name": "Admin"},
    ],
}