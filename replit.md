# Alat Bantu Kerja Guru BK

## Overview
This is a Flask-based web application designed to help Indonesian guidance counselors (Guru BK) generate service documents based on learning achievement phases (Capaian Pembelajaran). The application automates the creation of service objectives and achievement criteria documentation.

## Purpose
- Generate counseling service documents based on educational phase selection
- Automate the analysis of learning achievements (CP) into service objectives (TL) and achievement criteria (KKTL)
- Support all educational phases from Foundation (PAUD) through Phase F (High School)

## Current State
The application is fully functional and running on Replit with:
- Python 3.11
- Flask web framework
- Template-based rendering system
- Static CSS styling
- Form-based user input
- Automated document generation

## Recent Changes
- **2025-10-02**: Initial Replit environment setup
  - Configured Flask to bind to 0.0.0.0:5000 for Replit hosting
  - Set up Flask Server workflow
  - Created Python .gitignore
  - Configured deployment settings

## Project Architecture

### Technology Stack
- **Backend**: Flask (Python 3.11)
- **Frontend**: HTML, CSS (Jinja2 templates)
- **Dependency Management**: UV package manager

### File Structure
```
.
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── index.html        # Form input page
│   └── hasil.html        # Results display page
└── static/               # Static assets
    └── style.css         # Application styling
```

### Key Features
1. **Data Model**: Embedded CP (Capaian Pembelajaran) data for all educational phases
2. **Analysis Engine**: Automatic conversion of CP to TL (Tujuan Layanan) and KKTL (Kriteria Ketercapaian)
3. **User Input**: Form-based data collection for school and teacher information
4. **Document Generation**: Automated table-based output with phase-specific analysis

### Routes
- `/` - Main form page (GET)
- `/generate-dokumen` - Document generation (POST)

### Educational Phases Supported
- FONDASI (Foundation - PAUD/Early Childhood)
- A (Grades 1-2 SD)
- B (Grades 3-4 SD)
- C (Grades 5-6 SD)
- D (Grades 7-9 SMP)
- E (Grade 10 SMA/SMK)
- F (Grades 11-12 SMA/SMK)

## Development
- Server runs on port 5000
- Development server is configured for production-safe operation
- Templates use Jinja2 for dynamic content rendering

## Deployment
Configured for Replit deployment with proper port binding and host configuration.
