import symphony.rest.endpoints as sym_ep

from symphony.api_base import APIBase


class User(APIBase):
    def __init__(self, session):
        super().__init__(session)

    def list_user_groups(self):
        ep = self.get_endpoint(sym_ep.list_user_groups("ROLE_SCOPE"))

        return self.get(ep)

    def create_service_user(self, first_name: str, last_name: str, email: str, username: str, public_key: str):
        user = {
            "userAttributes": {
                "accountType": "SYSTEM",
                "emailAddress": email,
                "firstName": first_name,
                "lastName": last_name,
                "userName": username,
                "currentKey": {"key": public_key}
            }
        }

        # for key, value in kwargs.items():
        #     user["userAttributes"][key] = value

        ep = self.get_endpoint(sym_ep.create_user())

        return self.post(ep, user)