from os.path import abspath

import responses
from pytest import raises
from vonage_http_client import HttpClient
from vonage_video import (
    AddStreamRequest,
    ComposedLayout,
    CreateArchiveRequest,
    LayoutType,
    ListArchivesFilter,
    OutputMode,
    StreamMode,
    Video,
    VideoResolution,
)
from vonage_video.errors import (
    IndividualArchivePropertyError,
    InvalidArchiveStateError,
    LayoutScreenshareTypeError,
    LayoutStylesheetError,
    NoAudioOrVideoError,
)
from vonage_video.models.archive import Transcription

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)

video = Video(HttpClient(get_mock_jwt_auth()))


def test_create_archive_request_valid():
    request = CreateArchiveRequest(
        session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
        has_audio=True,
        has_video=True,
        layout=ComposedLayout(type=LayoutType.BEST_FIT),
        multi_archive_tag='test_multi_archive_tag',
        output_mode=OutputMode.COMPOSED,
        resolution=VideoResolution.RES_1280x720,
        stream_mode=StreamMode.AUTO,
    )
    assert request.session_id == "1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5"
    assert request.has_audio is True
    assert request.has_video is True
    assert request.layout.type == LayoutType.BEST_FIT
    assert request.multi_archive_tag == 'test_multi_archive_tag'
    assert request.output_mode == OutputMode.COMPOSED
    assert request.resolution == VideoResolution.RES_1280x720
    assert request.stream_mode == StreamMode.AUTO


def test_create_archive_request_no_audio_or_video():
    with raises(NoAudioOrVideoError) as e:
        CreateArchiveRequest(
            session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
            has_audio=False,
            has_video=False,
        )


def test_create_archive_request_individual_output_mode_with_resolution():
    with raises(IndividualArchivePropertyError):
        CreateArchiveRequest(
            session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
            has_audio=True,
            output_mode=OutputMode.INDIVIDUAL,
            resolution=VideoResolution.RES_720x1280,
        )


def test_create_archive_request_individual_output_mode_with_layout():
    with raises(IndividualArchivePropertyError):
        CreateArchiveRequest(
            session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
            has_audio=True,
            output_mode=OutputMode.INDIVIDUAL,
            layout=ComposedLayout(type=LayoutType.BEST_FIT),
        )


def test_create_archive_request_composed_output_mode_with_transcription_error():
    with raises(IndividualArchivePropertyError):
        CreateArchiveRequest(
            session_id='test_session_id',
            has_audio=True,
            output_mode=OutputMode.COMPOSED,
            has_transcription=True,
        )


def test_create_archive_request_valid_quantization_parameter():
    """Test that quantization_parameter is accepted for composed archives with valid
    values."""
    request = CreateArchiveRequest(
        session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
        has_audio=True,
        has_video=True,
        output_mode=OutputMode.COMPOSED,
        quantization_parameter=25,
    )
    assert request.quantization_parameter == 25


def test_create_archive_request_quantization_parameter_boundary_values():
    """Test that quantization_parameter accepts boundary values (15 and 40)."""
    # Test minimum value
    request_min = CreateArchiveRequest(
        session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
        has_audio=True,
        quantization_parameter=15,
    )
    assert request_min.quantization_parameter == 15

    # Test maximum value
    request_max = CreateArchiveRequest(
        session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
        has_audio=True,
        quantization_parameter=40,
    )
    assert request_max.quantization_parameter == 40


def test_create_archive_request_quantization_parameter_invalid_low():
    """Test that quantization_parameter rejects values below 15."""
    with raises(ValueError):
        CreateArchiveRequest(
            session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
            has_audio=True,
            quantization_parameter=14,
        )


def test_create_archive_request_quantization_parameter_invalid_high():
    """Test that quantization_parameter rejects values above 40."""
    with raises(ValueError):
        CreateArchiveRequest(
            session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
            has_audio=True,
            quantization_parameter=41,
        )


def test_create_archive_request_individual_output_mode_with_quantization_parameter():
    """Test that quantization_parameter is rejected for individual archives."""
    with raises(IndividualArchivePropertyError):
        CreateArchiveRequest(
            session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
            has_audio=True,
            output_mode=OutputMode.INDIVIDUAL,
            quantization_parameter=25,
        )


def test_create_archive_request_serialization_with_quantization_parameter():
    """Test that quantization_parameter is properly serialized with the correct alias."""
    request = CreateArchiveRequest(
        session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
        has_audio=True,
        has_video=True,
        output_mode=OutputMode.COMPOSED,
        quantization_parameter=30,
    )

    serialized = request.model_dump(by_alias=True, exclude_unset=True)
    assert 'quantizationParameter' in serialized
    assert serialized['quantizationParameter'] == 30
    assert (
        'quantization_parameter' not in serialized
    )  # Ensure Python field name is not used


