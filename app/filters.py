def ord_filter(value):
    return ord(value)

def register_filters(app):
    app.jinja_env.filters["ord"] = ord_filter