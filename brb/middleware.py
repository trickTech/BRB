def cors_middleware(get_response):
    def middleware(request):
        request_origin = request.get_host()
        response = get_response(request)
        response['Access-Control-Allow-Origin'] = request_origin

        return response

    return middleware
