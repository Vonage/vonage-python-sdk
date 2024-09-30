from typing import List

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient
from vonage_video.models.audio_connector import AudioConnectorData, AudioConnectorOptions
from vonage_video.models.captions import CaptionsData, CaptionsOptions
from vonage_video.models.experience_composer import (
    ExperienceComposer,
    ExperienceComposerOptions,
)
from vonage_video.models.session import SessionOptions, VideoSession
from vonage_video.models.signal import SignalData
from vonage_video.models.stream import StreamInfo, StreamLayoutOptions
from vonage_video.models.token import TokenOptions


class Video:
    """Calls Vonage's Video API."""

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
    def generate_client_token(self, token_options: TokenOptions) -> bytes:
        """Generates a client token for the Vonage Video API.

        Args:
            token_options (TokenOptions): The options for the token.

        Returns:
            str: The client token.
        """
        return self._http_client.auth.generate_application_jwt(
            token_options.model_dump(exclude_none=True)
        )

    @validate_call
    def create_session(self, options: SessionOptions = None) -> VideoSession:
        """Creates a new session for the Vonage Video API.

        Args:
            options (SessionOptions): The options for the session.

        Returns:
            VideoSession: The new session ID, plus the config options specified in `options`.
        """

        response = self._http_client.post(
            self._http_client.video_host,
            '/session/create',
            options.model_dump(by_alias=True, exclude_none=True) if options else None,
            sent_data_type='form',
        )

        session_response = {
            'session_id': response[0]['session_id'],
            **(options.model_dump(exclude_none=True) if options else {}),
        }

        return VideoSession(**session_response)

    @validate_call
    def list_streams(self, session_id: str) -> List[StreamInfo]:
        """Lists the streams in a session from the Vonage Video API.

        Args:
            session_id (str): The session ID.

        Returns:
            List[StreamInfo]: Information about the video streams.
        """

        response = self._http_client.get(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/stream',
        )

        return [StreamInfo(**stream) for stream in response['items']]

    @validate_call
    def get_stream(self, session_id: str, stream_id: str) -> StreamInfo:
        """Gets a stream from the Vonage Video API.

        Args:
            session_id (str): The session ID.
            stream_id (str): The stream ID.

        Returns:
            StreamInfo: Information about the video stream.
        """

        response = self._http_client.get(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/stream/{stream_id}',
        )

        return StreamInfo(**response)

    @validate_call
    def change_stream_layout(
        self, session_id: str, stream_layout_options: StreamLayoutOptions
    ) -> List[StreamInfo]:
        """Changes the layout of a stream in a session in the Vonage Video API.

        Args:
            session_id (str): The session ID.
            stream_layout_options (StreamLayoutOptions): The options for the stream layout.

        Returns:
            List[StreamInfo]: Information about the video streams.
        """

        response = self._http_client.put(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/stream',
            stream_layout_options.model_dump(by_alias=True, exclude_none=True),
        )

        return [StreamInfo(**stream) for stream in response['items']]

    @validate_call
    def send_signal(
        self, session_id: str, data: SignalData, connection_id: str = None
    ) -> None:
        """Sends a signal to a session in the Vonage Video API. If `connection_id` is not provided,
        the signal will be sent to all connections in the session.

        Args:
            session_id (str): The session ID.
            data (SignalData): The data to send in the signal.
            connection_id (str, Optional): The connection ID to send the signal to. If not provided,
                the signal will be sent to all connections in the session.
        """
        if connection_id is not None:
            url = f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/connection/{connection_id}/signal'
        else:
            url = f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/signal'

        self._http_client.post(
            self._http_client.video_host, url, data.model_dump(exclude_none=True)
        )

    @validate_call
    def disconnect_client(self, session_id: str, connection_id: str) -> None:
        """Disconnects a client from a session in the Vonage Video API.

        Args:
            session_id (str): The session ID.
            connection_id (str): The connection ID of the client to disconnect.
        """
        self._http_client.delete(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/connection/{connection_id}',
        )

    @validate_call
    def mute_stream(self, session_id: str, stream_id: str) -> None:
        """Mutes a stream in a session using the Vonage Video API.

        Args:
            session_id (str): The session ID.
            stream_id (str): The stream ID.
        """
        self._http_client.post(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/stream/{stream_id}/mute',
        )

    @validate_call
    def mute_all_streams(
        self, session_id: str, excluded_stream_ids: List[str] = None
    ) -> None:
        """Mutes all streams in a session using the Vonage Video API.

        Args:
            session_id (str): The session ID.
            excluded_stream_ids (List[str], Optional): The stream IDs to exclude from muting.
        """
        params = {'active': True, 'excludedStreamIds': excluded_stream_ids}
        self._toggle_mute_all_streams(session_id, params)

    @validate_call
    def disable_mute_all_streams(self, session_id: str) -> None:
        """Disables muting all streams in a session using the Vonage Video API.

        Args:
            session_id (str): The session ID.
        """
        self._toggle_mute_all_streams(session_id, {'active': False})

    @validate_call
    def _toggle_mute_all_streams(self, session_id: str, params: dict) -> None:
        """Mutes all streams in a session using the Vonage Video API.

        Args:
            session_id (str): The session ID.
            params (dict): The parameters to send in the request.
        """
        self._http_client.post(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/mute',
            params,
        )

    @validate_call
    def start_captions(self, options: CaptionsOptions) -> CaptionsData:
        """Enables captions in a session using the Vonage Video API.

        Args:
            options (CaptionsOptions): Options for the captions.

        Returns:
            CaptionsData: Class containing captions ID.
        """
        response = self._http_client.post(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/captions',
            options.model_dump(exclude_none=True, by_alias=True),
        )

        return CaptionsData(captions_id=response['captionsId'])

    @validate_call
    def stop_captions(self, captions: CaptionsData) -> None:
        """Disables captions in a session using the Vonage Video API.

        Args:
            captions (CaptionsData): The captions data.
        """
        self._http_client.post(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/captions/{captions.captions_id}/stop',
        )

    @validate_call
    def start_audio_connector(self, options: AudioConnectorOptions) -> AudioConnectorData:
        """Starts an audio connector in a session using the Vonage Video API.

        Args:
            options (AudioConnectorOptions): Options for the audio connector.

        Returns:
            AudioConnectorData: Class containing audio connector ID.
        """
        response = self._http_client.post(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/connect',
            options.model_dump(exclude_none=True, by_alias=True),
        )

        return AudioConnectorData(**response)

    @validate_call
    def start_experience_composer(
        self, options: ExperienceComposerOptions
    ) -> ExperienceComposer:
        """Starts an experience composer using the Vonage Video API.

        Args:
            options (ExperienceComposerOptions): Options for the experience composer.

        Returns:
            ExperienceComposer: Class containing experience composer data.
        """

        response = self._http_client.post(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/render',
            options.model_dump(exclude_none=True, by_alias=True),
        )

        return ExperienceComposer(**response)
