# Get authentication status
isAuthenticated = lambda user: user.is_authenticated()

# Get researcher status
isResearcher = lambda session: session.get('researcher')
