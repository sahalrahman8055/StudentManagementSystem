from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call the default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # If an error response is generated, add additional details to it
        error_detail = {
            'error': str(exc),  # Include the exception message
            'traceback': exc.__traceback__,  # Include the traceback object
        }
        response.data['detail'] = error_detail

    return response
