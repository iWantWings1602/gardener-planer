import asyncio
import time
import httpx
from fastapi import APIRouter, HTTPException
from app.services.external import get_coordinates, get_weather_by_coords

router = APIRouter(prefix="/explore", tags=["explore"])


async def fetch_city_report(client: httpx.AsyncClient, city_name: str) -> dict:
    geo_data = await get_coordinates(client, city_name)
    if not geo_data:
        return {
            "city": city_name,
            "temperature_c": 12.0,
            "precipitation_mm": 0.0,
            "status": "No connection to weather service. Defaulting to safe status.",
            "action_required": True
        }

    weather_data = await get_weather_by_coords(client, geo_data["lat"], geo_data["lon"])

    precip = weather_data.get("precipitation_mm", 0.0)
    temp = weather_data.get("temperature", 0.0)

    if precip > 1.0:
        status = "Watering is skipped. Nature is doing the job today!"
        action_required = False
    else:
        status = "No significant rain detected. Check your plants schedule."
        action_required = True

    return {
        "city": geo_data["name"],
        "temperature_c": temp,
        "precipitation_mm": precip,
        "status": status,
        "action_required": action_required
    }


@router.get("/watering-status")
async def explore_watering():
    start_time = time.perf_counter()
    cities = ["Lviv", "Kyiv", "Lutsk"]

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            tasks = [fetch_city_report(client, city) for city in cities]
            report = await asyncio.gather(*tasks)
    except Exception:
        raise HTTPException(status_code=502, detail="External service error")

    return {
        "title": "Gardener Assistant Async Report",
        "total_cities_checked": len(report),
        "report": report,
        "took_seconds": round(time.perf_counter() - start_time, 2)
    }

