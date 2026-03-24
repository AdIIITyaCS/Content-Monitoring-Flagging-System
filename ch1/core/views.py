from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Keyword,ContentItem,Flag
from core.serializers import KeywordSerializer,FlagSerializer
from django.shortcuts import render

import json 
import os
from django.conf import settings
from core.services import ScannerService

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
class FlagViewSet(viewsets.ModelViewSet):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer
    http_method_names = ['get', 'patch', 'head']


@api_view(['POST'])
def run_scan(request):
    try:
        scanner = ScannerService()
        flags_created = scanner.run()
        
        return Response(
            {"message": "Scan completed successfully", "new_flags_created": flags_created},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)