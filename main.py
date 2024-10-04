from fastapi import FastAPI, Request
import logging
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import api_router
from src.core.config import settings
from src.core.database import engine, Base

from src.schemas.response import APIResponse

import time

# Logging Configuration
logging.basicConfig(
    filename="server.log",  # Log file
    level=logging.INFO,  # Log Level
    format="%(asctime)s - %(levelname)s - %(message)s",
)

if settings.APP_ENV == "development":
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url="/docs",
    )
else:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

logger = logging.getLogger("fastapi_logger")


# Middleware to log each request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Log information about the incoming request
    logger.info(
        f"Request {request.method} on {request.url} from {request.client.host}"
    )

    # Call the next step (i.e. execute the route)
    response = await call_next(request)

    # Query execution time
    duration = time.time() - start_time
    logger.info(
        f"Response {response.status_code} for {request.url} in {duration:.4f} seconds"
    )

    return response


@app.get("/", response_model=APIResponse)
def read_root():
    return APIResponse.success(message="Welcome to the API")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
