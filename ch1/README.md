# Content Monitoring & Flagging System

## Overview
This is a backend service built with Django and Django REST Framework (DRF) that monitors simulated incoming content, matches it against a set of predefined keywords, and flags items for reviewer review.

## Prerequisites
- Python 3.10+
- pip (Python package installer)

## Setup Instructions

1. **Navigate to the project directory**
   Open your terminal and make sure you are in the `ch1` folder (where `manage.py` is located).

2. **Create and Activate a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install django djangorestframework
   ```

4. **Run Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (For Django Admin Access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

## How to Test the Application

1. **Add Keywords via Django Admin**
   - Go to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.
   - Add some Keywords (e.g., "python", "django", "recipe").

2. **Run the Scanner (Trigger Mock Data Scan)**
   - Open your browser or API client (Postman/curl) to: `http://127.0.0.1:8000/api/scan/`
   - Send a `POST` request. This will scan the hardcoded mock content against your keywords.

3. **View Flags**
   - Visit: `http://127.0.0.1:8000/api/flags/`
   - You will see the generated flags with their respective scores.

4. **Reviewer Action (Update Flag Status)**
   - Visit a specific flag URL (e.g., `http://127.0.0.1:8000/api/flags/1/`).
   - Use the DRF Browsable API interface at the bottom to send a `PATCH` request with the JSON payload:
     ```json
     {
         "status": "irrelevant"
     }
     ```

5. **Test Suppression Logic**
   - Run the scanner again (`POST /api/scan/`).
   - Verify that the previously marked 'irrelevant' flag did NOT revert back to 'pending'. This satisfies the core suppression requirement.

## Assumptions & Trade-offs

1. **Separation of Concerns (Service Layer)**
   Instead of writing the scanning and matching logic directly inside `views.py` or the `models.py`, all business logic is encapsulated in `core/services.py` (`ScannerService`). This keeps views thin and adheres to software engineering best practices.

2. **Mock Data Handling**
   The assignment didn't require a live external content API integration. Therefore, the mock JSON response representing fetched articles/content is hardcoded inside the `ScannerService.get_mock_data()` method. It mimics the structure expected from an external source.

3. **Suppression Mechanism**
   The suppression logic relies on timestamps. If a `Flag` is marked as `'irrelevant'`, the scanner compares the `last_updated` datetime of the `ContentItem` against the `updated_at` datetime of the `Flag`. The flag is only escalated to `'pending'` again if the `ContentItem` has been updated *after* the flag was marked irrelevant.

4. **Scoring Logic Execution**
   Scoring logic handles exact matching (`100`), partial matching (`70`), and body-only matching (`40`) via Python string matching. Everything is converted to lowercase to ensure case-insensitive evaluation.
