from core.requester import Requester

from phases.recon.detect_graphql \
import DetectGraphQL

from phases.schema.introspection \
import Introspection

from phases.fingerprint.apollo \
import Apollo


import argparse

print("[*] Starting GraphQLHunter")
print("[*] URL:",args.u)

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


headers={}

if args.H:

    for h in args.H:

        k,v=h.split(
        ":",
        1
        )

        headers[
        k.strip()
        ]=v.strip()


req=Requester(
args.u,
headers
)


recon=DetectGraphQL(
req
)


if not recon.run():

    print(
    "not graphql"
    )

    exit()


response=req.post(
"{__typename}"
)


apollo=Apollo()

r=apollo.detect(
response
)

if r:

    print(r)


schema=Introspection(
req
)

print(
schema.run()
)