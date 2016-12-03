def cross_site(get_response):
    def middleware(request):
        response = get_response(request)
        refer = request.META.get('HTTP_REFERER')
        response["Access-Control-Allow-Origin"] = refer
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Credentials"] = True
        response["Access-Control-Max-Age"] = '86400'
        response["Access-Control-Allow-Headers"] = "X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept"
        return response

    return middleware
