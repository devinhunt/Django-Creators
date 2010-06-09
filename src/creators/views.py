from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from vice3d.megaphone.models import Alert
from vice3d.megaphone.forms import NodeForm

def index(request):
    return render_to_response('megaphone/index.html', { })
    
@login_required
def dashboard(request):
    latest_alerts = Alert.objects.all().order_by('-created')
    node_form = NodeForm();
    return render_to_response('megaphone/dashboard.html', { 'alerts': latest_alerts,
                                                            'node_form': node_form })

@login_required    
def alert_add(request):
    try:
        new_alert = Alert(title = request.POST['alert_title'], message = request.POST['alert_message'])
    except (KeyError):
        return render_to_response('megaphone/dashboard.html', {
            'error_message': "You done fucked up, son."
        })
    else:
        new_alert.save()
        return HttpResponseRedirect(reverse('vice3d.megaphone.views.dashboard'))
        
def node_upload(request):
    if request.method == 'POST':
        form = NodeForm(request.POST, request.FILES)
        if form.is_valid():
            
    return HttpResponseRedirect(reverse('vice3d.megaphone.views.dashboard'))