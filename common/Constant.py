# 响应成功，状态码200
CODE_SUCCESS = 200
MSG_SUCCESS = '成功'
# token失效或权限认证错误，状态码401
CODE_AUTH_ERROR = 2000
MSG_AUTH_ERROR = 'token认证失败, 请重新登录'
# 业务上的错误
CODE_BUSSINESS_ERROR = 3000
MSG_BUSSINESS_ERROR = '业务出错'
# 服务器内部错误，状态码500
CODE_SERVER_ERROR = 5000
MSG_SERVER_ERROR = '网络操作失败，请稍后重试'
# 未发现接口
CODE_NOT_FOUND_ERROR = 4000
MSG_NOT_FOUND_ERROR = '服务器没有此接口'
# 未知错误
CODE_UNKNOWN_ERROR = 5001
MSG_UNKNOWN_ERROR = '未知错误'
# 拒绝访问
CODE_REJECT_ERROR = 2001
MSG_REJECT_ERROR = '拒绝访问'
# 拒绝访问
CODE_METHOD_ERROR = 2002
MSG_METHOD_ERROR = '请求方法错误'
# 缺少参数
CODE_PARAMETER_ERROR = 4001
MSG_PARAMETER_ERROR = '请求参数异常，请核对后重新输入'
