from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import Http404

from forms import ArtForm
from models import Art

@login_required
def manage_art(request, template_name, art_id=None):
    try:
        request.user.get_profile()
    except:
        raise Http404
    painting = get_object_or_404(Art, id=art_id) if art_id else None
    if request.method == 'POST':
        form = ArtForm(data=request.POST, files=request.FILES, instance=painting,
                       user=request.user)
        if form.is_valid():
            form.save()
            return redirect(form.instance)
    else:
        form = ArtForm(instance=painting, user=request.user)
    context = RequestContext(request)
    return render_to_response(template_name, {'form': form}, 
                              context_instance=context)
