from functools import lru_cache

from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse
from typing_extensions import Annotated

import config
import json

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import  ApiException

from dto.signup import *

app = FastAPI()

@lru_cache()
def get_settings():
    return config.Settings()


sib_configuration = sib_api_v3_sdk.Configuration()
sib_configuration.api_key['api-key'] = get_settings().brevo_api_key

contacts_api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(sib_configuration))



@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Ned Finance"

@app.post("/signup-pre-launch")
async def signup(data:SignupPreLaunchRequestDto, settings: Annotated[config.Settings, Depends(get_settings)]):
    contact = sib_api_v3_sdk.CreateContact()
    contact.email = data.email
    contact.list_ids = [3]
    
    try:
        api_response = contacts_api_instance.create_contact(contact)
        
        return SignupPreLaunchResponseDto(
            success= True,
            message= "Contact added successfully"
        )
        
    except ApiException as e:
        res = json.loads(e.body)
        print(res['code'] )
        if res['code'] == 'duplicate_parameter':
            return SignupPreLaunchResponseDto(
                success= False,
                message= "Already subscribed"
            )
        else:
            return SignupPreLaunchResponseDto(
                success= False,
                message= "There was an error please try again"
            )
