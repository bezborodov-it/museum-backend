from fastapi import APIRouter, Response, status

from api import schemas
from api.configuration.config import settings

site_router = APIRouter(prefix="/health", tags=["health"])

@site_router.get(
    "",
    status_code=200,
    response_model=schemas.HealthStatus,
    responses={
        503: {"description": "Service Unavailable", "model": schemas.HealthStatus},
    },
)
async def health(response: Response) -> schemas.HealthStatus:
    if not settings.SERVICE_ENABLED:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return schemas.HealthStatus(
            status=schemas.HealthStatusEnum.MAINTENANCE,
            version=settings.APP_VERSION,
        )
    return schemas.HealthStatus(
        status=schemas.HealthStatusEnum.OK,
        version=settings.APP_VERSION,
    )