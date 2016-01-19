import base64

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect, HttpResponseRedirect

from .forms import SubmitUrlForm
from .models import CondensedUrl


def parse_condensed_url(request, condensed_url_id):
    """
    Return a URL for a given condensed URL.

    :param request: a Django HttpRequest
    :type request: `django.http.request.HttpRequest`
    :param condensed_url_id: the base64 encoded database id of the CondensedUrl
    :type condensed_url_id: str

    :returns: either HTTP 302 or 404
    :rtype: `django.http.request.HttpResponsePermanentRedirect` or `django.http.request.HttpResponseNotFound`
    """
    # base64 has minimum padding requirements
    if len(condensed_url_id) < 4:
        return HttpResponseNotFound()

    # we require ASCII for base64 to work nicely which is fine
    # considering all codes generated are ASCII
    # TODO unicode madness may break this - thanks Python2!
    decoded_url_id = base64.urlsafe_b64decode(condensed_url_id.encode('ascii'))
    condensed_url = get_object_or_404(CondensedUrl, pk=int(decoded_url_id))
    return HttpResponsePermanentRedirect(condensed_url.original_url)


def index(request):
    """
    Index page for the site. Also contains the main form for entering a
    URL to be condensed.

    :param request: a Django HttpRequest
    :type request: `django.http.request.HttpRequest`

    :returns: a Django HttpResponse
    :rtype: `django.http.request.HttpResponse`
    """
    if request.method == 'POST':
        form = SubmitUrlForm(request.POST)

        if form.is_valid():
            CondensedUrl.objects.create(original_url=form.cleaned_data['url'])
            HttpResponseRedirect(reverse('index'))
    else:
        form = SubmitUrlForm()

    return render(request, 'condensed_urls/index.html', {'form': form})
