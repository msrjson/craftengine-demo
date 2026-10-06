"""Auth controller - login, register, logout, and dashboard."""

from craft.facades import Auth
from craft.http.controller import Controller
from craft.http.response import redirect
from craft.support import __

from app.Http.Requests.Auth.LoginRequest import LoginRequest
from app.Http.Requests.Auth.RegisterRequest import RegisterRequest
from app.Models.User import User


class AuthController(Controller):
    """Sign-in, registration and sign-out.

    Validation and the anti-spam check live in the FormRequests beside this
    file; `passes()` runs both. A failure goes back to the form with the errors
    and the input the visitor typed - never the password.
    """

    def show_login(self, request):
        return self.view("auth.login")

    def show_signin(self, request):
        return redirect(route="login")

    def login(self, request):
        form = LoginRequest(request)
        if not form.passes():
            return self._back(request, form.errors, "/login")

        credentials = {"email": request.get_input("email"), "password": request.get_input("password")}
        if Auth.attempt(credentials):
            return redirect(route="home")
        return self._back(request, {"email": [__("auth.login.failed")]}, "/login")

    def show_register(self, request):
        return self.view("auth.register")

    def register(self, request):
        form = RegisterRequest(request)
        if not form.passes():
            return self._back(request, form.errors, "/register")

        user = User.create({
            "name": (request.get_input("name") or "").strip(),
            "email": (request.get_input("email") or "").strip(),
            "password": request.get_input("password") or "",
        })
        Auth.login(user)
        return redirect(route="home")

    def logout(self, request):
        Auth.logout()
        return redirect(route="login")

    def dashboard(self, request):
        return self.view("auth.dashboard", {"user": Auth.user()})

    @staticmethod
    def _back(request, errors, form_path):
        """Return to the form with errors and every field except the password.

        The form's own path is the fallback: without a Referer header - a
        privacy setting, a script, a test client - going "back" landed on the
        home page, and the errors were flashed to a page that never shows them.
        """
        kept = {key: value for key, value in request.all().items() if "password" not in key}
        return redirect.back(request, fallback=form_path).with_errors(errors).with_input(kept)
