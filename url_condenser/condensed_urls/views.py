from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SubmitUrlForm
from .models import CondensedUrl


def index(request):
    if request.method == 'POST':
        form = SubmitUrlForm(request.POST)

        if form.is_valid():
            CondensedUrl.objects.create(original_url=form.cleaned_data['url'])
            HttpResponseRedirect(reverse('index'))
    else:
        form = SubmitUrlForm()

    return render(request, 'condensed_urls/index.html', {'form': form})
