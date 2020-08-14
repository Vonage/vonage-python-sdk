import json, re


class Error(Exception):
    pass


class ClientError(Error):
    pass


class ServerError(Error):
    pass


class AuthenticationError(ClientError):
    pass


class NexmoError(ClientError):
    pass


#Code 1: Throttled
class ThrottledError(NexmoError):
    pass


#Code 2: Missing params
class MissingParamError(NexmoError):
    pass


#Code 3: Invalid params
class InvalidParamError(NexmoError):
    pass


#Code 4: Invalid credentials
class CredentialError(NexmoError):
    pass

#Code 5: Internal Error
class InternalError(NexmoError):
    pass


#Code 6: Invalid message
class InvalidMessageError(NexmoError):
    pass


#Code 7: Number barred
class NumberBarredError(NexmoError):
    pass


#Code 8: Partner account barred
class PartnerAccountBarredError(NexmoError):
    pass


#Code 9: Partner quota exceeded
class PartnerQuotaExceededError(NexmoError):
    pass


#Code 11: Account not enabled for REST
class AccountNoRestError(NexmoError):
    pass


#Code 12: Message too long
class MessageLengthError(NexmoError):
    pass


#Code 13: Communication Failed
class CommunicationError(NexmoError):
    pass


#Code 14: Invalid Signature
class InvalidSignatureError(NexmoError):
    pass


#Code 15: Illegal Sender Address - rejected
class IllegalSenderError(NexmoError):
    pass


#Code 16: Invalid TTL
class InvalidTTLError(NexmoError):
    pass


#Code 19: Facility not allowed
class FacilityError(NexmoError):
    pass


#Code 20: Invalid Message class
class InvalidMessageClassError(NexmoError):
    pass


#Code 23: Bad callback :: Missing Protocol
class MissingProtocolError(NexmoError):
    pass


#Code 29: Non White-listed Destination
class BlackListDestinationError(NexmoError):
    pass


#Code 34: Invalid or Missing Msisdn Param
class MsisdnError(NexmoError):
    pass


#Code 400: Bad request - when voice Api
class BadRequestError(NexmoError):
    def __init__(self, data):
        error_data = data
        message = data
        if isinstance(data, bytes):
            #convert data bytes in dict and re-assign
            error_data = json.loads(data.decode('utf-8'))
        if "type" in error_data and "title" in error_data:
            if "detail" in error_data:
                message = "{title}: {detail} ({type})".format(
                        title=error_data["title"], detail=error_data["detail"], type=error_data["type"]
                )
            elif "invalid_parameters" in error_data:
                message = "{title}: Invalid parameters, reason: {reason}, param hint: {name}".format(
                    title=error_data["title"], reason=error_data["invalid_parameters"][0]["reason"], name=error_data["invalid_parameters"][0]["name"]
                )
        super().__init__(message)


class NotFoundError(NexmoError):
    def __init__(self, data):
        error_data = data
        message = data
        is_json = False
        if isinstance(data, bytes):
            #convert data bytes in dict and re-assign
            try:
                error_data = json.loads(data.decode('utf-8'))
                is_json = True
            except:
                error_data = data.decode('utf-8')
                pass
        if is_json:
            if "type" in error_data and "title" in error_data:
                if "detail" in error_data:
                    message = "{title}: {detail} ({type})".format(
                            title=error_data["title"], detail=error_data["detail"], type=error_data["type"]
                    )
        elif re.search("404 Not Found", error_data):
            message = "404: Resource not found"
        super().__init__(message)

class ExceptionHandler():
    #Register exceptions by error code in the private exception matrix
    __exceptions = {
        '1': ThrottledError,
        '2': MissingParamError,
        '3': InvalidParamError,
        '4': CredentialError,
        '5': InternalError,
        '6': InvalidMessageError,
        '7': NumberBarredError,
        '8': PartnerAccountBarredError,
        '9': PartnerQuotaExceededError,
        '11': AccountNoRestError,
        '12': MessageLengthError,
        '13': CommunicationError,
        '14': InvalidSignatureError,
        '15': IllegalSenderError,
        '16': InvalidTTLError,
        '19': FacilityError,
        '20': InvalidMessageClassError,
        '23': MissingProtocolError,
        '29': BlackListDestinationError,
        '34': MsisdnError,
        '400': BadRequestError,
        '404': NotFoundError
    }

    def validate_code(self, code):
        return code in self.__exceptions

    def trigger(self, code, message):
        raise  self.__exceptions[code](message)