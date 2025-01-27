from typing import Optional

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from application.models.exercise_routine import ExerciseRoutine
from application.utils.json_response import JsonResponse, JsonErrorResponse


class RoutineAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, routine_id: Optional[str] = None) -> Response:
        if not routine_id:
            return JsonErrorResponse(message="Missing routine id.").to_response()

        found_routine = ExerciseRoutine.objects.filter(uuid=routine_id).first()
        if not found_routine:
            return JsonErrorResponse(message="Missing routine id.").to_response()

        if not found_routine.is_public:
            if not found_routine.creator == request.user:
                return JsonErrorResponse(
                    message="You are not allowed to see this routine."
                ).to_response()

        exercises = [
            exercise.to_dict() for exercise in found_routine.find_routine_exercises()
        ]
        response = JsonResponse(message="ok").to_dict()
        response["exercises"] = exercises
        return Response(response)
