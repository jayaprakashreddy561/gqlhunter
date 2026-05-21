import requests
import urllib3

urllib3.disable_warnings()

class Requester:

    def __init__(
            self,
            url,
            headers
    ):

        self.url=url
        self.headers=headers

        self.headers.setdefault(
            "Content-Type",
            "application/json"
        )

    def post(
            self,
            query
    ):

        payload={

            "query":query

        }

        print("\n"+"="*60)
        print("[REQUEST]")
        print("URL:",self.url)
        print("Headers:",self.headers)
        print("Payload:",payload)
        print("="*60)

        try:

            r=requests.post(
                self.url,
                json=payload,
                headers=self.headers,
                verify=False,
                timeout=20
            )

            print("\n"+"="*60)
            print("[RESPONSE]")
            print("Status:",r.status_code)

            print("Response Headers:")
            for k,v in r.headers.items():
                print(f"{k}: {v}")

            print("\nBody:\n")

            print(r.text[:1000])

            print("="*60)

            return r

        except Exception as e:

            print("\n[EXCEPTION]")
            print(type(e).__name__)
            print(str(e))

            return None