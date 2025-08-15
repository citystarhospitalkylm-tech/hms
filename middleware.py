# core/middleware.py
import logging

class ResponseInspectorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, Exception):
            logging.error(
                "⚠️ get_response returned an exception object: %r", response,
                exc_info=True
            )
        return response