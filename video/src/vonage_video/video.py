from typing import List

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient
from vonage_video.models.session import SessionOptions, VideoSession
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
            VideoSession: The new session.
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
    def change_stream_layout(
        self, session_id: str, stream_layout_options: StreamLayoutOptions
    ) -> None:
        """Changes the layout of a stream in a session in the Vonage Video API.

        Args:
            session_id (str): The session ID.
            stream_layout_options (StreamLayoutOptions): The options for the stream layout.
        """

        self._http_client.put(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/stream',
            stream_layout_options.model_dump(by_alias=True, exclude_none=True),
        )

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

    def change_stream_layout(
        self, session_id: str, stream_layout_options: StreamLayoutOptions
    ) -> None:
        """Changes the layout of a stream in a session in the Vonage Video API.

        Args:
            session_id (str): The session ID.
            stream_layout_options (StreamLayoutOptions): The options for the stream layout.
        """

        self._http_client.put(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/stream',
            stream_layout_options.model_dump(by_alias=True, exclude_none=True),
        )
