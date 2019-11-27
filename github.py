from requests import get, post

class github(object):
    ISSUE_API = 'https://api.github.com/repos/{uri}/issues?state={state}'

    def __init__(self, uri):
        self.uri = uri
    def issues(self, state):
        api = github.ISSUE_API.format(uri=self.uri, state=state)
        return self.req(api)

    def req(self, api):
        return get(api).json()