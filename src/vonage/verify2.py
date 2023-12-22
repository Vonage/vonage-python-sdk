from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import Annotated

if TYPE_CHECKING:
    from vonage import Client

from pydantic import BaseModel, StringConstraints, ValidationError, field_validator, conint
from typing import List

import copy
import re

from ._internal import set_auth_type
from .errors import Verify2Error


class Verify2:
    valid_channels = [
        'sms',
        'whatsapp',
        'whatsapp_interactive',
        'voice',
        'email',
        'silent_auth',
    ]

    def __init__(self, client: Client):
        self._client = client
        self._auth_type = set_auth_type(self._client)

    def new_request(self, params: dict):
        self._remove_unnecessary_fraud_check(params)
        try:
            params_to_verify = copy.deepcopy(params)
            Verify2.VerifyRequest.model_validate(params_to_verify)
        except (ValidationError, Verify2Error) as err:
            raise err

        return self._client.post(
            self._client.api_host(),
            '/v2/verify',
            params,
            auth_type=self._auth_type,
        )

    def check_code(self, request_id: str, code: str):
        params = {'code': str(code)}

        return self._client.post(
            self._client.api_host(),
            f'/v2/verify/{request_id}',
            params,
            auth_type=self._auth_type,
        )

    def cancel_verification(self, request_id: str):
        return self._client.delete(
            self._client.api_host(),
            f'/v2/verify/{request_id}',
            auth_type=self._auth_type,
        )

    def _remove_unnecessary_fraud_check(self, params):
        if 'fraud_check' in params and params['fraud_check'] != False:
            del params['fraud_check']

    class VerifyRequest(BaseModel):
        brand: str
        workflow: List[dict]
        locale: str = None
        channel_timeout: conint(ge=60, le=900) = None
        client_ref: str = None
        code_length: conint(ge=4, le=10) = None
        fraud_check: bool = None
        code: Annotated[str, StringConstraints(
            min_length=4, max_length=10
        )] = None

        @field_validator('code')
        @classmethod
        def regex_check(cls, c: str):
            re_for_code: re.Pattern[str] = re.compile('^(?=[a-zA-Z0-9]{4,10}$)[a-zA-Z0-9]*$')

            if not re_for_code.match(c):
                raise ValueError("string does not match regex")
            return c

        @field_validator('workflow')
        @classmethod
        def check_valid_workflow(cls, v):
            for workflow in v:
                Verify2._check_valid_channel(workflow)
                Verify2._check_valid_recipient(workflow)
                Verify2._check_app_hash(workflow)
                if workflow['channel'] == 'whatsapp' and 'from' in workflow:
                    Verify2._check_whatsapp_sender(workflow)
                if workflow['channel'] == 'silent_auth':
                    Verify2._check_silent_auth_workflow(workflow)

    def _check_valid_channel(workflow):
        if 'channel' not in workflow or workflow['channel'] not in Verify2.valid_channels:
            raise Verify2Error(
                f'You must specify a valid verify channel inside the "workflow" object, one of: "{Verify2.valid_channels}"'
            )

    def _check_valid_recipient(workflow):
        if 'to' not in workflow or (
            workflow['channel'] != 'email' and not re.search(r'^[1-9]\d{6,14}$', workflow['to'])
        ):
            raise Verify2Error(
                f'You must specify a valid "to" value for channel "{workflow["channel"]}"'
            )

    def _check_app_hash(workflow):
        if workflow['channel'] == 'sms' and 'app_hash' in workflow:
            if type(workflow['app_hash']) != str or len(workflow['app_hash']) != 11:
                raise Verify2Error(
                    'Invalid "app_hash" specified. If specifying app_hash, \
                        it must be passed as a string and contain exactly 11 characters.'
                )
        elif workflow['channel'] != 'sms' and 'app_hash' in workflow:
            raise Verify2Error(
                'Cannot specify a value for "app_hash" unless using SMS for authentication.'
            )

    def _check_whatsapp_sender(workflow):
        if not re.search(r'^[1-9]\d{6,14}$', workflow['from']):
            raise Verify2Error('You must specify a valid "from" value if included.')

    def _check_silent_auth_workflow(workflow):
        if 'redirect_url' in workflow:
            if type(workflow['redirect_url']) != str:
                raise Verify2Error('"redirect_url" must be a string if specified.')
        if 'sandbox' in workflow:
            if type(workflow['sandbox']) != bool:
                raise Verify2Error('"sandbox" must be a boolean if specified.')
