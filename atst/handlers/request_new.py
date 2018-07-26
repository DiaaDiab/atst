import tornado
from collections import defaultdict

from atst.handler import BaseHandler
from atst.forms.request import RequestForm
from atst.forms.org import OrgForm
from atst.forms.poc import POCForm
from atst.forms.review import ReviewForm


class RequestNew(BaseHandler):
    def initialize(self, page, requests_client, fundz_client):
        self.page = page
        self.requests_client = requests_client
        self.fundz_client = fundz_client

    @tornado.gen.coroutine
    def get_existing_request(self, request_id):
        if request_id is None:
            return {}
        request = yield self.requests_client.get("/requests/{}".format(request_id))
        return request.json

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self, screen=1, request_id=None):
        self.check_xsrf_cookie()
        screen = int(screen)
        post_data = self.request.arguments
        current_user = self.get_current_user()
        existing_request = yield self.get_existing_request(request_id)
        jedi_flow = JEDIRequestFlow(
            self.requests_client,
            self.fundz_client,
            screen,
            post_data=post_data,
            request_id=request_id,
            current_user=current_user,
            existing_request=existing_request,
        )

        rerender_args = dict(
            f=jedi_flow.form,
            data=post_data,
            page=self.page,
            screens=jedi_flow.screens,
            current=screen,
            next_screen=jedi_flow.next_screen,
            request_id=jedi_flow.request_id,
        )

        if jedi_flow.validate():
            response = yield jedi_flow.create_or_update_request()
            if response.ok:
                valid = yield jedi_flow.validate_warnings()
                if valid:
                    if jedi_flow.next_screen >= len(jedi_flow.screens):
                        where = "/requests"
                    else:
                        where = self.application.default_router.reverse_url(
                            "request_form_update", jedi_flow.next_screen, jedi_flow.request_id
                        )
                    self.redirect(where)
                else:
                    self.render(
                        "requests/screen-%d.html.to" % int(screen),
                        **rerender_args
                    )
            else:
                self.set_status(response.code)
        else:
            self.render(
                "requests/screen-%d.html.to" % int(screen),
                **rerender_args
            )

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, screen=1, request_id=None):
        screen = int(screen)
        request = None

        if request_id:
            response = yield self.requests_client.get(
                "/requests/{}".format(request_id),
                raise_error=False,
            )
            if response.ok:
                request = response.json

        jedi_flow = JEDIRequestFlow(
            self.requests_client, self.fundz_client, screen, request, request_id=request_id
        )

        self.render(
            "requests/screen-%d.html.to" % int(screen),
            f=jedi_flow.form,
            data=jedi_flow.current_step_data,
            page=self.page,
            screens=jedi_flow.screens,
            current=screen,
            next_screen=screen + 1,
            request_id=request_id,
            can_submit=jedi_flow.can_submit
        )


class JEDIRequestFlow(object):
    def __init__(
        self,
        requests_client,
        fundz_client,
        current_step,
        request=None,
        post_data=None,
        request_id=None,
        current_user=None,
        existing_request=None,
    ):
        self.requests_client = requests_client
        self.fundz_client = fundz_client

        self.current_step = current_step
        self.request = request

        self.post_data = post_data
        self.is_post = self.post_data is not None

        self.request_id = request_id
        self.form = self._form()

        self.current_user = current_user
        self.existing_request = existing_request

    def _form(self):
        if self.is_post:
            return self.form_class()(self.post_data)
        elif self.request:
            return self.form_class()(data=self.current_step_data)
        else:
            return self.form_class()()

    def validate(self):
        return self.form.validate()

    @tornado.gen.coroutine
    def validate_warnings(self):
        valid = yield self.form.perform_extra_validation(
            self.existing_request.get('body', {}).get(self.form_section),
            self.fundz_client,
        )
        return valid

    @property
    def current_screen(self):
        return self.screens[self.current_step - 1]

    @property
    def form_section(self):
        return self.current_screen["section"]

    def form_class(self):
        return self.current_screen["form"]

    @property
    def current_step_data(self):
        data = {}

        if self.is_post:
            data = self.post_data

        if self.request:
            if self.form_section == "review_submit":
                data = self.request["body"]
            else:
                data = self.request["body"].get(self.form_section, {})

        return defaultdict(lambda: defaultdict(lambda: 'Input required'), data)

    @property
    def can_submit(self):
        return self.request and self.request["status"] != "incomplete"

    @property
    def next_screen(self):
        return self.current_step + 1

    @property
    def screens(self):
        return [
            {
                "title": "Details of Use",
                "section": "details_of_use",
                "form": RequestForm,
                "subitems": [
                    {
                        "title": "Overall request details",
                        "id": "overall-request-details",
                    },
                    {"title": "Cloud Resources", "id": "cloud-resources"},
                    {"title": "Support Staff", "id": "support-staff"},
                ],
                "show": True,
            },
            {
                "title": "Information About You",
                "section": "information_about_you",
                "form": OrgForm,
                "show": True,
            },
            {
                "title": "Primary Point of Contact",
                "section": "primary_poc",
                "form": POCForm,
                "show": True,
            },
            {
                "title": "Review & Submit",
                "section": "review_submit",
                "form": ReviewForm,
                "show":True,
            },
        ]

    @tornado.gen.coroutine
    def create_or_update_request(self):
        request_data = {
            "creator_id": self.current_user["id"],
            "request": {self.form_section: self.form.data},
        }
        if self.request_id:
            response = yield self.requests_client.patch(
                "/requests/{}".format(self.request_id), json=request_data
            )
        else:
            response = yield self.requests_client.post("/requests", json=request_data)
            self.request = response.json
            self.request_id = self.request["id"]

        return response
