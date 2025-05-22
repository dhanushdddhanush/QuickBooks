from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse
app = FastAPI()

load_dotenv()

QBO_TOKEN = os.getenv("QBO_TOKEN")
QBO_REALM_ID = os.getenv("QBO_REALM_ID")



app = FastAPI()

@app.get("/copilot-plugin.json")
def get_manifest():
    manifest_path = os.path.join(os.getcwd(), "copilot-plugin.json")
    return FileResponse(manifest_path, media_type="application/json")


@app.get("/openapi.json")
def custom_openapi():
    return get_openapi(
        title="QuickBooks Invoice Plugin",
        version="1.0.0",
        routes=app.routes,
    )


@app.get("/invoices")
def get_invoices():
    query = "SELECT * FROM Invoice ORDERBY TxnDate DESC MAXRESULTS 10"
    url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{QBO_REALM_ID}/query?query={query}"

    headers = {
        "Authorization": f"Bearer {QBO_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/text"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
