from django.http import HttpResponseForbidden

def admin_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_admin():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrap

def stock_manager_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.has_role('stock-manager', 'admin'):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrap

def shop_keeper_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.has_role('shop-keeper', 'admin'):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrap
