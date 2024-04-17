from quart import Quart, render_template, request, jsonify
import random

app = Quart(__name__)


async def read_file(filename: str) -> str:
    """
    Reads a file and returns its content as a string
    """
    with open(filename, "r") as myfile:
        text = myfile.read()
        return text


@app.get("/sensordata/")
async def getparametertest():
    sensordata = [
        random.randint(0, 100),
        random.randint(0, 100),
        random.randint(0, 100),
    ]
    return jsonify(sensordata)


@app.get("/")
async def default_page():
    file = await read_file("html/default.html")
    return file


# @app.post("/postparam/")
# async def postparametertest():
#
#     formargs = await request.form
#     param1 = "GOT NOTHING"
#     param2 = "GOT NOTHING"
#     if "parameter1" in formargs:
#         param1 = formargs["parameter1"]
#     if "parameter2" in formargs:
#         param2 = formargs["parameter2"]
#
#     # print the received params
#     print(f"PARAMETER RECEIVED VIA POST: 1:{param1} 2:{param2}")
#
#     # Return some text
#     return f"You send me this (POST): 1:{param1}  {param2}"
#

app.run(host="0.0.0.0", port=4444)

