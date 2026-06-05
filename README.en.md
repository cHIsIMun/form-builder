# form-builder

🇺🇸 English | 🇧🇷 [Português](README.md)

> A Django REST backend for building multi-step dynamic forms, with typed answer collection.

## Overview

A Django REST API for **building dynamic forms** organized into steps and sections, and collecting typed answers. The data model follows a **Step → Section → Field** hierarchy, and submissions are linked to users.

## Data model

- **Step** → **Section** → **Field** (ordered via `unique_together`).
- Typed answers: `AnswerText`, `AnswerNumber`, `AnswerBoolean`, `AnswerDate`, `AnswerFile`.
- **Submission** associated with a user and a step.

## Features

- CRUD ViewSets for steps, sections, and fields.
- Form-structure retrieval (`/form-structure/`, `/step/<id>/`, `/section/<id>/`).
- Answer collection with type conversion.
- Custom email-based authentication (`AbstractBaseUser`), permissions, and groups.

## Stack

Python · Django · Django REST Framework · SQLite.

## Running

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt   # or per the project's manager
python manage.py migrate
python manage.py runserver        # http://localhost:8000
```

## Project status

Well-structured backend with solid models. For production it still needs: token/JWT authentication, CORS configuration, and tests.

## License

This project does not yet declare a license. Until one is added, all rights are reserved by the author.
