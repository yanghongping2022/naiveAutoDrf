from rest_framework.response import Response
import six
from common.Constant import CODE_SUCCESS, MSG_SUCCESS
from rest_framework import status


class BaseResponse(Response):
    """
    对response返回的内容做统一处理
    """
    def __init__(self, code=CODE_SUCCESS, message=MSG_SUCCESS, data=None, status=status.HTTP_200_OK,
                 template_name=None, headers=None, exception=False, content_type='application/json'):
        super(Response, self).__init__(None, status=status)
        if data is None:
            data = {}
        self._code = code
        self._message = message
        self._data = data

        self.data = {"code": code, "message": message, "data": data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
