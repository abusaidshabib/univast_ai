from rest_framework.exceptions import APIException
from rest_framework import status

class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A server error occurred.'

    def __init__(self, detail=None, field=None):
        if detail is not None:
            self.detail = {"error": detail}
            if field is not None:
                self.detail["field"] = field
        else:
            self.detail = {"error": self.default_detail}
