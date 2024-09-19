# Flashcards App

## Description
A simple flashcard application to help users learn phrasal verbs.

## Features
- Add new flashcards with verb, meaning, examples, and images.
- Review flashcards using a spaced repetition system (SRS).

## Installation

### Prerequisites
- Python 3.x
- pip (Python package manager)
- Virtualenv (optional but recommended)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/stantejada/flashcards_app.git
   cd flashcards_app

### Optional
1. Create a virtual environment
   ```bash
   python -m venv venv

3. Activate the virtual environment
* For Windows
  ```bash
  .\venv\Scripts\activate
        
* For macOS/Linux
  ```bash
  source venv/bin/activate

4. Install dependencies
   ```bash
    pip install -r requirements.txt
6. Setup Database
* Initialize the database:
   ```bash
    flask db init
* Create a migration script:
   ```bash
    flask db migrate -m "Initial migration."
* Apply the migration to the database:
  ```bash
    flask db upgrade
### Running the Application
    flask run

Visit http://localhost:5000 in your web browser to access the application.
