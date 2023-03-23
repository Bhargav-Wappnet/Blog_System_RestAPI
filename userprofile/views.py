from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from django.utils import timezone
from django.contrib.auth import logout


class UpdateUsernameAPIView(APIView):
    """
    API endpoint that allows a user to update their username.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Update the current user's username.

        Args:
            request (Request): The incoming request object.

        Returns:
            Response: A response object containing a success/failure status,
                    a message, and data.

        Raises:
            None
        """
        new_username = request.data.get("new_username")

        # Check if a new username was provided.
        if not new_username:
            return Response(
                {
                    "status": False,
                    "message": "Please provide a new username.",
                    "data": None,
                },
                status=HTTP_400_BAD_REQUEST,
            )

        # Check if the new username is already taken.
        if User.objects.filter(username=new_username).exists():
            return Response(
                {
                    "status": False,
                    "message": "This username is already taken.",
                    "data": None,
                },
                status=HTTP_400_BAD_REQUEST,
            )

        # Update the user's username and save the changes.
        user = request.user
        user.username = new_username
        user.save()

        # Return a success response with the updated username.
        return Response(
            {
                "status": True,
                "message": "Username updated successfully.",
                "data": {
                    "new_username": new_username,
                },
            },
            status=HTTP_200_OK,
        )


class UserSoftDeleteAPIView(APIView):
    """
    API endpoint that allows a user to soft delete their account.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Soft delete the current user's account.

        If the user has already been soft-deleted, return an error response.
        Otherwise, soft delete the account by setting the `deleted_at` field
        to the current date and time.

        Returns:
            A response with a status code of 200 if the account was successfully
            soft-deleted, or a status code of 400 if the user has already been
            soft-deleted.
        """
        user = request.user
        if user.deleted_at:
            return Response(
                {
                    "status": False,
                    "message": "User Account has already been soft-deleted.",
                    "data": None,
                },
                status=HTTP_400_BAD_REQUEST,
            )
        user.deleted_at = timezone.now()
        user.save()

        return Response(
            {
                "status": True,
                "message": "Account soft deleted successfully.",
                "data": None,
            },
            status=HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    """
    API endpoint that allows a user to logout and delete their token.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Log out the current user and delete their token.

        Deletes the user's authentication token and logs them out of the current
        session.

        Returns:
            A response with a status code of 200 if the user was successfully logged
            out, or a status code of 500 if an error occurred.
        """
        user = request.user
        if user.auth_token:
            user.auth_token.delete()
        logout(request)
        return Response(
            {
                "status": True,
                "message": "User logged out successfully.",
                "data": None,
            },
            status=HTTP_200_OK,
        )
