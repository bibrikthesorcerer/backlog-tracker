from rest_framework.views import APIView


class MethodPermissionsMixin:
    """
    MethodPermissionsMixin lets you apply permission classes per-method (HTTP)
    """
    method_permissions: dict = {}

    def get_permissions(self):
        method = self.request.method.upper()
        perms = self.method_permissions.get(method, self.permission_classes)
        return [p() for p in perms]


class BaseView(MethodPermissionsMixin, APIView):
    pass