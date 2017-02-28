# Get authentication status
isAuthenticated = lambda user: user.is_authenticated()

# Get researcher status
isResearcher = lambda request: isAuthenticated(request.user) and request.session.get('researcher')

isSubject = lambda request: isAuthenticated(request.user) and not request.session.get('researcher')
