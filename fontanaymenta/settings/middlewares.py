import logging
from django.contrib.auth import logout
from django.http import HttpResponseServerError

class WebFactionFixes(object):
    """Sets 'REMOTE_ADDR' based on 'HTTP_X_FORWARDED_FOR', if the latter is
    set.

    Based on http://djangosnippets.org/snippets/1706/
    """
    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
            request.META['REMOTE_ADDR'] = ip


class HandleExceptionMiddleware:
    """ http://stackoverflow.com/questions/3823280/ioerror-request-data-read-error/7089413 """
    def process_exception(self, request, exception):
        if isinstance(exception, IOError) and 'request data read error' in unicode(exception):
            logging.info('%s %s: %s: Request was canceled by the client.' % (
                    request.build_absolute_uri(), request.user, exception))
            return HttpResponseServerError()


class Subdomains:
    def process_request(self, request):
        request.META['HTTP_X_SUBDOMAIN'] = request.get_host()

    def process_response(self, request, response):
        response['X-Subdomain'] = request.META['HTTP_X_SUBDOMAIN']
        return response


class ActiveUserMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return
        if not request.user.is_active:
           logout(request)