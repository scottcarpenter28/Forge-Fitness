import json
from dataclasses import dataclass
from typing import Dict, Any

from rest_framework.response import Response


@dataclass
class JsonResponse:
    error: bool = False
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"error": self.error, "message": self.message}

    def to_response(self) -> Response:
        return Response(self.to_dict())


@dataclass
class JsonErrorResponse(JsonResponse):
    error = True
