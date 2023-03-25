from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

def guest_login_required(view_func=None, redirect_field_name = REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        # is_authenticatedかつrole_aのユーザのみ許可する
        lambda u: u.is_authenticated and hasattr(u, "guestuser"),
        login_url=login_url,
        redirect_field_name = redirect_field_name,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def host_login_required(view_func=None, redirect_field_name = REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        # is_authenticatedかつrole_aのユーザのみ許可する
        lambda u: u.is_authenticated and hasattr(u, "hostuser"),
        login_url=login_url,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

#以下、required_uidさえ渡せれば動かせるはずのuid認証。method_decoratorにおける引数の渡し方が分からず断念。
def guest_uid_login_required(required_uid, view_func=None, login_url=None):
    actual_decorator = user_passes_test(
        # is_authenticatedかつrole_aのユーザのみ許可する
        lambda u: u.is_authenticated and (u.guestuser.uid == required_uid),
        login_url=login_url,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def host_uid_login_required(required_uid, view_func=None, login_url=None):
    actual_decorator = user_passes_test(
        # is_authenticatedかつrole_aのユーザのみ許可する
        lambda u: u.is_authenticated and (u.hostuser.uid == required_uid),
        login_url=login_url,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator