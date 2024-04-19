from quart import Quart, render_template, request

app = Quart(__name__)


# Some Example function definition
# It does nothing and to demonstrate a basic definition
def do_nothing(param: str):
    "The Function description can be defined as a string statement in the first line of a function"

    # The next command does nothing.
    # Every function needs at least one statement. Empty definitions are not allowed.
    # The "pass" command is therefore just a trick to make the function valid.
    # Same holds for classes for-loops, if-statements, etc.
    # For example:
    #   something = True
    #   if something is True:
    #       print("It is true")
    #   else:
    #       pass
    #
    pass


# Some Examples for string definitions
# It has one input parameter of type string
# It returns an object of type 'None'
# Types are optional.
# If you know what you do you can just ommit them:
# --> Also valid: def print_stuff(param):
def print_stuff(param: str) -> None:
    """
    I am a function description in a multi-line string.
    Therefore Thre double quotes.
    Only One double qoute would also be possible but then has to be a single line.
    Only one single qoute is also a string.
    With f-strings variables can be included into strings.
    """
    foo = """Multiline
    String"""
    bar = "Single line string"
    baz = "Single quotes string"
    qux = f""" Multi-line f-string
    {param}"""
    quux = f"Single line f-string{param}"
    corge = f"Single quotes f-string {param}"
    grault = foo + " SOMETHING " + bar
    print("PRINT_STUFF: %s %s %s %s %s %s %s", foo, bar, baz, qux, quux, corge, grault)
    return None


def i_am_synchronous():
    """
    Synchronous means ''blocking'. The function is invoked immidiately but blocks the main thread!
    """
    print("Synchronous print statement")
    return "sync result text"


async def i_am_asynchronous():
    """
    Asynchronous means 'non-blocking'. The function is started as a new thread and returns immidiately!
    We can wait for such commands by using the "await" statement.
    With await we can turn a ''non-blcoking' call into a 'non-blocking' one.
    """
    print("Asynchronous print statement")
    return "async result text"


async def read_file(filename: str) -> str:
    """
    Reads a file and returns its content as a string
    """
    # The with statement declares a context
    # In the background a "ContextManager" handles creation and deletion of used objects
    # So if a filehandle is opened, the filehandle is only available during its context.
    # The filehandle is automatically closed if the context is left.
    # So its the "clean way" of handling things with a context.
    # The open function has such a ContextManager and has two parameters:
    # Filename and interaction mode. "r" for read, "w" for write, "a" for append and several others...
    # with "as myfile" the contexted-variable is specified and can be used within the context.
    # We put this files in the folder "html" but there is no convention. So we can do what we want.
    with open(filename, "r") as myfile:
        text = myfile.read()
        return text


@app.route("/")
async def landingpage():
    """
    Reads a html textfile and returns it
    Quart expects template files in the subfolder 'templates'
    """

    do_nothing("")

    text = """
    The page is created as a template in the function landingpage()
    It is created by using the render_template() function from the quart library.
    It reads an input file ('template.html') and uses parameters which are put into that file.
    In template.html curly brackets are used to define contexts in which these parameters are valid.
    The text you read now was once a python string and has been put in that way into the textarea in blue.

    Example to use variable 'input_text':
    ... <textarea>{{input_text}}</textarea> ...

    The page as 7 Endpoints:
        /              -> This page ( with render_template() )
        /pictest       -> Uses a static file ( with read_file() )
        /htmltest      -> Reads file to return valid html ( with read_file() )
        /printtest     -> Different styles of printing ( print_stuff() )
        /synctest      -> Examples for sync and async functions ( sync/async )
        /getparameter  -> A simple GET request with a user parameter ( /getparam/abc )
        /postparameter -> A simple POST request with a user parameter ( /postparam and form-arguments )

        Good Luck! ;-)


        def foo(parameter):
            print("foo");

        foo("abc")
    """
    return await render_template(
        "template.html", input_headline="Your Headline", input_text=text
    )


@app.route("/htmltest")
async def htmltest():
    """
    Reads a textfile containing html and returns it

    We put the html file in folder "html", but we can put it wherever we want.
    """

    # Read the text asynchronously
    htmltext = await read_file("html/hello.html")

    # Return html content
    return htmltext


@app.route("/pictest")
async def pictest():
    """
    Reads a html textfile conatining a static file (the image)

    Quart expects static files in the subfolder 'static'
    We put the html file in folder "html", but we can put it wherever we want.
    """

    # Read the text asynchronously
    htmltext = await read_file("html/picture.html")

    # Return html content
    return htmltext


@app.route("/printtest")
async def printtest():
    """Executes print function"""

    # Execute a blocking function
    print_stuff("TEST-TEXT")

    # Return some the texts
    return "ALL PRINTED"


@app.route("/synctest")
async def synctest():
    """Executes blocking and non-blocking functions"""

    # Execute a blocking function
    sync_result = i_am_synchronous()
    print(f"RESULT  SYNC:{sync_result}")

    # Execute a non-blocking function
    async_result = await i_am_asynchronous()
    print(f"RESULT ASYNC:{async_result}")

    # Return some text
    return f"SYNC: {sync_result} ASYNC: {async_result}"


@app.get("/getparam/<testparameter>")
async def getparametertest(testparameter: str):

    # print the received params
    print(f"PARAMETER RECEIVED VIA GET: {testparameter}")

    # Return some text
    return f"You send me this (GET): {testparameter}"


@app.post("/postparam/")
async def postparametertest():

    formargs = await request.form
    param1 = "GOT NOTHING"
    param2 = "GOT NOTHING"
    if "parameter1" in formargs:
        param1 = formargs["parameter1"]
    if "parameter2" in formargs:
        param2 = formargs["parameter2"]

    # print the received params
    print(f"PARAMETER RECEIVED VIA POST: 1:{param1} 2:{param2}")

    # Return some text
    return f"You send me this (POST): 1:{param1}  {param2}"


app.run(host="0.0.0.0", port=4444)

