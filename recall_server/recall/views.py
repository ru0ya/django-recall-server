"""
Custom views for the `recall` Django app.
"""

from recall_server.recall.models import Recall
from recall_server.recall.serializers import RecallSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class RecallCreateView(APIView):
    """
    Custom, class-based API dispatcher for the `recall.Recall` model.
    """
  
    permission_classes=[IsAuthenticated]

    def get(self, request):
        recalls = Recall.objects.all()
        serializer = RecallSerializer(recalls, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(recaller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
        


class RecallDetailView(APIView):
    """
    Custom, class-based API dispatcher for the `recall.Recall` model.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Recall.objects.get(pk=pk)
        except Recall.DoesNotExist:
            return None

    def get(self, request, pk):
        recall = self.get_object(pk)
        if recall is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RecallSerializer(recall)
        return Response(serializer.data)

    def put(self, request, pk):
        recall = self.get_object(pk)
        if recall is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RecallSerializer(recall, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recall = self.get_object(pk)
        if recall is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        recall.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def add_support(self, request,  pk=None):
        """Add current user as a supporter"""
        recall =self.get_object()
        
        if not recall.can_add_supporter(request.user):
            return Response(
                {
                    "error": "You cannot support this recall (wrong constituency/county/ward)"
                },
                status = status.HTTP_403_FORBIDDEN
            )
            
        recall.recall_supporters.add(request.user)
        recall.update_signature_count()
        
        return Response(
            {
                "message": "Support added successfully",
                "current_count": recall.current_signature_count,
            },
            status = status.HTTP_200_OK
        )
            
    
    def remove_support(self, request, pk=None):
        """Remove current user as a supporter"""
        recall = self.get_object()
        recall.recall_supporters.remove(request.user)
        recall.update_signature_count()
        
        return Response(
            {
                "message": "Support removed successfully",
                "current_count": recall.current_signature_count,
            },
            status = status.HTTP_200_OK
        )
