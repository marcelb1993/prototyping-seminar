
# uvicorn is required if you want do debug your API before containerization
# >> starts server on localhost
import uvicorn

# requests is required to send http requests (e.g. GET, POST) to a REST API
import requests

# import FastAPI framework to build the API
from fastapi import FastAPI


# create FastAPI-object
app = FastAPI()

# specify root-message when opening the summarization-API-localhost
@app.get("/")
async def root():
    return {"message": """Test the swagger API via http://localhost:8000/docs and the frontend via http://localhost:8000/summarization_app"""}

# POST-request to send data from frontend to the summarization microservice
# via the central-API
@app.post("/summarization_app")
async def summarization(txt: str, ratio: float): 

    """
    Parameters
    ----------
    txt: str
        Text to be summarized
    ratio: float
        Proportion of total number of sentences. If the ratio falls under 1/#(number of sentences) nothing will be returned.
    """

    # specify the URL that the POST-request needs to be sent to
    # to receive the summarization 
    #url = "http://summary-api:8001/summarization-api/"
    url = "http://localhost:8001/summarization-api/"


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
    return summary

# DEBUGGING SETUP
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
