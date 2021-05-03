# FastAPI is our webframework for the REST API
from fastapi import FastAPI, Form

# import uvicorn to start the server which runs the fastapi webframework 
import uvicorn

# with the pydantic basemodel you're able to put data into the body of the request
from pydantic import BaseModel

# summariztion Package
from gensim.summarization.summarizer import summarize # https://radimrehurek.com/gensim_3.8.3/summarization/summariser.html

app = FastAPI()

# BaseModel with text and ratio to define the expected body in the create_summary function 
class Summary_Data(BaseModel):
    text: str
    ratio: float


@app.post("/summarization-api/")
async def create_summary(data: Summary_Data):
    """ Create an extractive summarization with text rank algorithm within the gensim package.
    Parameters
    ----------
    data : Basemodel
        Basemodel with text that should be summarized and the additional ratio parameter.
    Returns
    -------
    result : str
        Returns the inferred summary.
    """
    # get the length wordcount of the input text
    input_text_wordcount = len(data.text.split())

    # get the summary with the summarize function
    summary = summarize(text=data.text, ratio=data.ratio)

    # get wordcount of the output text 
    summary_wordcount = len(summary.split())

    # remove \n from the summary so we don't have that many linebreaks in the result
    summary = summary.replace('\n', '')

    # form the result string
    result = '\n'.join(["Wordcount input text: {}.".format(input_text_wordcount),
                        "Wordcount summary: {}.".format(summary_wordcount),
                        "----------------------------------------------------------------",
                        "Summary: {}".format(summary)])

    return result

# # DEBUGGING SETUP
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8001)