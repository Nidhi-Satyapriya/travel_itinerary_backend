# 🧳 Travel Itinerary Backend

A backend system using **FastAPI**, **SQLAlchemy**, and **Pydantic v2** for managing and recommending travel itineraries with day-wise activities, hotels, and transfers.

---

## 🚀 Features

- Create and fetch itineraries with full structure
- Day-wise planning with hotels, transfers, and activities
- Recommendation engine for itineraries based on number of nights
-  Seeded data for Phuket and Krabi (Thailand)

---

## 🧱 Database Architecture

### 📊 Schema Overview

| Table       | Description                                              |
|-------------|----------------------------------------------------------|
| Itinerary   | Represents a complete trip (e.g., "Phuket Escape")       |
| Day         | Each day in an itinerary, with hotel, transfer, activities |
| Activity    | Activities/excursions for each day                       |
| Hotel       | Hotel names (inline, no separate table)                 |
| Transfer    | Transfer info (e.g., "Ferry from Phuket to Krabi")       |

### 🔗 Relationships

- One `Itinerary` ➡️ has many `Days`
- One `Day` ➡️ has many `Activities`
- `Day.hotel` and `Day.transfer` are inline fields
- Activities are linked to specific days (foreign key: `day_id`)
- Cascading delete: deleting an `Itinerary` deletes related `Days` and `Activities`

### ⚙️ Constraints & Indexes

- Primary keys on all models (`id`)
- Foreign keys:
  - `Day.itinerary_id` → `Itinerary.id`
  - `Activity.day_id` → `Day.id`
- Unique constraint on `Day.day_number` per `Itinerary`
- Indexes on `nights` for fast recommendation lookup

---

## 📬 API Endpoints

### 🌐 Root

| Method | Path                  | Description                                      |
|--------|-----------------------|--------------------------------------------------|
| GET    | `/`                   | Welcome message and route listing                |

### 📦 Itinerary

| Method | Path                              | Description                                  |
|--------|-----------------------------------|----------------------------------------------|
| POST   | `/api/itineraries/`               | Create a new itinerary                        |
| GET    | `/api/itineraries/`               | Get all existing itineraries                  |
| GET    | `/api/itineraries/{itinerary_id}` | Get a specific itinerary by ID                |

### 🔍 Recommendations

| Method | Path                            | Description                                  |
|--------|----------------------------------|----------------------------------------------|
| GET    | `/api/recommendations/{nights}` | Get itinerary recommendations by trip length |

---

## 📦 Setup Instructions

```bash
# Clone repository
git clone https://github.com/Nidhi-Satyapriya/travel_itinerary_backend.git
cd travel_backend

# Create and activate virtual environment
python -m venv vienv
# Windows
vienv\Scripts\activate
# macOS/Linux
source vienv/bin/activate

# Set up environment variables
# Create a `.env` file in the root of the project directory with the following content:

# .env example:
# DATABASE_URL=sqlite:///./travel.db   # Local SQLite database
# If you want to use a PostgreSQL database, use this format:
# DATABASE_URL=postgresql://user:password@localhost:5432/travel_db
# ENV=development   # Optional: Set FastAPI environment (e.g., development, production)

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn travel_backend.main:app --reload --log-level debug
