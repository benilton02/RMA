class HttpErrors:
    """Http Errors"""

    @staticmethod
    def error_422():
        """HTTP 422"""

        return {'status_code': 422, 'body': {'error': 'Unprocessable Entity'}}

    @staticmethod
    def error_400():
        """HTTP 400"""

        return {'status_code': 400, 'body': {'error': 'Bad Request'}}

    @staticmethod
    def error_403():
        """HTTP 403"""

        return {'status_code': 403, 'body': {'error': 'Forbidden'}}

    @staticmethod
    def error_401():
        """HTTP 401"""

        return {'status_code': 401, 'body': {'error': 'Permission Denied'}}

    @staticmethod
    def error_409():
        """HTTP 409"""

        return {'status_code': 409, 'body': {'error': 'Conflict'}}

    @staticmethod
    def error_500():
        """HTTP 500"""

        return {'status_code': 500, 'body': {'error': 'Internal Server Error'}}

    @staticmethod
    def error_404():
        """HTTP 404"""

        return {'status_code': 404, 'body': {'error': 'Not Found'}}
