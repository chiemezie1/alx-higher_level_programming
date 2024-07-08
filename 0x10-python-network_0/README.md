## URL

A URL (Uniform Resource Locator) is the address used to access resources on the internet. It consists of several components that define the location of the resource.

## HTTP

HTTP (Hypertext Transfer Protocol) is the protocol used for transferring hypertext requests and information on the internet. It defines how messages are formatted and transmitted, and how web servers and browsers should respond to various commands.

## Reading a URL

A URL typically follows this structure:

```bash
scheme://subdomain.domain:port/path?query#fragment

```

## The Scheme for an HTTP URL

The scheme specifies the protocol to be used. For HTTP URLs, the scheme is `http` or `https` (for secure HTTP).

Example:

```
http://www.example.com
https://www.example.com

```

## Domain Name

A domain name is the main part of a URL that specifies the website's address. It usually consists of a name and a top-level domain (TLD).

Example:

```
example.com

```

## Sub-Domain

A sub-domain is a prefix added to the domain name to help organize and navigate different sections of a website.

Example:

```
blog.example.com

```

## Defining a Port Number in a URL

A port number can be specified after the domain, separated by a colon. If no port is specified, the default port for HTTP is 80 and for HTTPS is 443.

Example:

```
http://www.example.com:8080

```

## Query String

A query string is the part of a URL that contains data to be passed to web applications. It follows the `?` in the URL and consists of key-value pairs separated by `&`.

Example:

```
http://www.example.com/search?q=openai&lang=en

```

## HTTP Request

An HTTP request is a message sent by a client to a server to request a resource. It consists of a request line, headers, and an optional message body.

## HTTP Response

An HTTP response is a message sent by a server to a client in response to an HTTP request. It consists of a status line, headers, and an optional message body.

## HTTP Headers

HTTP headers are key-value pairs in HTTP requests and responses that convey additional information about the request or response.

Example:

```bash
Content-Type: application/json

```

## HTTP Message Body

The HTTP message body is the part of an HTTP request or response that contains the actual data being transferred.

## HTTP Request Method

HTTP request methods indicate the desired action to be performed on a resource. Common methods include:

- `GET`: Retrieve a resource.
- `POST`: Submit data to be processed.
- `PUT`: Update a resource.
- `DELETE`: Delete a resource.

## HTTP Response Status Code

HTTP response status codes indicate the result of the HTTP request. Common status codes include:

- `100 Informational`: The request was received, but not processed.
- `200 OK`: The request was successful.
- `300 Redirect`: The request was redirected.
- `404 Not Found`: The requested resource could not be found.
- `500 Internal Server Error`: The server encountered an error.

## HTTP Cookie

An HTTP cookie is a small piece of data sent from a server and stored on the client's computer. It is used to remember information about the client between requests.

## Making a Request with cURL

`cURL` is a command-line tool for making HTTP requests. Here's an example of a basic GET request:

```
curl http://www.example.com

```
`CURL OPTIONS`
    The `curl` command is a powerful tool used for transferring data with URLs. It supports various protocols, including HTTP, HTTPS, FTP, and many more. Here are some common options used with `curl`:

1. **X, --request <command>**: Specify a custom request method to use when communicating with the HTTP server. For example, `X POST`.
2. **d, --data <data>**: Sends the specified data in a POST request to the HTTP server.
3. **H, --header <header>**: Pass custom header(s) to the server.
4. **u, --user [user:password](https://www.notion.so/20e7b43a9355430dac425401f85b7524?pvs=21)**: Server user and password.
5. **o, --output <file>**: Write output to a file instead of stdout.
6. **O, --remote-name**: Write output to a file named as the remote file.
7. **L, --location**: Follow redirects.
8. **I, --head**: Fetch the headers only.
9. **v, --verbose**: Make the operation more talkative.
10. **s, --silent**: Silent or quiet mode. Don't show progress meter or error messages.
11. **k, --insecure**: Allow connections to SSL sites without certificates.
12. **F, --form <name=content>**: Emulate a filled-in form where `name` is the field name and `content` is the data for that field.
13. **-max-time <seconds>**: Maximum time in seconds that you allow the whole operation to take.
14. **b, --cookie <data|filename>**: Pass the data to the HTTP server as a cookie.
15. **c, --cookie-jar <filename>**: Specify the file to save cookies after the operation.
16. **-compressed**: Request a compressed response using one of the algorithms curl supports (gzip, deflate, or br).

To make a POST request with JSON data:

```
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://www.example.com/ap

```
