from vonage import InputTypes


def test_create_dtmf_model():
    dtmf = InputTypes.Dtmf(timeOut=5, maxDigits=2, submitOnHash=True)
    assert type(dtmf) == InputTypes.Dtmf
    assert dtmf.dict() == {'maxDigits': 2, 'submitOnHash': True, 'timeOut': 5}


def test_create_dtmf_model_from_dict():
    dtmf_dict = {'timeOut': 3, 'maxDigits': 4, 'submitOnHash': True}
    dtmf_model = InputTypes.create_dtmf_model(dtmf_dict)
    assert type(dtmf_model) == InputTypes.Dtmf
    assert dtmf_model.dict() == {'maxDigits': 4, 'submitOnHash': True, 'timeOut': 3}


def test_create_speech_model():
    speech = InputTypes.Speech(
        uuid='my-uuid',
        endOnSilence=2.5,
        language='en-GB',
        context=['sales', 'billing'],
        startTimeout=20,
        maxDuration=30,
        saveAudio=True,
    )
    assert type(speech) == InputTypes.Speech
    assert speech.dict() == {
        'uuid': 'my-uuid',
        'endOnSilence': 2.5,
        'language': 'en-GB',
        'context': ['sales', 'billing'],
        'startTimeout': 20,
        'maxDuration': 30,
        'saveAudio': True,
    }


def test_create_speech_model_from_dict():
    speech_dict = {'uuid': 'my-uuid', 'endOnSilence': 2.5, 'maxDuration': 30}
    speech_model = InputTypes.create_speech_model(speech_dict)
    assert type(speech_model) == InputTypes.Speech
    assert speech_model.dict(exclude_none=True) == {
        'uuid': 'my-uuid',
        'endOnSilence': 2.5,
        'maxDuration': 30,
    }
