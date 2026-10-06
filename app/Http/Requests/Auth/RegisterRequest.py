"""Registration request validator."""

from craft.validation.form_request import FormRequest


class RegisterRequest(FormRequest):
    antispam = True

    def authorize(self) -> bool:
        return True

    def rules(self) -> dict:
        return {
            "name": ["required", "string", "min:2", "max:100"],
            "email": ["required", "email", "unique:users,email"],
            "password": ["required", "min:8"],
        }
