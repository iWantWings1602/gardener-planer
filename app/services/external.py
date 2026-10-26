import httpx


GEO_URL = "https://open-meteo.com"
WEATHER_URL = "https://open-meteo.com"

FALLBACK_COORDS = {
    "lviv": {"latitude": 49.8397, "longitude": 24.0297, "name": "Lviv"},
    "kyiv": {"latitude": 50.4501, "longitude": 30.5234, "name": "Kyiv"},
    "lutsk": {"latitude": 50.7472, "longitude": 25.3254, "name": "Lutsk"}
}


async def get_coordinates(client: httpx.AsyncClient, city: str) -> dict | None:
    city_lower = city.strip().lower()

    try:
        response = await client.get(GEO_URL, params={"name": city, "count": 1})
        if response.status_code == 200:
            data = response.json()
            results = data.get("results")
            if results and isinstance(results, list) and len(results) > 0:
                place = results[0]
                return {
                    "lat": place.get("latitude"),
                    "lon": place.get("longitude"),
                    "name": place.get("name", city)
                }
    except Exception:
        pass

    if city_lower in FALLBACK_COORDS:
        fallback = FALLBACK_COORDS[city_lower]
        return {
            "lat": fallback["latitude"],
            "lon": fallback["longitude"],
            "name": fallback["name"]
        }

    return None


async def get_weather_by_coords(client: httpx.AsyncClient, lat: float, lon: float) -> dict | None:
    try:
        response = await client.get(WEATHER_URL, params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,precipitation",
            "timezone": "auto"
        })
        if response.status_code == 200:
            current = response.json().get("current", {})
            return {
                "temperature": current.get("temperature_2m", 0.0),
                "precipitation_mm": current.get("precipitation", 0.0)
            }
    except Exception:
        pass
    return {"temperature": 15.0, "precipitation_mm": 0.0}  # Дефолтні безпечні дані на випадок збою мережі


