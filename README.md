# Food Ordering Project

A sample restaurant menu and pickup-order app for learning full-stack basics.

## Stack
Python 3, Django, SQLite, HTML, CSS, vanilla JavaScript.

## Changes in this customized version
- Menu categories and vegetarian filter
- Cart quantity controls and order totals
- Pickup order confirmation stored in the database
- Responsive menu layout

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Open http://127.0.0.1:8000. Sample menu data is loaded automatically.

## Source and attribution
Feature inspiration: [Soufiane-Majdar/Food_Project](https://github.com/Soufiane-Majdar/Food_Project), MIT License. This repository contains a simplified, reworked implementation for practice; original copyright notice is retained in LICENSE.

Demo only: use fictional data. No real orders or payments are processed.
