from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Contact


# Create your views here.
def index(request):
    contacts = Contact.objects.order_by('-id').filter(
        show = True
    )
    paginator = Paginator(contacts, 5)

    page = request.GET.get('p')
    contacts = paginator.get_page(page)
    return render(request, 'contacts/index.html', {
        'contacts': contacts
    })

def see_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if not contact.show:
        raise Http404()
    return render(request, 'contacts/see_contact.html', {
        'contact': contact
    })