def test_layout_custom_without_stylesheet():
    with raises(LayoutStylesheetError):
        ComposedLayout(type=LayoutType.CUSTOM)


def test_layout_best_fit_with_stylesheet():
    with raises(LayoutStylesheetError):
        ComposedLayout(
            type=LayoutType.BEST_FIT, stylesheet='http://example.com/stylesheet.css'
        )


def test_layout_screenshare_type_without_best_fit():
    with raises(LayoutScreenshareTypeError):
        ComposedLayout(type=LayoutType.PIP, screenshare_type=LayoutType.BEST_FIT)


@responses.activate
def test_list_archives():
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/archive',
        'list_archives.json',
    )

    filter = ListArchivesFilter(offset=0, page_size=10, session_id='test_session_id')
    archives, count, next_page = video.list_archives(filter)

    assert count == 2
    assert next_page is None
    assert archives[0].id == '5b1521e6-115f-4efd-bed9-e527b87f0699'
    assert archives[0].status == 'paused'
    assert archives[0].resolution == '1280x720'
    assert archives[0].session_id == 'test_session_id'
    assert archives[1].id == 'a9cdeb69-f6cf-408b-9197-6f99e6eac5aa'
    assert archives[1].status == 'available'
    assert archives[1].reason == 'session ended'
    assert archives[1].duration == 134
    assert archives[1].sha256_sum == 'test_sha256_sum'
    assert archives[1].url == 'https://example.com/archive.mp4'
    assert archives[1].max_bitrate == 2_000_000

    @responses.activate
    def test_list_archives_no_parameters():
        build_response(
            path,
            'GET',
            'https://video.api.vonage.com/v2/project/test_application_id/archive',
            'list_archives.json',
        )

        filter = ListArchivesFilter(session_id='test_session_id')
        archives, count, next_page = video.list_archives(filter)

        assert count == 2
        assert next_page is None
        assert archives[0].id == '5b1521e6-115f-4efd-bed9-e527b87f0699'
        assert archives[0].status == 'paused'
        assert archives[0].resolution == '1280x720'
        assert archives[0].session_id == 'test_session_id'
        assert archives[1].id == 'a9cdeb69-f6cf-408b-9197-6f99e6eac5aa'
        assert archives[1].status == 'available'
        assert archives[1].reason == 'session ended'
        assert archives[1].duration == 134
        assert archives[1].sha256_sum == 'test_sha256_sum'
        assert archives[1].url == 'https://example.com/archive.mp4'
        assert archives[1].max_bitrate == 2_000_000


@responses.activate
def test_start_archive():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/archive',
        'archive.json',
    )

    archive_options = CreateArchiveRequest(
        session_id='test_session_id',
        has_audio=True,
        has_video=True,
        layout=ComposedLayout(
            type=LayoutType.BEST_FIT, screenshare_type=LayoutType.HORIZONTAL_PRESENTATION
        ),
        multi_archive_tag='my-multi-archive',
        name='first archive test',
        output_mode=OutputMode.COMPOSED,
        resolution=VideoResolution.RES_1280x720,
        stream_mode=StreamMode.MANUAL,
        max_bitrate=2_000_000,
    )

    archive = video.start_archive(archive_options)

    assert archive.id == '5b1521e6-115f-4efd-bed9-e527b87f0699'
    assert archive.session_id == 'test_session_id'
    assert archive.application_id == 'test_application_id'
    assert archive.created_at == 1727870434974
    assert archive.updated_at == 1727870434977
    assert archive.status == 'started'
    assert archive.name == 'first archive test'
    assert archive.resolution == '1280x720'
    assert archive.max_bitrate == 2_000_000
    assert archive.quantization_parameter == 25


@responses.activate
def test_get_archive():
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/archive/5b1521e6-115f-4efd-bed9-e527b87f0699',
        'archive.json',
    )

    archive = video.get_archive('5b1521e6-115f-4efd-bed9-e527b87f0699')

    assert archive.id == '5b1521e6-115f-4efd-bed9-e527b87f0699'
    assert archive.session_id == 'test_session_id'
    assert archive.application_id == 'test_application_id'
    assert archive.created_at == 1727870434974
    assert archive.updated_at == 1727870434977
    assert archive.status == 'started'
    assert archive.name == 'first archive test'
    assert archive.resolution == '1280x720'
    assert archive.quantization_parameter == 25


@responses.activate
def test_delete_archive():
    build_response(
        path,
        'DELETE',
        'https://video.api.vonage.com/v2/project/test_application_id/archive/5b1521e6-115f-4efd-bed9-e527b87f0699',
        status_code=204,
    )

    video.delete_archive('5b1521e6-115f-4efd-bed9-e527b87f0699')

    assert video.http_client.last_response.status_code == 204


