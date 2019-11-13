from rest_framework import generics
from rest_framework import permissions

from knox.auth import TokenAuthentication

from .models import BookmarkedTender, BookmarkedContract
from .serializers import BookmarkedContractListSerializer, BookmarkedContractCreateSerializer
from .serializers import BookmarkedTenderListSerializer, BookmarkedTenderCreateSerializer


# Create your views here.
class BookmarkedContractList(generics.ListAPIView):

    serializer_class = BookmarkedContractListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return BookmarkedContract.objects.filter(user=self.request.user).order_by('-id')


class BookmarkedTenderList(generics.ListAPIView):

    serializer_class = BookmarkedTenderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return BookmarkedTender.objects.filter(user=self.request.user).order_by('-id')


class BookmarkedContractCreate(generics.CreateAPIView):

    serializer_class = BookmarkedContractCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookmarkedTenderCreate(generics.CreateAPIView):

    serializer_class = BookmarkedTenderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SingleBookmarkedContract(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = BookmarkedContractCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return BookmarkedContract.objects.filter(user=self.request.user).order_by('-id')


class SingleBookmarkedTender(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = BookmarkedTenderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return BookmarkedTender.objects.filter(user=self.request.user).order_by('-id')
