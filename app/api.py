try:
    from app.configurations import API_PREFIX

    DOCS_URL = f'{API_PREFIX}/docs'
    OPENAPI_URL = f'{API_PREFIX}/openapi.json'
except ImportError as error:
    raise

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.apps.translator.controllers import translator_router
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram


app = FastAPI(
    docs_url=DOCS_URL,
    openapi_url=OPENAPI_URL
)

# Define custom metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total number of HTTP requests", [
        "method", "endpoint"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Histogram of request latency in seconds", [
        "method", "endpoint"]
)
REQUEST_ERRORS = Counter(
    "http_request_errors_total", "Total number of HTTP request errors", [
        "method", "endpoint"]
)


# @TODO: not for production
# @NOTE: original should be domain or IP of Client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path

    # Ignore requests to /metrics endpoint
    if endpoint == "/metrics":
        return await call_next(request)

    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

    with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
        response = await call_next(request)

    if response.status_code >= 400:
        REQUEST_ERRORS.labels(method=method, endpoint=endpoint).inc()

    return response


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")

app.include_router(
    translator_router, prefix=f"{API_PREFIX}/translator", tags=["Translator"]
)
