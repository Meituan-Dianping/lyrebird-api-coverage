"""
上下文，保存缓存数据
"""
class Context:
    def __init__(self):
        # base url list
        self.base_list = []
        # user tested url list（base包含的）
        self.user_list = []
        # 用户访问的原始url
        self.user_org_list = []
        # 前端需要的list，base数据和user访问数据 merge之后的结果list
        self.merge_list = []
        # 参数校验需要的dict
        self.path_param_dic = {}
        # 优先级级名list
        self.priority_list = []
        # coverage 覆盖率信息
        self.coverage = {}
        # base文件对应的sha1
        self.base_sha1 = ''
        # base文件对应的filename
        self.filename = ''
        # 过滤规则包含host和regular
        self.filter_dic = {}
        # device & APP信息
        self.info = {}
        # 来自base文件的信息
        self.business = ''
        self.version_name = ''
        self.version_code = None
        # user_info
        self.user_info = {}
        # 记录请求最后的时间，避免频繁emit io消息
        self.endtime = 0
        # 时间间隔，每隔指定时间触发1次socket io消息，防止刷新频繁
        self.timer = 1


# 单例模式
app_context = Context()
