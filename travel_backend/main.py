from fastapi import FastAPI
from travel_backend.api.routes import router
from travel_backend.db.db_setup import engine
from travel_backend.models.base import Base


import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


Base.metadata.create_all(bind=engine)

# Create the FastAPI app instance
app = FastAPI(title="Travel Itinerary API")

# Include the routes from the 'routes.py' file
app.include_router(router, prefix="/api")

@app.get("/", tags=["Root"])
def root():
    """
    Displays a formatted list of all available API routes with descriptions.
    """
    routes = []
    for route in app.routes:
        if route.path != "/docs" and route.path != "/redoc": 
            route_info = {
                "path": route.path,
                "methods": ", ".join(route.methods),  # Join methods with comma for cleaner display
                "description": get_route_description(route)  # Get descriptions for the routes
            }
            routes.append(route_info)

    # Generate the message to show each route and description in a new line
    available_routes = [
        f"Path: {route['path']}\nMethods: {route['methods']}\nDescription: {route['description']}"
        for route in routes
    ]

    return {
        "message": "Welcome to the Travel Itinerary API",
        "available_routes": available_routes  # Return the formatted list
    }

def get_route_description(route):
    """
    Returns a description for each route. You can manually edit this based on your route's purpose.
    """
    # addinf descriptions for each route 
    route_descriptions = {
        "/openapi.json": "Fetch OpenAPI JSON specification.",
        "/docs/oauth2-redirect": "OAuth2 redirect URL for documentation.",
        "/api/itineraries/": "Create a new itinerary or get all itineraries.",
        "/api/itineraries/{itinerary_id}": "Get details of a specific itinerary.",
        "/api/recommendations/{nights}": "Get itinerary recommendations based on the number of nights.",
        "/": "Root endpoint showing available routes."
    }
    return route_descriptions.get(route.path, "N/A")  # Default to "N/A" if no description is found
