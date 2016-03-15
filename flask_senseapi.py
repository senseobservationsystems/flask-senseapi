from flask import current_app, request

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

import senseapi
import json

class SenseAPIException(Exception):
    pass

class SenseAPI(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("SENSEAPI_SERVER", "live")
        app.config.setdefault("SENSEAPI_VERBOSE", False)
        app.config.setdefault("SENSEAPI_HTTPS", True)

        self.app = app

    def _get_sense_api(self):
        api = senseapi.SenseAPI()
        api.setServer(self.app.config['SENSEAPI_SERVER'])
        api.setVerbosity(self.app.config['SENSEAPI_VERBOSE'])
        api.setUseHTTPS(self.app.config['SENSEAPI_HTTPS'])
        
        session_id = request.headers.get('SESSION-ID', None)
        if session_id is not None:
            api.SetSessionId(session_id)

        return api
        
    @property
    def api(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'senseapi'):
                ctx.senseapi = self._get_sense_api()
            return ctx.senseapi

    def GetCurrentUser(self):
        if not self.api.UsersGetCurrent():
            current_app.logger.info("Can't Get Current User: {} - {}".format(self.api.getResponseStatus(), self.api.getResponse()))
            print "Can't Get Current User: {} - {}".format(self.api.getResponseStatus(), self.api.getResponse())
            raise SenseAPIException()
            
        response = json.loads(self.api.getResponse())

        return response["user"]

    def GetUser(self, user_id):
        if not self.api.UsersGet(user_id):
            current_app.logger.info("Can't Get User {}: {} - {}".format(user_id, self.api.getResponseStatus(), self.api.getResponse()))
            print "Can't Get User {}: {} - {}".format(user_id, self.api.getResponseStatus(), self.api.getResponse())
            raise SenseAPIException()

        response = json.loads(self.api.getResponse())

        return response["user"]

    def GetDomains(self, is_manager=False):
        parameters = self.api.DomainsGet_Parameters()
        if is_manager:
            parameters["member_type"] = "manager"

        domains = []
        done = False

        while not done:
            if not self.api.DomainsGet(parameters=parameters):
                current_app.logger.info("Can't Get Domains: {} - {}".format(self.api.getResponseStatus(), self.api.getResponse()))
                print "Can't Get Domains: {} - {}".format(self.api.getResponseStatus(), self.api.getResponse())
                raise SenseAPIException()

            response = json.loads(self.api.getResponse())
            if len(response["domains"]) < parameters["per_page"]:
                done = True
            else:
                parameters["page"] += 1

            domains += response["domains"]
                
        return domains

    def GetDomain(self, domain_id):
        if not self.api.DomainsGet(domain_id=domain_id):
            current_app.logger.info("Can't Get Domain {}: {} - {}".format(domain_id, self.api.getResponseStatus(), self.api.getResponse()))
            print "Can't Get Domain {}: {} - {}".format(domain_id, self.api.getResponseStatus(), self.api.getResponse())
            raise SenseAPIException()

        response = json.loads(self.api.getResponse())

        return response["domains"]

    def GetDomainUsers(self, domain_id):
        parameters = self.api.DomainUsersGet_Parameters()

        users = []
        done = False
        while not done:
            if not self.api.DomainUsersGet(domain_id=domain_id, parameters=parameters):
                current_app.logger.info("Can't Get Domain Users: {} - {}".format(self.api.getResponseStatus(), self.api.getResponse()))
                print "Can't Get Domain User {}: {} - {}".format(domain_id, self.api.getResponseStatus(), self.api.getResponse())
                raise SenseAPIException()

            response = json.loads(self.api.getResponse())
            if len(response["users"]) < parameters["per_page"]:
                done = True
            else:
                parameters["page"] += 1

            users += response["users"]

        return users
