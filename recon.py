#!/usr/bin/env python3

import requests
import json
import argparse
import urllib3

urllib3.disable_warnings()

BANNER = r"""
   ____                 _      ____                      
  / ___| _ __ __ _ _ __| |__  |  _ \ ___  ___ ___  _ __  
 | |  _ | '__/ _` | '__| '_ \ | |_) / _ \/ __/ _ \| '_ \
 | |_| || | | (_| | |  | | | ||  _ <  __/ (_| (_) | | | |
  \____||_|  \__,_|_|  |_| |_||_| \_\___|\___\___/|_| |_|

 GraphQL Recon v1
 AWS AppSync Support
"""

INTROSPECTION_QUERY = """
query IntrospectionQuery {
 __schema {
   queryType {
      name
   }
   mutationType{
      name
   }
   types{
      name
      kind
      fields{
         name
      }
   }
 }
}
"""

class GraphQLRecon:

    def __init__(self,url,headers):

        self.url=url

        self.headers=headers

        self.headers.setdefault(
            "Content-Type",
            "application/json"
        )

    def detect_graphql(self):

        payload={

            "query":"{__typename}"

        }

        try:

            r=requests.post(
                self.url,
                json=payload,
                headers=self.headers,
                timeout=15,
                verify=False
            )

            body=r.text

            if "__typename" in body:
                return True

            if '"data"' in body:
                return True

            if "GraphQL" in body:
                return True

            return False

        except Exception:

            return False


    def fingerprint(self):

        print("[*] Fingerprinting")

        payload={

            "query":"{__typename}"

        }

        try:

            r=requests.post(
                self.url,
                json=payload,
                headers=self.headers,
                timeout=10,
                verify=False
            )

            h=r.headers

            body=r.text


            indicators=[]

            if "x-amzn-requestid" in h:
                indicators.append(
                    "x-amzn-requestid"
                )

            if "x-amz-cf-id" in h:
                indicators.append(
                    "CloudFront"
                )

            if "appsync-api" in body.lower():
                indicators.append(
                    "appsync-api"
                )

            if "aws" in str(h).lower():
                indicators.append(
                    "aws"
                )

            if indicators:

                print(
                    "[+] GraphQL Engine: AWS AppSync"
                )

                print(
                    "[+] Indicators:"
                )

                for i in indicators:

                    print("   -",i)

                return "AWS AppSync"

            return None

        except Exception:

            return None


    def schema_dump(self):

        print(
            "[*] Running introspection"
        )

        payload={

            "query":
            INTROSPECTION_QUERY
        }

        r=requests.post(
            self.url,
            json=payload,
            headers=self.headers,
            verify=False
        )

        try:

            data=r.json()

        except:

            print(
                "[-] JSON parse failed"
            )
            return

        if "errors" in data:

            print(
                "[-] Introspection disabled"
            )

            print(
                json.dumps(
                    data,
                    indent=4
                )
            )

            return


        with open(
            "schema.json",
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

        print(
            "[+] Schema saved:"
            " schema.json"
        )

        schema=data[
            "data"
        ][
            "__schema"
        ]


        print("\nQueries")

        qt=schema.get(
            "queryType"
        )

        print(qt)


        print(
            "\nMutations"
        )

        mt=schema.get(
            "mutationType"
        )

        print(mt)


        print(
            "\nTypes"
        )

        for t in schema[
            "types"
        ]:

            print(
                "-",
                t["name"]
            )


def parse_headers(items):

    h={}

    if not items:
        return h

    for item in items:

        key,value=item.split(
            ":",
            1
        )

        h[
            key.strip()
        ]=value.strip()

    return h



def main():

    print(BANNER)

    parser=argparse.ArgumentParser()

    parser.add_argument(
        "-u",
        required=True
    )

    parser.add_argument(
        "-H",
        action="append"
    )

    args=parser.parse_args()

    headers=parse_headers(
        args.H
    )

    g=GraphQLRecon(
        args.u,
        headers
    )

    print(
        "[*] Detecting GraphQL"
    )

    if not g.detect_graphql():

        print(
            "[-] GraphQL not detected"
        )

        return

    print(
        "[+] GraphQL detected"
    )

    engine=g.fingerprint()

    if engine=="AWS AppSync":

        g.schema_dump()

    else:

        print(
            "[-] Unknown GraphQL implementation"
        )


if __name__=="__main__":
    main()