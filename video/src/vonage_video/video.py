from typing import List, Optional, Tuple

from pydantic import validate_call
from vonage_http_client.errors import HttpRequestError
from vonage_http_client.http_client import HttpClient
from vonage_video.errors import InvalidArchiveStateError
from vonage_video.models.archive import (
    AddStreamRequest,
    Archive,
    ComposedLayout,
    CreateArchiveRequest,
    ListArchivesFilter,
)
from vonage_video.models.audio_connector import AudioConnectorData, AudioConnectorOptions
from vonage_video.models.captions import CaptionsData, CaptionsOptions
from vonage_video.models.experience_composer import (
    ExperienceComposer,
    ExperienceComposerOptions,
    ListExperienceComposersFilter,
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
        """Starts an Experience Composer using the Vonage Video API.

        Args:
            options (ExperienceComposerOptions): Options for the Experience Composer.

        Returns:
            ExperienceComposer: Class containing Experience Composer data.
        """

        response = self._http_client.post(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/render',
            options.model_dump(exclude_none=True, by_alias=True),
        )

        return ExperienceComposer(**response)

    @validate_call
    def list_experience_composers(
        self, filter: ListExperienceComposersFilter = ListExperienceComposersFilter()
    ) -> Tuple[List[ExperienceComposer], int, Optional[int]]:
        """Lists Experience Composers associated with your Vonage application.

        Args:
            filter (ListExperienceComposersFilter): Filter for the Experience Composers.

        Returns:
            Tuple[List[ExperienceComposer], int, Optional[int]]: A tuple containing a list of experience
                composer objects, the total count of Experience Composers and the required offset value
                for the next page, if applicable.
                i.e.
                experience_composers: List[ExperienceComposer], count: int, next_page_offset: Optional[int]
        """
        response = self._http_client.get(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/render',
            filter.model_dump(exclude_none=True, by_alias=True),
        )

        index = filter.offset + 1 or 1
        page_size = filter.page_size
        experience_composers = []

        try:
            for ec in response['items']:
                experience_composers.append(ExperienceComposer(**ec))
        except KeyError:
            return [], 0, None

        count = response['count']
        if count > page_size * (index):
            return experience_composers, count, index
        return experience_composers, count, None

    @validate_call
    def get_experience_composer(self, experience_composer_id: str) -> ExperienceComposer:
        """Gets an Experience Composer associated with your Vonage application.

        Args:
            experience_composer_id (str): The ID of the Experience Composer.

        Returns:
            ExperienceComposer: The Experience Composer object.
        """
        response = self._http_client.get(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/render/{experience_composer_id}',
        )

        return ExperienceComposer(**response)

    @validate_call
    def stop_experience_composer(self, experience_composer_id: str) -> None:
        """Stops an Experience Composer associated with your Vonage application.

        Args:
            experience_composer_id (str): The ID of the Experience Composer.
        """
        self._http_client.delete(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/render/{experience_composer_id}',
        )

    @validate_call
    def list_archives(
        self, filter: ListArchivesFilter
    ) -> Tuple[List[Archive], int, Optional[int]]:
        """Lists archives associated with a Vonage Application.

        Args:
            filter (ListArchivesFilter): The filters for the archives.

        Returns:
            Tuple[List[Archive], int, Optional[int]]: A tuple containing a list of archive objects,
                the total count of archives and the required offset value for the next page, if applicable.
                i.e.
                archives: List[Archive], count: int, next_page_offset: Optional[int]
        """
        response = self._http_client.get(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/archive',
            filter.model_dump(exclude_none=True, by_alias=True),
        )

        index = filter.offset + 1 or 1
        page_size = filter.page_size
        archives = []

        try:
            for archive in response['items']:
                archives.append(Archive(**archive))
        except KeyError:
            return [], 0, None

        count = response['count']
        if count > page_size * (index):
            return archives, count, index
        return archives, count, None

    @validate_call
    def start_archive(self, options: CreateArchiveRequest) -> Archive:
        """Starts an archive in a Vonage Video API session.

        Args:
            options (CreateArchiveRequest): The options for the archive.

        Returns:
            Archive: The archive object.
        """
        response = self._http_client.post(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/archive',
            options.model_dump(exclude_none=True, by_alias=True),
        )

        return Archive(**response)

    @validate_call
    def get_archive(self, archive_id: str) -> Archive:
        """Gets an archive from the Vonage Video API.

        Args:
            archive_id (str): The archive ID.

        Returns:
            Archive: The archive object.
        """
        response = self._http_client.get(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/archive/{archive_id}',
        )

        return Archive(**response)

    @validate_call
    def delete_archive(self, archive_id: str) -> None:
        """Deletes an archive from the Vonage Video API.

        Args:
            archive_id (str): The archive ID.

        Raises:
            InvalidArchiveStateError: If the archive has a status other than `available`, `uploaded`, or `deleted`.
        """
        try:
            self._http_client.delete(
                self._http_client.video_host,
                f'/v2/project/{self._http_client.auth.application_id}/archive/{archive_id}',
            )
        except HttpRequestError as e:
            if e.response.status_code == 409:
                raise InvalidArchiveStateError(
                    'You can only delete an archive that has one of the following statuses: `available` OR `uploaded` OR `deleted`.'
                )
            raise e

    @validate_call
    def add_stream_to_archive(self, archive_id: str, params: AddStreamRequest) -> None:
        """Adds a stream to an archive in the Vonage Video API. Use this method to change the
        streams included in a composed archive that was started with the streamMode set to "manual".

        Args:
            archive_id (str): The archive ID.
            params (AddStreamRequest): Params for adding a stream to an archive.
        """
        self._http_client.patch(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/archive/{archive_id}/streams',
            params.model_dump(exclude_none=True, by_alias=True),
        )

    @validate_call
    def remove_stream_from_archive(self, archive_id: str, stream_id: str) -> None:
        """Removes a stream from an archive in the Vonage Video API.

        Args:
            archive_id (str): The archive ID.
            stream_id (str): ID of the stream to remove.
        """
        self._http_client.patch(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/archive/{archive_id}/streams',
            params={'removeStream': stream_id},
        )

    @validate_call
    def stop_archive(self, archive_id: str) -> Archive:
        """Stops a Vonage Video API archive.

        Args:
            archive_id (str): The archive ID.

        Returns:
            Archive: The archive object.

        Raises:
            InvalidArchiveStateError: If the archive is not being recorded.
        """
        try:
            response = self._http_client.post(
                self._http_client.video_host,
                f'/v2/project/{self._http_client.auth.application_id}/archive/{archive_id}/stop',
            )
        except HttpRequestError as e:
            if e.response.status_code == 409:
                raise InvalidArchiveStateError(
                    'You can only stop an archive that is being recorded.'
                )
            raise e
        return Archive(**response)

    @validate_call
    def change_archive_layout(self, archive_id: str, layout: ComposedLayout) -> Archive:
        """Changes the layout of an archive in the Vonage Video API.

        Args:
            archive_id (str): The archive ID.
            layout (ComposedLayout): The layout to change to.

        Returns:
            Archive: The archive object.
        """
        response = self._http_client.put(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/archive/{archive_id}/layout',
            layout.model_dump(exclude_none=True, by_alias=True),
        )

        return Archive(**response)
