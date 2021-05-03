
# uvicorn is required if you want do debug your API before containerization
# >> starts server on localhost
import uvicorn

# requests is required to send http requests (e.g. GET, POST) to a REST API
import requests

# import FastAPI framework to build the API
from fastapi import FastAPI, Request, Form

# import further components of FastAPI
# >> Jinja2Template, HTMLResponse: required for frontend
# >> StaticFiles: required to serve static files (css-file in our case)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# create FastAPI-object
app = FastAPI()

# mount folder "/static" to FastAPI-object to serve files in this folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# determine directory for frontend templates
templates = Jinja2Templates(directory="templates")


# specify root-message when opening the summarization-API-localhost
@app.get("/")
async def root():
    return {"message": """Test the swagger API via http://localhost:8000/docs and the frontend via http://localhost:8000/summarization_app"""}


# initialize GET-request for initial frontend based on item.html in /templates
@app.get("/summarization_app", response_class=HTMLResponse)
async def summarization(request: Request):
    summary = "Please insert some text in the input-box."
    return templates.TemplateResponse("item.html", context={"request": request, "summary": summary})


# POST-request to send data from frontend to the summarization microservice
# via the central-API
@app.post("/summarization_app", response_class=HTMLResponse)
async def summarization(request: Request, txt: str = Form(...), ratio: float = Form(...)): 

    """
    Parameters
    ----------
    request: Request 
        Will return a template.
    txt: str
        Text to be summarized submitted from the frontend
    ratio: float
        Proportion of total number of sentences. If the ratio falls under 1/#(number of sentences) nothing will be returned.
    """

    # specify the URL that the POST-request needs to be sent to
    # to receive the summarization
    # url = "http://localhost:8001/summarization-api/"
    url = "http://summary-api:8001/summarization-api/"

    # specify request-body and -parameter to fit summarization-microservice
    body = {"text": txt, 
            "ratio": ratio}

    # send POST-request to summarization-microservice and save the response
    response = requests.request("POST", url, json = body)

    # response only shows that the request was successful (or not)
    # >> the response-body containing the actual text-summary is accessed here
    summary = response.json()

    # return the text-summary embedded in the frontend
    # >> frontend-template is specified as "item.html" in the /templates-folder
    return templates.TemplateResponse("item.html", context={"request": request, "summary": summary})
