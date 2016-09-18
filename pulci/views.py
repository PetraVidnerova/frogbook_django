from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from .models import Citation

import locale
locale.setlocale(locale.LC_ALL, "cs_CZ.utf8")

# Create your views here.
def pulci(request):
    sort_type = request.GET.get("sort_type", "likes")
    if sort_type == "likes":
        citations = Citation.objects.order_by('-likes')
    elif sort_type == "date":
        citations = Citation.objects.order_by('-date')
    else:
        raise ValueError("unsupported sort")

    votable = [ str(x.id) not in request.session.get('voted',[]) for x in citations ]
    id_list = [ c.id for c in citations ]
    previous = [ id_list[-1]] + id_list[:-1]
    next = id_list[1:] + [id_list[0]]
    citation_list = zip(citations, votable, previous, next)
    context = {
        'citation_list' : citation_list,
        'sort_type' : sort_type
    }
    return render(request, "pulci/pulci.html", context)


def detail(request, id):
    """ Display one citation, links to previous and next citation."""
    citation = get_object_or_404(Citation, pk=id)
    votable = citation.id not in request.session.get('voted',[])
    previous = citation.id - 1
    next = citation.id + 1
    if next >= len(Citation.objects.order_by('-likes')):
        next = -1

    context = {
        'citation' : citation,
        'votable' : votable,
        'previous' : previous,
        'next' : next
    }

    return render(request, "pulci/detail.html", context)

def vote(request, id):
    print(id)
    print(request.session.get('voted', list()))
    if id in request.session.get('voted', list()):
        # already voted for this citation
        return HttpResponseBadRequest()

    # vote
    cit = get_object_or_404(Citation, pk=id)
    cit.likes += 1
    cit.save()

    if request.session.get('voted', False):
        print("apend")
        # append didn't work
        new_list = request.session['voted']
        new_list.append(id)
        request.session['voted'] = new_list
        print(request.session['voted'])
    else:
        request.session['voted'] = [ id ]
    return HttpResponse(str(cit.likes))

    #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def fill_datebase(request):
    """ Feeds the citations from file to database. Should be called
        only once. """
    import re
    from datetime import datetime
    import locale
    locale.setlocale(locale.LC_ALL, ('cs_CZ', 'utf-8'))

    def create_citation(date, who, text):

        cit = Citation()

        date = re.sub(' v .*', '', date).strip()
        datetime_object = datetime.strptime(date, "%d. %B %Y")

        cit.date = datetime_object
        cit.who = who
        cit.text = text
        cit.save()


    state = None
    EAT_WHO = 0
    EAT_TEXT = 1
    date, who, text = "", "", ""

    with open("fill_database/hlasky.txt", encoding="utf-8") as f:
        for line in f:
            if line.startswith("DATE"):
                if state == EAT_TEXT:
                    #start of new citation
                    create_citation(date, who, text)
                    date, who, text = "", "", ""
                date = line.strip("DATE")
                state = EAT_WHO
                continue

            if state == EAT_WHO:
                who = line.strip()
                state = EAT_TEXT
                continue

            if state == EAT_TEXT:
                text += line
                continue

    create_citation(date, who, text)
    return HttpResponse("OK")