@responses.activate
def test_delete_archive_error_invalid_status():
    build_response(
        path,
        'DELETE',
        'https://video.api.vonage.com/v2/project/test_application_id/archive/5b1521e6-115f-4efd-bed9-e527b87f0699',
        'delete_archive_error.json',
        status_code=409,
    )

    with raises(InvalidArchiveStateError) as e:
        video.delete_archive('5b1521e6-115f-4efd-bed9-e527b87f0699')

    assert '"code": 15004' in str(e.value)


@responses.activate
def test_add_stream_to_archive():
    build_response(
        path,
        'PATCH',
        'https://video.api.vonage.com/v2/project/test_application_id/archive/test_archive_id/streams',
        status_code=204,
    )

    params = AddStreamRequest(
        stream_id='47ce017c-28aa-40d0-b094-2e5dc437746c', has_audio=True, has_video=True
    )
    video.add_stream_to_archive(archive_id='test_archive_id', params=params)

    assert video.http_client.last_response.status_code == 204


@responses.activate
def test_remove_stream_from_archive():
    build_response(
        path,
        'PATCH',
        'https://video.api.vonage.com/v2/project/test_application_id/archive/test_archive_id/streams',
        status_code=204,
    )

    video.remove_stream_from_archive(
        archive_id='test_archive_id', stream_id='47ce017c-28aa-40d0-b094-2e5dc437746c'
    )

    assert video.http_client.last_response.status_code == 204


@responses.activate
def test_stop_archive():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/archive/e05d6f8f-2280-4025-b1d2-defc4f5c8dfa/stop',
        'stop_archive.json',
    )

    archive = video.stop_archive('e05d6f8f-2280-4025-b1d2-defc4f5c8dfa')

    assert archive.id == 'e05d6f8f-2280-4025-b1d2-defc4f5c8dfa'
    assert archive.status == 'stopped'
    assert archive.reason == 'user initiated'


@responses.activate
def test_stop_archive_invalid_state_error():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/archive/e05d6f8f-2280-4025-b1d2-defc4f5c8dfa/stop',
        'stop_archive_error.json',
        status_code=409,
    )

    with raises(InvalidArchiveStateError) as e:
        video.stop_archive('e05d6f8f-2280-4025-b1d2-defc4f5c8dfa')

    assert '"code": 15002' in str(e.value)


@responses.activate
def test_change_archive_layout():
    build_response(
        path,
        'PUT',
        'https://video.api.vonage.com/v2/project/test_application_id/archive/5b1521e6-115f-4efd-bed9-e527b87f0699/layout',
        'archive.json',
    )

    layout = ComposedLayout(type=LayoutType.BEST_FIT, screenshare_type=LayoutType.PIP)
    archive = video.change_archive_layout('5b1521e6-115f-4efd-bed9-e527b87f0699', layout)

    assert archive.id == '5b1521e6-115f-4efd-bed9-e527b87f0699'
    assert video.http_client.last_response.status_code == 200


# Tests for new Transcription options
def test_transcription_model_with_all_options():
    """Test that the Transcription model can be created with all new options."""
    transcription = Transcription(
        status="completed",
        reason="transcription completed successfully",
        url="https://example.com/transcription.json",
        primaryLanguageCode="en-US",
        hasSummary=True,
    )

    assert transcription.status == "completed"
    assert transcription.reason == "transcription completed successfully"
    assert transcription.url == "https://example.com/transcription.json"
    assert transcription.primaryLanguageCode == "en-US"
    assert transcription.hasSummary is True


def test_transcription_model_with_partial_options():
    """Test that the Transcription model can be created with only some new options."""
    transcription = Transcription(
        status="processing", url="https://example.com/transcription.json"
    )

    assert transcription.status == "processing"
    assert transcription.url == "https://example.com/transcription.json"
    assert transcription.primaryLanguageCode is None
    assert transcription.hasSummary is None
    assert transcription.reason is None


def test_transcription_model_with_url_only():
    """Test that the Transcription model can be created with just the url option."""
    transcription = Transcription(url="https://example.com/transcription.json")

    assert transcription.url == "https://example.com/transcription.json"
    assert transcription.status is None
    assert transcription.reason is None
    assert transcription.primaryLanguageCode is None
    assert transcription.hasSummary is None


def test_transcription_model_with_primary_language_code_only():
    """Test that the Transcription model can be created with just the primaryLanguageCode
    option."""
    transcription = Transcription(primaryLanguageCode="es-ES")

    assert transcription.primaryLanguageCode == "es-ES"
    assert transcription.status is None
    assert transcription.reason is None
    assert transcription.url is None
    assert transcription.hasSummary is None


def test_transcription_model_with_has_summary_only():
    """Test that the Transcription model can be created with just the hasSummary
    option."""
    transcription = Transcription(hasSummary=False)

    assert transcription.hasSummary is False
    assert transcription.status is None
    assert transcription.reason is None
    assert transcription.url is None
    assert transcription.primaryLanguageCode is None


