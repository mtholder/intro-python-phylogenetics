#  HTTP and requests background
Static web sites simply serve up the same information every time a user visits.
Many sites that are of interest to scientists are dynamic because they provide
    users with a view on a (changing) data store.
For instance, "GenBank" refers to both a web site that you can visit, but also
    (and more importantly) the data stores of sequence data that has been deposited.

It is often useful to think about a data-base-driven web site's architecuture, 
    by decomposing it into "front end" and "back end" code.
Front end code determines how the site appears to the users and how users interact
    with the site.
The back end code provides access to the data in a reliable manner through an "API."

An API is an "application programmer interface" - essentially it is a protocol
    for programmers to use when interacting with another computational resource.
A library of code (a "package" in Python) has an API that dictates
    the correct way to interact with the library.

### "front end" of web apps (not the focus of this workshop)
Front end programming technologies interact with your
    web browser using HTML (to describe the basic content to be rendered to the user),
    CSS (an ugly set of conventions for describing how to display the elements of HTML
    to the user), and JavaScript.
JavaScript is an interpreted language that is interpreted by your browser - your
    browser acts like the Python executable to run the JavaScript code whenever
    you load a page which contains JavaScript.
JavaScript is great for making sites interactive, because the appearance of behavior
    of a page can change in response to user's actions without having to reload
    data from the remote web server.

Frequently JavaScript is also used to coordinate the fetching of the data from the
    back end using the API.
In sites using this approach, your initial load of a page gives you shell of page, and
    the JavaScript code (once the core document is loaded) then starts to fetch relevant
    data from the back end and fill out the page.

Learning HTML and CSS is great if you want to design a web site.
But if you just want to interact with a remote data store, it is nice to be able
    to call the back end APIs from your scripts without the use of a web browser
    and without obscuring the structure of the data by embedding it in HTML tags.

*Optional:* If you use Google Chrome you can enable, `Developer Tools` to show up in the `Tools`
    menu. This will let you debug JavaScript code execution.
    You can also examine the web service calls that the page's JavaScript performs (check
    the "Network" tab of the dev tools, and reload the page of interest to fill that tab).

### "back end" of web apps
HTTP is a protocol for exchanging information between programs (which may be running
    on different machines).
Most of us are used to seeing HTTP as the first part of URL, because it is the protocol
    used by the web browser (a program running on your machine) fetches web pages
    from a http server (a program running on a remote "server").
But we can also use HTTP to exchange raw data in different forms.
The API layer of many website now uses the combination of:

   * HTTP as a protocol for how to let different programs talk to each other, and
   * JSON as a syntax for representing data.

JSON is a simple syntax that looks a whole lot like the syntax we use for writing
    string, numeric, list, and dict literals in Python.
In fact it is an object literal syntax of JavaScript (which gives it the name
    "JavaScript Object Notation").

HTTP describes how programs pass streams of data back and forth to one another.
If you know a web API is using JSON, then your code knows how to format its input
    data and interpret the response data.

The Open Tree of Life web API that we'll use for this step is a http + JSON web API.

## Basics of HTTP
Making an HTTP request is a lot like making a function call. 

  * The URL is kind of like the function name - it conveys which function to call.
  * You can pass in arguments to the function by a body of the HTTP request (or through
    encoding key-value pairs in an optional part of the URL)
  * The server gives you a response that is like the return value of a function.

Unfortunately, there are a few details that you need to know about...

#### HTTP "verbs"
Rather than thinking of a URL as a function name, it is more accurate to think of it as
    the name of a "resource" (the word "resource" is intentionally vague).
HTTP's analog of a function name in a programming language is the combination of a 
    verb and the URL.
We don't see the verb used by our web-browser when we type in an address (the verb GET
    is the default verb), so most users are unaware of this aspect of HTTP.
    
The correct name for the HTTP verb is the HTTP "Request Method" - you can read about
    them [on Wikipedia](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods)
    or in the [HTTP Spec](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html) if you
    are the kind of person who likes the gory details.

In this exercise we'll use the python [requests](http://docs.python-requests.org/en/master/)
    package to perform HTTP calls.
The `requests.get` function takes a URL as an argument, and it uses the GET HTTP verb 
    to perform the operation.
You have to use `requests.post` if the API requires the POST verb, *et cetera*.

When using a web API, you need to check the API docs to see what HTTP verbs are used
    for each call.
Using the wrong verb will result in errors.


#### HTTP status code
In addition to the HTTP response having a body that contains the data returned, the
    protocol also demands that the server return a numeric status code.

Codes in the 200's correspond to some type of success.
You can see the full list [here](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes),
    and you are probably familiar with seeing the 404 code
    when you type a URL incorrectly (or click on a broken link).

The `requests` package returns a response object for every HTTP call that does not time out.
It has a handy `raise_for_status()` method that will raise a Python exception
    if the status code indicates that there was an error.
This is a common source of confusion for new users because even a status code in the 
    400's or 500's (indicating client or server errors) may contain
    a body in the response.
Some web APIs have a different form of JSON returned in the event of an error.
So, just being able to extract a JSON structure out of the response does not mean that
    the intent of your request has been fulfilled - you have to check the status code.

#### HTTP headers
Behind the scenes, the client and server are exchanging streams of data, so it is
    important that they know how to decode that stream of bytes into data structures.
There is a `headers` aspect of the HTTP request that tells the server how to interpret
    the argument stream of information and what types of responses the client can
    deal with.
The `Accept` header tells the server what the client can accept, and the `Content-Type`
    header tells the server how to decode the arguments that are sent to the server.



In fact there are a wide variety of header fields (see [here](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields#Request_fields)
for a more exhaustive list) that affect how a request is dealt with.
If you are ever find that you can fetch data from an API when you are using your 
    browser, but not from your scripts, it is a good idea to check the headers
    and authentication parts of the HTTP interactions.

The `requests` package's HTTP functions take an optional `headers` argument that
    can accept a dictionary headers for the call.

#### the HTTP response payload
From the response object returned by a requests call, you can get a string representation
    of the response body as a `text` attribute:
    
    resp = requests.get(...)
    print(resp.text)

If you know that the content is encoded as JSON, then requests will convert it to the 
    equivalent Python representation of the JSON object with the `json` attribute:

    resp = requests.get(...)
    obj = resp.json()


## Setup
    pip install --upgrade requests