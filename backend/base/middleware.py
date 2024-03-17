from django.db import connection

class QueryCounterMiddleware:
    """Middleware to count the ammount of calls that a View does to a database.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.query_count = 0

    def __call__(self, request):
        start_count = len(connection.queries)
        response = self.get_response(request)
        self.query_count += len(connection.queries) - start_count
        print(f"Number of database calls for request '{request.path}': {self.query_count}")
        return response
