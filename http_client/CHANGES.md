# 1.5.1
- Remove unnecessary `Content-Type` check on error

# 1.5.0
- Add new `HttpClient.download_file_stream` method
- Add new `FileStreamingError` exception type
- Add backoff exponential timeout increase for HTTP request retries
- Add retries for `RemoteDisconnected` exceptions

# 1.4.3
- Update JWT dependency version

# 1.4.2
- Support for Python 3.13, drop support for 3.8

# 1.4.1
- Add docstrings to data models

# 1.4.0
- Add new `oauth2` logic for calling APIs that require Oauth

# 1.3.1
- Update minimum dependency version

# 1.3.0
- Add new PUT method

# 1.2.1
- Expose classes and errors at the package level

# 1.2.0
- Add `last_request` and `last_response` properties
- Add new `Forbidden` error

# 1.1.1
- Add new Patch method
- New input fields for different ways to pass data in a request

# 1.1.0
- Add support for signature authentication

# 1.0.0
- Initial upload
