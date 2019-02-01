from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile."""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile."""
        """This function is called every time a request is made to our API the
        result of that function determine whether the user has the permission or
        doesn't have the permisson to perform the action. So this object
        permission class returns a simple true or false depending on what the
        result of the permission is."""
        """First thing that we want to do with this permission is we want to
        allow users to be able to view any profile in the system so we dont want
        to apply any permission if the user is trying to just simply view a
        profile. We do this by checking safe methods list that's provided by the
        Django rest framework. A safe method is a HTTP method that is classified
        as safe. That is a non-destructive method so it allows you to retrieve
        data but it doesn't allow you to change or modify or delete any object
        in the system. So a safe method is HTTP GET."""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id
