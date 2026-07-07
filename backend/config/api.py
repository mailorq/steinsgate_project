from ninja import NinjaAPI

from accounts.api import auth_router, profile_router
from catalog.api import router as catalog_router
from comments.api import router as comments_router
from watch.api import router as watch_router

api = NinjaAPI(
    title="SteinsGate API",
    version="1.0.0",
    docs_url="/docs",
)

api.add_router("/auth", auth_router)
api.add_router("/profile", profile_router)
api.add_router("", catalog_router)
api.add_router("", comments_router)
api.add_router("", watch_router)
