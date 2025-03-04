import json
from http.server import HTTPServer
from request_handler import HandleRequests, status
from views import create_user


class JSONServer(HandleRequests):

    def do_GET(self):
        # """Handle GET requests from a client"""
        # response_body = ""
        # url = self.parse_url(self.path)

        # if url["requested_resource"] == "register":
        #     if url["pk"] != 0:
        #         response_body = retrieve_user(url["pk"])
        #         return self.response(response_body, status.HTTP_200_SUCCESS.value)

        #     response_body = list_docks()
        #     return self.response(response_body, status.HTTP_200_SUCCESS.value)

        # else:
        #     return self.response(
        #         "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
        #     )
        pass

    def do_PUT(self):
        pass

    def do_POST(self):
        """Handle POST requests from a client"""
        url = self.parse_url(self.path)
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        decoded = request_body.decode("utf-8")  # Convert bytes to string
        parsed_body = json.loads(decoded)  # Parse JSON string into dictionary

        new_item = None

        if url["requested_resource"] == "register":
            new_item = create_user(parsed_body)
            return self.response(new_item, status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return self.response(
                "Invalid resource",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )

    def do_DELETE(self):
        pass


def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
