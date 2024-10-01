from pytest import raises
from vonage_video.errors import (
    IndividualArchivePropertyError,
    LayoutScreenshareTypeError,
    LayoutStylesheetError,
    NoAudioOrVideoError,
)
from vonage_video.models.archive import CreateArchiveRequest, Layout
from vonage_video.models.enums import LayoutType, OutputMode, StreamMode, VideoResolution


def test_create_archive_request_valid():
    request = CreateArchiveRequest(
        session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
        has_audio=True,
        has_video=True,
        layout=Layout(type=LayoutType.BEST_FIT),
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
            layout=Layout(type=LayoutType.BEST_FIT),
        )


def test_layout_custom_without_stylesheet():
    with raises(LayoutStylesheetError):
        Layout(type=LayoutType.CUSTOM)


def test_layout_best_fit_with_stylesheet():
    with raises(LayoutStylesheetError):
        Layout(type=LayoutType.BEST_FIT, stylesheet='http://example.com/stylesheet.css')


def test_layout_screenshare_type_without_best_fit():
    with raises(LayoutScreenshareTypeError):
        Layout(type=LayoutType.PIP, screenshare_type=LayoutType.BEST_FIT)
