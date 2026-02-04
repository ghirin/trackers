# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2026-02-04
### Added
- Location model and migrations to normalize/manage locations. 🔧
- Reports filtering (date range, location, model, IMEI, serial, SIM). 📊
- XLSX export of installations (via openpyxl) with applied filters. 📁
- AJAX modal forms for Car/Tracker/Installation (fetch + Bootstrap modal). ✨
- Dashboard: added columns (IMEI, board number, model, protocol, SIMs, inventory numbers, comments). 🧾
- Tests: basic tests for reports and export. 🧪
- Docs: `DEV_SETUP.md`, `README_GIT_PUSH.md`, updated `requirements.txt`. 📝

### Fixed
- Date input format in installation form (ISO date) to properly support input[type=date]. 🛠️
- Migration conflicts and import dependency issues (django-import-export). 🔁
- Export crash when Location object was passed to openpyxl cells. ✅
- Templating bug (invalid ternary) in `dashboard.html`. ✅

---

*Prepared and pushed by automated workflow.*
