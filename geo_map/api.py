import requests


class UnauthorizedException(Exception):
    pass


def auth_decorator(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except UnauthorizedException:
            self.login()
            return func(self, *args, **kwargs)

    return wrapper


class API:

    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self):
        resp = self.session.post(
            f"{self.url}/api/token", data={"username": self.username, "password": self.password}
        )
        if resp.status_code == 200:
            token = resp.json()["access"]
            print("Logged in successfully")
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    @auth_decorator
    def update_layer(self, layer_name: str, file_path: str):
        layer_id = None
        resp = self.session.get(f"{self.url}/maps/api/layers?name={layer_name}")
        if resp.status_code in [401, 403]:
            raise UnauthorizedException(resp.text)

        if resp.status_code == 200:
            data = resp.json()
            print("Layers:", data)
            if len(data) > 0:
                layer_id = data[0]["id"]

        if layer_id is not None:
            form_data = {"from_file": open(file_path, "rb")}
            resp = self.session.patch(f"{self.url}/maps/api/layers/{layer_id}/", files=form_data)
            print(resp)
            if resp.status_code in [401, 403]:
                raise UnauthorizedException(resp.text)
