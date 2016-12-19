class ViewSearchMixin(object):
    search_fields = []
    object_model = None

    def filter_queryset(self, queryset):
        for attr, value in self.request.query_params.items():
            if hasattr(self.object_model, attr):
                try:
                    queryset = queryset.filter(**{attr: value})
                except Exception:
                    return []

        return queryset