def test_transcription_model_empty():
    """Test that the Transcription model can be created with no options set."""
    transcription = Transcription()

    assert transcription.status is None
    assert transcription.reason is None
    assert transcription.url is None
    assert transcription.primaryLanguageCode is None
    assert transcription.hasSummary is None


def test_transcription_model_serialization():
    """Test that the Transcription model serializes correctly."""
    transcription = Transcription(
        status="completed",
        reason="success",
        url="https://example.com/transcription.json",
        primaryLanguageCode="en-US",
        hasSummary=True,
    )

    serialized = transcription.model_dump()
    expected = {
        "status": "completed",
        "reason": "success",
        "url": "https://example.com/transcription.json",
        "primaryLanguageCode": "en-US",
        "hasSummary": True,
    }

    assert serialized == expected


def test_transcription_model_serialization_exclude_unset():
    """Test that the Transcription model serializes correctly excluding unset values."""
    transcription = Transcription(
        url="https://example.com/transcription.json", hasSummary=True
    )

    serialized = transcription.model_dump(exclude_unset=True)
    expected = {"url": "https://example.com/transcription.json", "hasSummary": True}

    assert serialized == expected
    assert "status" not in serialized
    assert "reason" not in serialized
    assert "primaryLanguageCode" not in serialized


def test_transcription_model_deserialization():
    """Test that the Transcription model can be created from dictionary data."""
    data = {
        "status": "completed",
        "reason": "transcription finished",
        "url": "https://example.com/transcription.json",
        "primaryLanguageCode": "fr-FR",
        "hasSummary": True,
    }

    transcription = Transcription(**data)

    assert transcription.status == "completed"
    assert transcription.reason == "transcription finished"
    assert transcription.url == "https://example.com/transcription.json"
    assert transcription.primaryLanguageCode == "fr-FR"
    assert transcription.hasSummary is True


def test_transcription_model_with_various_language_codes():
    """Test that the Transcription model accepts various language codes."""
    test_cases = ["en-US", "es-ES", "fr-FR", "de-DE", "ja-JP", "zh-CN", "pt-BR"]

    for lang_code in test_cases:
        transcription = Transcription(primaryLanguageCode=lang_code)
        assert transcription.primaryLanguageCode == lang_code


def test_transcription_model_with_various_urls():
    """Test that the Transcription model accepts various URL formats."""
    test_urls = [
        "https://example.com/transcription.json",
        "https://storage.googleapis.com/bucket/file.json",
        "https://s3.amazonaws.com/bucket/transcription.txt",
        "http://example.org/path/to/transcription",
        "https://vonage.example.com/transcriptions/12345",
    ]

    for url in test_urls:
        transcription = Transcription(url=url)
        assert transcription.url == url


def test_transcription_model_boolean_has_summary():
    """Test that hasSummary properly handles boolean values."""
    # Test True
    transcription_true = Transcription(hasSummary=True)
    assert transcription_true.hasSummary is True

    # Test False
    transcription_false = Transcription(hasSummary=False)
    assert transcription_false.hasSummary is False

    # Test None (default)
    transcription_none = Transcription()
    assert transcription_none.hasSummary is None


@responses.activate
def test_archive_with_transcription_options():
    """Test that Archive model properly deserializes with transcription containing new
    options."""
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/archive/5b1521e6-115f-4efd-bed9-e527b87f0699',
        'archive_with_transcription.json',
    )

    archive = video.get_archive('5b1521e6-115f-4efd-bed9-e527b87f0699')

    assert archive.id == '5b1521e6-115f-4efd-bed9-e527b87f0699'
    assert archive.has_transcription is True

    # Test transcription object and its new properties
    assert archive.transcription is not None
    assert archive.transcription.status == "completed"
    assert archive.transcription.reason == "transcription completed successfully"
    assert archive.transcription.url == "https://example.com/transcription.json"
    assert archive.transcription.primaryLanguageCode == "en-US"
    assert archive.transcription.hasSummary is True


@responses.activate
def test_list_archives_with_transcription_options():
    """Test that listing archives properly handles transcription with new options."""
    # Create a modified list response that includes transcription data
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/archive',
        'list_archives_with_transcription.json',
    )

    filter = ListArchivesFilter(session_id='test_session_id')
    archives, count, next_page = video.list_archives(filter)

    # Find the archive with transcription
    transcribed_archive = None
    for archive in archives:
        if archive.has_transcription:
            transcribed_archive = archive
            break

    assert transcribed_archive is not None
    assert transcribed_archive.transcription is not None
    assert transcribed_archive.transcription.url is not None
    assert transcribed_archive.transcription.primaryLanguageCode is not None
    assert transcribed_archive.transcription.hasSummary is not None
