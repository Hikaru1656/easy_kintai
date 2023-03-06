from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

class AuthMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path == '/accounts/signup/' and not request.user.is_authenticated :
            pass
        elif request.path == '/accounts/password/reset/' and not request.user.is_authenticated :
            pass
        elif request.path == '/accounts/password/reset/done' and not request.user.is_authenticated :
            pass
        elif request.path == '/accounts/password/reset/' and not request.user.is_authenticated :
            pass
        elif request.path == '/accounts/confirm-email/' and not request.user.is_authenticated :
            pass
        # elif request.path != '/accounts/login/' and not request.user.is_authenticated :
        #     return HttpResponseRedirect('/accounts/login/')
        return response
