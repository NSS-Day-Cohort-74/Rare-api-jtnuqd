import json
from http.server import HTTPServer
from request_handler import HandleRequests, status
from views import (
    create_user,
    login_user,
    view_all_posts,
    view_all_tags,
    view_all_categories,
    view_post_detail,
    create_post,
    create_category,
    create_tag,
    get_current_user_posts,
)


class JSONServer(HandleRequests):

    def do_GET(self):
        """Handle GET requests from a client"""
        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                response_body = view_post_detail(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            else:
                response_body = view_all_posts()
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
        elif url["requested_resource"] == "tags":
            response_body = view_all_tags()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        elif url["requested_resource"] == "categories":
            # print("hitting categories")
            response_body = view_all_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        elif url["requested_resource"] == "myposts":
            if url["pk"] != 0:
                response_body = get_current_user_posts(url["pk"])
                print(response_body)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            return self.response(
                "", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value
            )
        else:
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

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
        elif url["requested_resource"] == "login":
            new_item = login_user(parsed_body)
            return self.response(new_item, status.HTTP_200_SUCCESS.value)
        elif url["requested_resource"] == "posts":
            new_item = create_post(parsed_body)
            # Return new post's ID to the client
            return self.response(str(new_item), status.HTTP_201_SUCCESS_CREATED.value)
        elif url["requested_resource"] == "categories":
            new_item = create_category(parsed_body)
            return self.response(
                "",
                status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value,
            )
        elif url["requested_resource"] == "tags":
            new_item = create_tag(parsed_body)
            return self.response("", status.HTTP_201_SUCCESS_CREATED.value)
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
