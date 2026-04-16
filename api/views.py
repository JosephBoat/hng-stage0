import requests
from datetime import datetime, timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "HNG Stage 0 API is live",
        "endpoint": "/api/classify?name=john"
    })

@api_view(["GET"])
def classify_name(request):
    name = request.GET.get("name")

    # Missing or empty
    if name is None or name.strip() == "":
        return Response(
            {"status": "error", "message": "Missing or empty name parameter"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Must be string
    if not isinstance(name, str):
        return Response(
            {"status": "error", "message": "name is not a string"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    try:
        res = requests.get("https://api.genderize.io", params={"name": name}, timeout=5)

        if res.status_code != 200:
            return Response(
                {"status": "error", "message": "Upstream service failure"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        data = res.json()

        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")

        if gender is None or count == 0:
            return Response(
                {
                    "status": "error",
                    "message": "No prediction available for the provided name",
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        probability = float(probability)
        sample_size = int(count)

        is_confident = probability >= 0.7 and sample_size >= 100

        processed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        return Response(
            {
                "status": "success",
                "data": {
                    "name": name.lower(),
                    "gender": gender,
                    "probability": probability,
                    "sample_size": sample_size,
                    "is_confident": is_confident,
                    "processed_at": processed_at,
                },
            }
        )

    except requests.exceptions.RequestException:
        return Response(
            {"status": "error", "message": "Failed to reach external service"},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    except Exception:
        return Response(
            {"status": "error", "message": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
