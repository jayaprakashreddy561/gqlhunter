import json

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


class Introspection:

    def __init__(
            self,
            requester
    ):

        self.r=requester


    def save_schema(
            self,
            data
    ):

        try:

            with open(
                "output/schema.json",
                "w"
            ) as f:

                json.dump(
                    data,
                    f,
                    indent=4
                )

            print(
                "[+] Schema saved:"
            )

            print(
                "    output/schema.json"
            )

        except Exception as e:

            print(
                "[-] Save failed:",
                e
            )


    def parse(
            self,
            schema
    ):

        print(
            "\n"+"="*50
        )

        print(
            "[SCHEMA SUMMARY]"
        )

        print(
            "="*50
        )


        qt=schema.get(
            "queryType"
        )

        if qt:

            print(
              "\n[Query Root]"
            )

            print(
              "   ",
              qt["name"]
            )


        mt=schema.get(
            "mutationType"
        )

        if mt:

            print(
              "\n[Mutation Root]"
            )

            print(
              "   ",
              mt["name"]
            )


        print(
         "\n[Types]"
        )


        for t in schema[
            "types"
        ]:

            print(
                f"\n{t['name']}"
            )

            print(
                "Kind:",
                t["kind"]
            )

            fields=t.get(
                "fields"
            )

            if not fields:
                continue

            for f in fields:

                print(
                    "   └─",
                    f["name"]
                )


    def run(self):

        print(
            "\n[*] Running Introspection"
        )


        r=self.r.post(
            INTROSPECTION_QUERY
        )


        if not r:

            return None


        try:

            data=r.json()

        except:

            print(
             "[-] Invalid JSON"
            )

            return None


        if "errors" in data:

            print(
             "[-] Introspection blocked"
            )

            print(
              json.dumps(
                 data,
                 indent=4
              )
            )

            return None


        self.save_schema(
            data
        )


        schema=data[
            "data"
        ][
            "__schema"
        ]


        self.parse(
            schema
        )

        return data