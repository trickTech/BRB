class ViewSearchMixin(object):
    search_fields = []
    object_model = None

    def filter_queryset(self, queryset):
        order = self.request.query_params.get('order', 'desc')
        orderby = self.request.query_params.get('orderby', 'created_at')

        for attr, value in self.request.query_params.items():
            if hasattr(self.object_model, attr):
                try:
                    queryset = queryset.filter(**{attr: value})
                except Exception:
                    return []

        if order and orderby:
            if hasattr(self.object_model, orderby):
                if order == 'desc':
                    orderby = '-' + orderby
                try:
                    queryset = queryset.order_by(orderby)
                except Exception:
                    return []

        return queryset
