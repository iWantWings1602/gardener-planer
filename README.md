# Gardener Assistant API

A modular FastAPI backend application featuring SQLAlchemy ORM (SQLite) and asynchronous integration with external Open-Meteo APIs using `asyncio.gather`.

## Project Structure
The project is built using a strict modular approach as required by the assignment guidelines:
- `app/database.py` — Database connection configuration, `SessionLocal` factory, and the `get_db` dependency.
- `app/models.py` — SQLAlchemy ORM model for the `Plant` entity containing 5 distinct data types.
- `app/schemas.py` — Pydantic validation schemas (`PlantCreate`, `PlantUpdate`, `PlantOut`) with strict `Field` constraints.
- `app/routers/plants.py` — Full CRUD API router managing the plant entity lifecycle.
- `app/routers/explore.py` — High-performance asynchronous endpoint orchestrating concurrent external API requests.
- `app/services/external.py` — Independent business logic layer isolating all outbound HTTP interactions.

## Installation & Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the FastAPI development server:
   ```bash
   fastapi dev app/main.py
   ```

3. Open the interactive Swagger UI documentation in your web browser:
   ```text
   http://127.0.0
   ```

## API Endpoints
- `POST /plants` — Creates a new plant entry (returns `201 Created`).
- `GET /plants` — Retrieves all plants with dynamic filtering by city, `limit`, and `offset` pagination.
- `GET /plants/{plant_id}` — Fetches detailed data for a specific plant (returns `404 Not Found` if missing).
- `PATCH /plants/{plant_id}` — Updates only the provided attributes using partial validation (`exclude_unset=True`).
- `DELETE /plants/{plant_id}` — Permanently removes a plant entry from the database (returns `204 No Content`).
- `GET /explore/watering-status` — Asynchronous analytics endpoint polling multiple cities concurrently via `asyncio.gather` and displaying total request execution metrics using `took_seconds`.
