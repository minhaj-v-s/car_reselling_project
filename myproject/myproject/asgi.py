# asgi.py

from channels.auth import AuthMiddleWareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from myapp import routing
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddleWareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})