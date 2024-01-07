import requests, json, random
from bs4 import BeautifulSoup

class report:
    def __init__(self):
        self.cookie = self._get_random_cookie()
        self.session = self._create_session()


    def _get_random_cookie(self):
        with open('./assets/cookies.json', 'r') as file:
            cookies = json.load(file)

        return random.choice(cookies)
    
    def _create_session(self):
        session = requests.Session()

        xcsrf_token_response = requests.post("https://auth.roblox.com/v2/logout", cookies={".ROBLOSECURITY": self.cookie})
        xcsrf_token = xcsrf_token_response.headers["x-csrf-token"]

        session.cookies.update({".ROBLOSECURITY": self.cookie})
        session.headers.update({"referer": "https://www.roblox.com", "x-csrf-token": xcsrf_token})

        return session
    
    def _select_random_report_reason(self):
        with open('./assets/reportMsgs.json', 'r') as file:
            sentences = json.load(file)

        return random.choice(sentences)
        

    def _get_request_verification_token(self, asset_id):
        html_response = self.session.get(f"https://www.roblox.com/abusereport/asset?id={asset_id}")
        soup = BeautifulSoup(html_response.text, "html.parser")
        request_verification_token = soup.find("input", {"name": "__RequestVerificationToken"}).attrs["value"]
        return request_verification_token

    def report_abuse(self, asset_id):
        request_verification_token = self._get_request_verification_token(asset_id)

        data = {
            "__RequestVerificationToken": request_verification_token,
            "ReportCategory": 7,
            "Comment": self._select_random_report_reason(),
            "Id": asset_id,
            "RedirectUrl": f"https://www.roblox.com/games/{asset_id}/",
            "PartyGuid": "",
            "ConversationId": ""
        }

        report_response = self.session.post(
            f"https://www.roblox.com/abusereport/asset?id={asset_id}&redirecturl=%2fgames%2f{asset_id}%2f",
            data=data
        )

        return report_response.status_code, report_response.json


def main():
    asset_id = 15764571875
    reporter = report()
    status_code = reporter.report_abuse(asset_id)

    print(status_code)

if __name__ == "__main__":
    main()
