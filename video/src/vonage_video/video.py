from typing import Optional, Type, Union

from pydantic import validate_call
from vonage_http_client.errors import HttpRequestError
from vonage_http_client.http_client import HttpClient
from vonage_utils.types import Dtmf
from vonage_video.errors import (
    InvalidArchiveStateError,
    InvalidBroadcastStateError,
    RoutedSessionRequiredError,
    VideoError,
)
from vonage_video.models.archive import (
    Archive,
    ComposedLayout,
    CreateArchiveRequest,
    ListArchivesFilter,
)
from vonage_video.models.audio_connector import AudioConnectorData, AudioConnectorOptions
from vonage_video.models.broadcast import (
    Broadcast,
    CreateBroadcastRequest,
    ListBroadcastsFilter,
)
from vonage_video.models.captions import CaptionsData, CaptionsOptions
from vonage_video.models.common import AddStreamRequest
from vonage_video.models.experience_composer import (
    ExperienceComposer,
    ExperienceComposerOptions,
    ListExperienceComposersFilter,
)
from vonage_video.models.session import SessionOptions, VideoSession
from vonage_video.models.signal import SignalData
from vonage_video.models.sip import InitiateSipRequest, SipCall
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
    def list_streams(self, session_id: str) -> list[StreamInfo]:
        """Lists the streams in a session from the Vonage Video API.

        Args:
            session_id (str): The session ID.

        Returns:
            list[StreamInfo]: Information about the video streams.
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
    ) -> list[StreamInfo]:
        """Changes the layout of a stream in a session in the Vonage Video API.

        Args:
            session_id (str): The session ID.
            stream_layout_options (StreamLayoutOptions): The options for the stream layout.

        Returns:
            list[StreamInfo]: Information about the video streams.
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
        """Sends a signal to a session in the Vonage Video API. If `connection_id` is not
        provided, the signal will be sent to all connections in the session.

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
        self, session_id: str, excluded_stream_ids: list[str] = None
    ) -> None:
        """Mutes all streams in a session using the Vonage Video API.

        Args:
            session_id (str): The session ID.
            excluded_stream_ids (list[str], Optional): The stream IDs to exclude from muting.
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
        """Starts an audio connector in a session using the Vonage Video API. Connects
        audio streams to a specified WebSocket URI.

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
    ) -> tuple[list[ExperienceComposer], int, Optional[int]]:
        """Lists Experience Composers associated with your Vonage application.

        Args:
            filter (ListExperienceComposersFilter, Optional): Filter for the Experience Composers.

        Returns:
            tuple[list[ExperienceComposer], int, Optional[int]]: A tuple containing a list of experience
                composer objects, the total count of Experience Composers and the required offset value
                for the next page, if applicable.
                i.e.
                experience_composers: list[ExperienceComposer], count: int, next_page_offset: Optional[int]
        """
        response = self._http_client.get(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/render',
            filter.model_dump(exclude_none=True, by_alias=True),
        )

        return self._list_video_objects(filter, response, ExperienceComposer)

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
        self, filter: ListArchivesFilter = ListArchivesFilter()
    ) -> tuple[list[Archive], int, Optional[int]]:
        """Lists archives associated with a Vonage Application.

        Args:
            filter (ListArchivesFilter, Optional): The filters for the archives.

        Returns:
            tuple[list[Archive], int, Optional[int]]: A tuple containing a list of archive objects,
                the total count of archives and the required offset value for the next page, if applicable.
                i.e.
                archives: list[Archive], count: int, next_page_offset: Optional[int]
        """
        response = self._http_client.get(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/archive',
            filter.model_dump(exclude_none=True, by_alias=True),
        )

        return self._list_video_objects(filter, response, Archive)

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
            conflict_error_message = 'You can only delete an archive that has one of the following statuses: `available` OR `uploaded` OR `deleted`.'
            self._check_conflict_error(
                e, InvalidArchiveStateError, conflict_error_message
            )

    @validate_call
    def add_stream_to_archive(self, archive_id: str, params: AddStreamRequest) -> None:
        """Adds a stream to an archive in the Vonage Video API. Use this method to change
        the streams included in a composed archive that was started with the streamMode
        set to "manual".

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
            conflict_error_message = (
                'You can only stop an archive that is being recorded.'
            )
            self._check_conflict_error(
                e, InvalidArchiveStateError, conflict_error_message
            )
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

    @validate_call
    def list_broadcasts(
        self, filter: ListBroadcastsFilter = ListBroadcastsFilter()
    ) -> tuple[list[Broadcast], int, Optional[int]]:
        """Lists broadcasts associated with a Vonage Application.

        Args:
            filter (ListBroadcastsFilter, Optional): The filters for the broadcasts.

        Returns:
            tuple[list[Broadcast], int, Optional[int]]: A tuple containing a list of broadcast objects,
                the total count of broadcasts and the required offset value for the next page, if applicable.
                i.e.
                broadcasts: list[Broadcast], count: int, next_page_offset: Optional[int]
        #
        """
        response = self._http_client.get(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/broadcast',
            filter.model_dump(exclude_none=True, by_alias=True),
        )

        return self._list_video_objects(filter, response, Broadcast)

    @validate_call
    def start_broadcast(self, options: CreateBroadcastRequest) -> Broadcast:
        """Starts a broadcast in a Vonage Video API session.

        Args:
            options (CreateBroadcastRequest): The options for the broadcast.

        Returns:
            Broadcast: The broadcast object.

        Raises:
            InvalidBroadcastStateError: If the broadcast has already started for the session,
                or if you attempt to start a simultaneous broadcast for a session without setting
                a unique `multi-broadcast-tag` value.
        """
        try:
            response = self._http_client.post(
                self._http_client.video_host,
                f'/v2/project/{self._http_client.auth.application_id}/broadcast',
                options.model_dump(exclude_none=True, by_alias=True),
            )
        except HttpRequestError as e:
            conflict_error_message = (
                'Either the broadcast has already started for the session, '
                'or you attempted to start a simultaneous broadcast for a session '
                'without setting a unique `multi-broadcast-tag` value.'
            )
            self._check_conflict_error(
                e, InvalidBroadcastStateError, conflict_error_message
            )

        return Broadcast(**response)

    @validate_call
    def get_broadcast(self, broadcast_id: str) -> Broadcast:
        """Gets a broadcast from the Vonage Video API.

        Args:
            broadcast_id (str): The broadcast ID.

        Returns:
            Broadcast: The broadcast object.
        """
        response = self._http_client.get(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/broadcast/{broadcast_id}',
        )

        return Broadcast(**response)

    @validate_call
    def stop_broadcast(self, broadcast_id: str) -> Broadcast:
        """Stops a Vonage Video API broadcast.

        Args:
            broadcast_id (str): The broadcast ID.

        Returns:
            Broadcast: The broadcast object.
        """
        response = self._http_client.post(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/broadcast/{broadcast_id}/stop',
        )
        return Broadcast(**response)

    @validate_call
    def change_broadcast_layout(
        self, broadcast_id: str, layout: ComposedLayout
    ) -> Broadcast:
        """Changes the layout of a broadcast in the Vonage Video API.

        Args:
            broadcast_id (str): The broadcast ID.
            layout (ComposedLayout): The layout to change to.

        Returns:
            Broadcast: The broadcast object.
        """
        response = self._http_client.put(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/broadcast/{broadcast_id}/layout',
            layout.model_dump(exclude_none=True, by_alias=True),
        )

        return Broadcast(**response)

    @validate_call
    def add_stream_to_broadcast(
        self, broadcast_id: str, params: AddStreamRequest
    ) -> None:
        """Adds a stream to a broadcast in the Vonage Video API. Use this method to change
        the streams included in a composed broadcast that was started with the streamMode
        set to "manual".

        Args:
            broadcast_id (str): The broadcast ID.
            params (AddStreamRequest): The video stream to add to the broadcast.
        """
        self._http_client.patch(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/broadcast/{broadcast_id}/streams',
            params.model_dump(exclude_none=True, by_alias=True),
        )

    @validate_call
    def remove_stream_from_broadcast(self, broadcast_id: str, stream_id: str) -> None:
        """Removes a stream from a broadcast in the Vonage Video API.

        Args:
            broadcast_id (str): The broadcast ID.
            stream_id (str): ID of the stream to remove.
        """
        self._http_client.patch(
            self._http_client.video_host,
            f'/v2/project/{self._http_client.auth.application_id}/broadcast/{broadcast_id}/streams',
            params={'removeStream': stream_id},
        )

    @validate_call
    def initiate_sip_call(self, sip_request_params: InitiateSipRequest) -> SipCall:
        """Initiates a SIP call using the Vonage Video API.

        Args:
            sip_request_params (SipParams): Model containing the session ID and a valid token,
                as well as options for the SIP call.

        Returns:
            SipCall: The SIP call object.
        """
        try:
            response = self._http_client.post(
                self._http_client.video_host,
                f'/v2/project/{self._http_client.auth.application_id}/dial',
                sip_request_params.model_dump(exclude_none=True, by_alias=True),
            )
        except HttpRequestError as e:
            conflict_error_message = 'SIP calling can only be used in a session with'
            ' `media_mode=routed`.'
            self._check_conflict_error(
                e, RoutedSessionRequiredError, conflict_error_message
            )

        return SipCall(**response)

    @validate_call
    def play_dtmf(self, session_id: str, digits: Dtmf, connection_id: str = None) -> None:
        """Plays DTMF tones into one or all SIP connections in a session using the Vonage
        Video API.

        Args:
            session_id (str): The session ID.
            digits (Dtmf): The DTMF digits to play. Numbers `0-9`, `*`, `#` and `p`
                (500ms pause) are supported.
            connection_id (str, Optional): The connection ID to send the DTMF tones to.
                If not provided, the DTMF tones will be played on all connections in
                the session.
        """
        if connection_id is not None:
            url = f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/connection/{connection_id}/play-dtmf'
        else:
            url = f'/v2/project/{self._http_client.auth.application_id}/session/{session_id}/play-dtmf'

        self._http_client.post(self._http_client.video_host, url, {'digits': digits})

    @validate_call
    def _list_video_objects(
        self,
        request_filter: Union[
            ListArchivesFilter, ListBroadcastsFilter, ListExperienceComposersFilter
        ],
        response: dict,
        model: Union[Type[Archive], Type[Broadcast], Type[ExperienceComposer]],
    ) -> tuple[list[object], int, Optional[int]]:
        """List objects of a specific model from a response.

        Args:
            request_filter (Union[ListArchivesFilter, ListBroadcastsFilter, ListExperienceComposersFilter]):
                The filter used to make the request.
            response (dict): The response from the API.
            model (Union[Type[Archive], Type[Broadcast], Type[ExperienceComposer]]): The type of a pydantic
                model to populate the response into.

        Returns:
            tuple[list[object], int, Optional[int]]: A tuple containing a list of objects,
                the total count of objects and the required offset value for the next page, if applicable.
                i.e.
                objects: list[object], count: int, next_page_offset: Optional[int]
        """
        index = request_filter.offset + 1 or 1
        page_size = request_filter.page_size
        objects = []

        try:
            for obj in response['items']:
                objects.append(model(**obj))
        except KeyError:
            return [], 0, None

        count = response['count']
        if count > page_size * index:
            return objects, count, index
        return objects, count, None

    def _check_conflict_error(
        self,
        http_error: HttpRequestError,
        ConflictError: Type[VideoError],
        conflict_error_message: str,
    ) -> None:
        """Checks if the error is a conflict error and raises the specified error.

        Args:
            http_error (HttpRequestError): The error to check.
            ConflictError (Type[VideoError]): The error to raise if there is a conflict.
            conflict_error_message (str): The error message if there is a conflict.
        """
        if http_error.response.status_code == 409:
            raise ConflictError(f'{conflict_error_message} {http_error.response.text}')
        raise http_error
