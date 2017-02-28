# Set researcher flag in session
def setResearcher(request):
    request.session['researcher'] = True if len(request.user.groups.filter(name='researcher')) == 1 \
                                         else False
