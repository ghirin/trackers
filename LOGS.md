# Audit Logs (ActionLog)

This project includes an `ActionLog` model which records create/update/delete operations performed on models.

Fields captured:
- user (nullable) — which user performed the action (if available)
- content_type / object_id / object_repr — the target object
- action — `create`, `update`, or `delete`
- changes — a JSON object describing changed fields (old/new values) or full snapshot on create/delete
- timestamp — time of the event
- request_path and ip_address when available

Admin features:
- A new menu entry `Логи действий` is available under the `Tracker` app in Django admin.
- You can filter and search logs and export selected items as CSV or JSON via admin actions.

Export formats suitable for automated post-processing:
- CSV: good for CSV-based ETL processes and spreadsheets. The `changes` column contains a JSON string.
- JSON: machine-friendly JSON array where `changes` is a JSON object.

Notes for integrators:
- The logging middleware stores the current `request.user` in thread-local storage so signal handlers can attach the user to the log entry. This works for normal HTTP requests.
- Operations performed outside of requests (e.g. manage.py commands) will record `user = null`.
- If you need additional export formats (XLSX, NDJSON, streaming export), I can add admin actions or management commands to generate those.
