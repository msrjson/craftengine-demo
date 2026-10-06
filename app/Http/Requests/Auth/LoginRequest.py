"""Login request validator."""

from craft.validation.form_request import FormRequest


class LoginRequest(FormRequest):
    # The honeypot and time trap rendered by @honeypot in the view are checked
    # by FormRequest.passes(); NR-06 requires them on any public form.
    antispam = True

    def authorize(self) -> bool:
        return True

    def rules(self) -> dict:
        return {
            "email": ["required", "email"],
            "password": ["required", "min:6"],
        }
