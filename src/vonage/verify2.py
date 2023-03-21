from pydantic import BaseModel, conint, constr, ValidationError, parse_obj_as
from typing import Optional, Literal, List
import copy

from .errors import Verify2Error


allowed_channels = 'sms', 'whatsapp', 'whatsapp_interactive', 'voice', 'email', 'silent_auth'


class VerifyWorkflow(BaseModel):
    channel: Literal['sms', 'whatsapp', 'whatsapp_interactive', 'voice', 'email', 'silent_auth']


class SmsWorkflow(VerifyWorkflow):
    to: constr(regex=r'^[1-9]\d{6,14}$')
    app_hash: Optional[constr(min_length=11, max_length=11)]


class VerifyRequest(BaseModel):
    locale: Optional[str]
    channel_timeout: Optional[conint(ge=60, le=900)]
    client_ref: Optional[str]
    code_length: Optional[conint(ge=4, le=10)]
    brand: str
    workflow: List[VerifyWorkflow]


class Verify2:
    def __init__(self, client):
        self._client = client
        self._auth_type = 'jwt'

    def new_request(self, params: dict):
        if 'workflow' not in params:
            raise Verify2Error(
                'You must provide the workflow for the verification request as a dictionary, inside a list, inside the params object.'
            )
        if 'channel' not in params['workflow'][0] or params['workflow'][0]['channel'] not in allowed_channels:
            raise Verify2Error(f'You must specify a valid verify channel, one of: {allowed_channels}')

        params_to_verify = copy.deepcopy(params)
        if params['workflow'][0]['channel'] == 'sms':
            params_to_verify['workflow'][0] = SmsWorkflow.parse_obj(params['workflow'][0])

        try:
            VerifyRequest.parse_obj(params_to_verify)
        except ValidationError as v:
            raise Verify2Error(
                f'Invalid input params to the verify v2 request. Validation error received:\n {v.json()}'
            )

        if not hasattr(self._client, '_application_id'):
            self._auth_type = 'header'

        return self._client.post(
            self._client.api_host(),
            '/v2/verify',
            params,
            auth_type=self._auth_type,
        )

    def check_code(self, request_id: str, code: str):
        params = {'code': code}

        if not hasattr(self._client, '_application_id'):
            self._auth_type = 'header'
        return self._client.post(
            self._client.api_host(),
            f'/v2/verify/{request_id}',
            params,
            auth_type=self._auth_type,
        )
