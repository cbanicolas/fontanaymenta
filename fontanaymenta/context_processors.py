from django.contrib.sites.models import Site

#A context processor to add the "current site" to the current Context
def current_site(request):
    try:
        current_site = Site.objects.get_current()
        return {'current_site': current_site}
    except Site.DoesNotExist:
        # always return a dict, no matter what!
        return {'current_site':''} # an empty string

def current_path(request):
    return {'current_path': request.path.replace('/','')}