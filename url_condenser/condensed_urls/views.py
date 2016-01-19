import base64

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseNotFound, HttpResponsePermanentRedirect, HttpResponseRedirect

from .forms import SubmitUrlForm
from .models import CondensedUrl


def view_condensed_url(request, condensed_url_code):
    """
    Return a page showing the generated condensed url

    :param request: a Django HttpRequest
    :type request: `django.http.request.HttpRequest`
    :param condensed_url_code: the base64 encoded database id of the CondensedUrl
    :type condensed_url_code: str

    :returns: a Django HttpResponse
    :rtype: `django.http.request.HttpResponse`
    """
    context = {'condensed_url': condensed_url_code}
    return render(request, 'condensed_urls/view_condensed_url.html', context)


def parse_condensed_url(request, condensed_url_code):
    """
    Return a URL for a given condensed URL.

    :param request: a Django HttpRequest
    :type request: `django.http.request.HttpRequest`
    :param condensed_url_code: the base64 encoded database id of the CondensedUrl
    :type condensed_url_code: str

    :returns: either HTTP 302 or 404
    :rtype: `django.http.request.HttpResponsePermanentRedirect` or `django.http.request.HttpResponseNotFound`
    """
    # base64 has minimum padding requirements
    if len(condensed_url_code) < 4:
        return HttpResponseNotFound()

    # we require ASCII for base64 to work nicely which is fine
    # considering all codes generated are ASCII
    # TODO unicode madness may break this - thanks Python2!
    decoded_url_id = base64.urlsafe_b64decode(condensed_url_code.encode('ascii'))
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
            condensed_url = CondensedUrl.objects.create(original_url=form.cleaned_data['url'])
            return HttpResponseRedirect(reverse('view_condensed_url', args=[condensed_url.condensed_url()]))
    else:
        form = SubmitUrlForm()

    return render(request, 'condensed_urls/index.html', {'form': form})
