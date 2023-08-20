from rest_framework.views import APIView
from rest_framework.response import Response
from .models import City, AreaOrCenter
from .serializers import CitySerializer, AreaOrCenterSerializer
from rest_framework import status

class CityListView(APIView):
    def get(self, request):
        city = City.objects.all()
        serializer = CitySerializer(city, many=True)
        return Response(serializer.data)


class AreaOrCenterListView(APIView):
    def get(self, request):
        city_id = request.query_params.get("city_id")
        if city_id:
            areas = AreaOrCenter.objects.filter(location_id=city_id)
            serializer = AreaOrCenter(areas, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Please provide a valid location ID."}, status=status.HTTP_400_BAD_REQUEST)