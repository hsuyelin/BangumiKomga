# get access token from: https://next.bgm.tv/demo/access-token
BANGUMI_ACCESS_TOKEN = 'SXXXXXXXXXXXXXXX'
KOMGA_BASE_URL = "http://IP:PORT"
KOMGA_EMAIL = "email"
KOMGA_EMAIL_PASSWORD = "password"
KOMGA_LIBRARY_LIST = []
KOMGA_COLLECTION_LIST = []

RECHECK_FAILED_SERIES = False
RECHECK_FAILED_BOOKS = False

CREATE_FAILED_COLLECTION = False

# support 'GOTIFY', 'WEBHOOK', 'HEALTHCHECKS'
NOTIF_TYPE_ENABLE = []

NOTIF_GOTIFY_ENDPOINT = "http://IP:PORT"
NOTIF_GOTIFY_TOKEN = "TOKEN"
NOTIF_GOTIFY_PRIORITY = 1
NOTIF_GOTIFY_TIMEOUT = 10

NOTIF_WEBHOOK_ENDPOINT = "http://IP:PORT"
NOTIF_WEBHOOK_METHOD = "POST"
NOTIF_WEBHOOK_HEADER = {"Content-Type": "application/json"}
NOTIF_WEBHOOK_TIMEOUT = 10

NOTIF_HEALTHCHECKS_ENDPOINT = "http://IP:PORT"
NOTIF_HEALTHCHECKS_TIMEOUT = 10

# Poster
USE_BANGUMI_THUMBNAIL=False
USE_BANGUMI_THUMBNAIL_FOR_BOOK=False