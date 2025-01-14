from typing import Optional

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient
from vonage_jwt.verify_jwt import verify_signature
from vonage_utils.types import Dtmf
from vonage_voice.models.ncco import NccoAction

from .models.requests import (
    AudioStreamOptions,
    CreateCallRequest,
    ListCallsFilter,
    TtsStreamOptions,
)
from .models.responses import CallInfo, CallList, CallMessage, CreateCallResponse


class Voice:
    """Calls Vonage's Voice API."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Voice API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Voice API.
        """
        return self._http_client

    @validate_call
    def create_call(self, params: CreateCallRequest) -> CreateCallResponse:
        """Creates a new call using the Vonage Voice API.

        Args:
            params (CreateCallRequest): The parameters for the call.

        Returns:
            CreateCallResponse: The response object containing information about the created call.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/v1/calls',
            params.model_dump(by_alias=True, exclude_none=True),
        )

        return CreateCallResponse(**response)

    @validate_call
    def list_calls(
        self, filter: ListCallsFilter = ListCallsFilter()
    ) -> tuple[list[CallInfo], Optional[int]]:
        """Lists calls made with the Vonage Voice API.

        Args:
            filter (ListCallsFilter): The parameters to filter the list of calls.

        Returns:
            tuple[list[CallInfo], Optional[int]] A tuple containing a list of `CallInfo` objects and the
                value of the `record_index` attribute to get the next page of results, if there
                are more results than the specified `page_size`.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            '/v1/calls',
            filter.model_dump(by_alias=True, exclude_none=True),
        )

        list_response = CallList(**response)
        if list_response.links.next is None:
            return list_response.embedded.calls, None
        next_page_index = list_response.record_index + 1
        return list_response.embedded.calls, next_page_index

    @validate_call
    def get_call(self, call_id: str) -> CallInfo:
        """Gets a call by ID.

        Args:
            call_id (str): The ID of the call to retrieve.

        Returns:
            CallInfo: Object with information about the call.
        """
        response = self._http_client.get(
            self._http_client.api_host, f'/v1/calls/{call_id}'
        )

        return CallInfo(**response)

    @validate_call
    def transfer_call_ncco(self, uuid: str, ncco: list[NccoAction]) -> None:
        """Transfers a call to a new NCCO.

        Args:
            uuid (str): The UUID of the call to transfer.
            ncco (list[NccoAction]): The new NCCO to transfer the call to.
        """
        serializable_ncco = [
            action.model_dump(by_alias=True, exclude_none=True) for action in ncco
        ]
        self._http_client.put(
            self._http_client.api_host,
            f'/v1/calls/{uuid}',
            {
                'action': 'transfer',
                'destination': {'type': 'ncco', 'ncco': serializable_ncco},
            },
        )

    @validate_call
    def transfer_call_answer_url(self, uuid: str, answer_url: str) -> None:
        """Transfers a call to a new answer URL.

        Args:
            uuid (str): The UUID of the call to transfer.
            answer_url (str): The new answer URL to transfer the call to.
        """
        self._http_client.put(
            self._http_client.api_host,
            f'/v1/calls/{uuid}',
            {'action': 'transfer', 'destination': {'type': 'ncco', 'url': [answer_url]}},
        )

    def hangup(self, uuid: str) -> None:
        """Ends the call for the specified UUID, removing them from it.

        Args:
            uuid (str): The UUID to end the call for.
        """
        self._http_client.put(
            self._http_client.api_host, f'/v1/calls/{uuid}', {'action': 'hangup'}
        )

    def mute(self, uuid: str) -> None:
        """Mutes a call for the specified UUID.

        Args:
            uuid (str): The UUID to mute the call for.
        """
        self._http_client.put(
            self._http_client.api_host, f'/v1/calls/{uuid}', {'action': 'mute'}
        )

    def unmute(self, uuid: str) -> None:
        """Unmutes a call for the specified UUID.

        Args:
            uuid (str): The UUID to unmute the call for.
        """
        self._http_client.put(
            self._http_client.api_host, f'/v1/calls/{uuid}', {'action': 'unmute'}
        )

    def earmuff(self, uuid: str) -> None:
        """Earmuffs a call for the specified UUID (prevents them from hearing audio).

        Args:
            uuid (str): The UUID you want to prevent from hearing audio.
        """
        self._http_client.put(
            self._http_client.api_host, f'/v1/calls/{uuid}', {'action': 'earmuff'}
        )

    def unearmuff(self, uuid: str) -> None:
        """Allows the specified UUID to hear audio.

        Args:
            uuid (str): The UUID you want to to allow to hear audio.
        """
        self._http_client.put(
            self._http_client.api_host, f'/v1/calls/{uuid}', {'action': 'unearmuff'}
        )

    @validate_call
    def play_audio_into_call(
        self, uuid: str, audio_stream_options: AudioStreamOptions
    ) -> CallMessage:
        """Plays an audio stream into a call.

        Args:
            uuid (str): The UUID of the call to stream audio into.
            stream_audio_options (StreamAudioOptions): The options for streaming audio.

        Returns:
            CallMessage: Object with information about the call.
        """
        response = self._http_client.put(
            self._http_client.api_host,
            f'/v1/calls/{uuid}/stream',
            audio_stream_options.model_dump(by_alias=True, exclude_none=True),
        )

        return CallMessage(**response)

    def stop_audio_stream(self, uuid: str) -> CallMessage:
        """Stops streaming audio into a call.

        Args:
            uuid (str): The UUID of the call to stop streaming audio into.

        Returns:
            CallMessage: Object with information about the call.
        """
        response = self._http_client.delete(
            self._http_client.api_host, f'/v1/calls/{uuid}/stream'
        )

        return CallMessage(**response)

    @validate_call
    def play_tts_into_call(self, uuid: str, tts_options: TtsStreamOptions) -> CallMessage:
        """Plays text-to-speech into a call.

        Args:
            uuid (str): The UUID of the call to play text-to-speech into.
            tts_options (TtsStreamOptions): The options for playing text-to-speech.

        Returns:
            CallMessage: Object with information about the call.
        """
        response = self._http_client.put(
            self._http_client.api_host,
            f'/v1/calls/{uuid}/talk',
            tts_options.model_dump(by_alias=True, exclude_none=True),
        )

        return CallMessage(**response)

    def stop_tts(self, uuid: str) -> CallMessage:
        """Stops playing text-to-speech into a call.

        Args:
            uuid (str): The UUID of the call to stop playing text-to-speech into.

        Returns:
            CallMessage: Object with information about the call.
        """
        response = self._http_client.delete(
            self._http_client.api_host, f'/v1/calls/{uuid}/talk'
        )

        return CallMessage(**response)

    @validate_call
    def play_dtmf_into_call(self, uuid: str, dtmf: Dtmf) -> CallMessage:
        """Plays DTMF tones into a call.

        Args:
            uuid (str): The UUID of the call to play DTMF tones into.
            dtmf (Dtmf): The DTMF tones to play, as a string of digits. It can include
                the characters from 0-9, #, *, and p.

        Returns:
            CallMessage: Object with information about the call.
        """
        response = self._http_client.put(
            self._http_client.api_host,
            f'/v1/calls/{uuid}/dtmf',
            {'digits': dtmf},
        )

        return CallMessage(**response)

    @validate_call
    def download_recording(self, url: str, file_path: str) -> None:
        """Downloads a call recording from the specified URL and saves it to a local file.

        Args:
            url (str): The URL of the recording to get.
            file_path (str): The path to save the recording to.
        """
        self._http_client.download_file_stream(url=url, file_path=file_path)

    @validate_call
    def verify_signature(self, token: str, signature: str) -> bool:
        """Verifies that a token has been signed with the provided signature. Used to
        verify that a webhook was sent by Vonage.

        Args:
            token (str): The token to verify.
            signature (str): The signature to verify the token against.

        Returns:
            bool: True if the token was signed with the provided signature, False otherwise.

        Raises:
            VonageVerifyJwtError: The signature could not be verified.
        """
        return verify_signature(token, signature)
