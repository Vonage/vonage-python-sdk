from .errors import InvalidRoleError, VideoError

import jwt
from time import time
from uuid import uuid4


class Video:
    auth_type = 'jwt'
    token_roles = {'subscriber', 'publisher', 'moderator'}

    def __init__(self, client):
        self._client = client

    def create_session(self, params=None):
        return self._client.post(
            self._client.video_host(), 
            '/session/create', 
            params, 
            auth_type=Video.auth_type,
            body_is_json=False
        )[0]

    def get_stream(self, session_id, stream_id):
        return self._client.get(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/session/{session_id}/stream/{stream_id}',
            auth_type=Video.auth_type
        )

    def list_streams(self, session_id):
        return self._client.get(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/session/{session_id}/stream',
            auth_type=Video.auth_type
        )

    def set_stream_layout(self, session_id, items):
        return self._client.put(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/session/{session_id}/stream',
            items,
            auth_type=Video.auth_type
        )

    def send_signal(self, session_id, type, data, connection_id=None):
        if connection_id:
            request_uri = f'/v2/project/{self._client.application_id}/session/{session_id}/connection/{connection_id}/signal'
        else:
            request_uri = f'/v2/project/{self._client.application_id}/session/{session_id}/signal'
        
        params = {'type': type, 'data': data}

        return self._client.post(
            self._client.video_host(),
            request_uri,
            params,
            auth_type=Video.auth_type
        )

    def disconnect_client(self, session_id, connection_id):
        return self._client.delete(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/session/{session_id}/connection/{connection_id}',
            auth_type=Video.auth_type
        )

    def mute_stream(self, session_id, stream_id):        
        return self._client.post(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/session/{session_id}/stream/{stream_id}/mute',
            params=None,           
            auth_type=Video.auth_type
        )

    def mute_all_streams(self, session_id, active=True, excluded_stream_ids: list = []):
        params = {'active': active, 'excludedStreamIds': excluded_stream_ids}

        return self._client.post(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/session/{session_id}/mute',
            params,           
            auth_type=Video.auth_type
        )

    def disable_mute_all_streams(self, session_id, excluded_stream_ids=[]):
        self.mute_all_streams(session_id, active=False, excluded_stream_ids=excluded_stream_ids)

    def list_archives(self, filter_params=None, **filter_kwargs):
        return self._client.get(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/archive',
            filter_params or filter_kwargs,           
            auth_type=Video.auth_type
        )

    def create_archive(self, params=None, **kwargs):
        return self._client.post(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/archive',
            params or kwargs,           
            auth_type=Video.auth_type
        )

    def get_archive(self, archive_id):
        return self._client.get(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/archive/{archive_id}',
            auth_type=Video.auth_type
        )

    def delete_archive(self, archive_id):
        return self._client.get(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/archive/{archive_id}',
            auth_type=Video.auth_type
        )

    def add_stream_to_archive(self, archive_id, stream_id, has_audio=True, has_video=True):
        params = {'addStream': stream_id, 'hasAudio': has_audio, 'hasvideo': has_video}

        return self._client.patch(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/archive/{archive_id}/streams',
            params,
            auth_type=Video.auth_type
        )
    
    def remove_stream_from_archive(self, archive_id, stream_id):
        params = {'removeStream': stream_id}

        return self._client.patch(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/archive/{archive_id}/streams',
            params,
            auth_type=Video.auth_type
        )

    def stop_archive(self, archive_id):
        return self._client.post(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/archive/{archive_id}/stop',
            params=None,
            auth_type=Video.auth_type
        )

    def change_archive_layout(self, archive_id, params=None, **kwargs):
        return self._client.put(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/archive/{archive_id}/layout',
            params or kwargs,
            auth_type=Video.auth_type
        )

    def generate_client_token(self, session_id, token_options=None):
        now = int(time())
        claims = {
            'application_id': self._client.application_id,
            'scope': 'session.connect',
            'session_id': session_id,
            'role': 'publisher',
            'initial_layout_class_list': '',
            'jti': str(uuid4()),
            'iat': now
        }

        if hasattr(token_options, 'role'):
            claims['role'] = token_options['role']
        if hasattr(token_options, 'data'):
            claims['data'] = token_options['data']
        if hasattr(token_options, 'initialLayoutClassList'):
            claims['initial_layout_class_list'] = token_options['initialLayoutClassList']
        if hasattr(token_options, 'expireTime') and token_options['expireTime'] > now:
            claims['exp'] = token_options['expireTime']
        if hasattr(token_options, 'jti'):
            claims['jti'] = token_options['jti']
        if hasattr(token_options, 'iat'):
            claims['iat'] = token_options['iat']
        if hasattr(token_options, 'subject'):
            claims['subject'] = token_options['subject']
        if hasattr(token_options, 'acl'):
            claims['acl'] = token_options['acl']

        self.validate_client_token_options(claims)
        headers = {
            'typ': 'JWT',
            'alg': 'RS256'
        }

        return jwt.encode(payload=claims, key=self._client._private_key, algorithm='RS256', headers=headers)
        
    def validate_client_token_options(self, claims):
        now = int(time())
        if claims['role'] not in Video.token_roles:
            raise InvalidRoleError(f'Invalid role specified for the client token. Valid values are: {Video.token_roles}')
        if hasattr(claims, 'exp') and claims['exp'] > now + 3600 * 24 * 30:
            raise VideoError('Token expiry date must be less than 30 days from now.')