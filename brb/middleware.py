def cross_site(get_response):
    def middleware(request):
        response = get_response(request)
        refer = request.META.get('HTTP_REFERER')
        response["Access-Control-Allow-Origin"] = refer
        return response

    return middleware