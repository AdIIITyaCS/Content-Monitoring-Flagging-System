CONTENT MONITORING AND FLAGGING SYSTEM
PROJECT OVERVIEW
This backend system is designed to monitor external content and flag
specific keyword matches for manual review. The project is built
using Django and Python, focusing on efficient data modeling and
specific business logic for scoring and suppression.

TECHNICAL STACK
Django,Django REST Framework,SQLite

DATA MODELS
Keyword: Stores monitoring targets.
ContentItem: Stores titles, bodies, and sources of ingested content.
Flag: Links keywords to content with a calculated score and status.

CORE LOGIC
SCORING MECHANISM
Matches are scored based on location and type:
Exact match in title: 100 points.
Partial match in title: 70 points.
Keyword found in body only: 40 points.

SUPPRESSION RULES:
This is the most critical business rule:
If a reviewer marks a flag as irrelevant, it is suppressed from future scans.
A suppressed item only reappears if the last_updated timestamp on the content changes.

API ENDPOINTS:
POST /keywords/     : Create a new keyword.
POST /scan/         : Trigger the content scanning process.
GET /flags/         : Retrieve generated flags for review.
PATCH /flags/{id}/  : Update the status of a flag.

SETUP INSTRUCTIONS:
Install dependencies via pip.
Run "python manage.py migrate" to set up the SQLite database.
Run "python manage.py runserver" to start the backend.
Trigger a scan via the /scan/ endpoint using either mock data or a public API.
