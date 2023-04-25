import lyrebird
from lyrebird_api_coverage.client import format_url
from lyrebird_api_coverage.client.context import app_context
import time


class MergeAlgorithm:

    def first_result_handler(self, json_obj):
        """
        初始化/首次/切换base之后 需要重新生成base_list，merge_list
        注意没有初始化coverage
        coverage初始化需要在getCoverage接口实现
        """

        # 清空
        app_context.user_list.clear()
        app_context.base_list.clear()
        app_context.user_org_list.clear()
        # 清空coverage
        app_context.coverage.clear()
        # 清空缓存list
        app_context.merge_list.clear()
        # 清空 参数列表中间处理数据
        app_context.path_param_dic.clear()
        # 初始化base数据，format成需要的数据格式
        self.init_basedata_handler(json_obj)
        # 初始化coverage数据
        self.coverage_arithmetic(json_obj)
        # 获取所有的base URL
        app_context.base_list = list(
            map(lambda x: x.get('url'), json_obj.get('api_list')))

    def init_basedata_handler(self, dic):
        # for k, v in dic.items():
        #     url_dic = {'url': k, 'desc': v.get('desc'), 'priority': v.get('priority'), 'count': 0, 'status': 0,
        #                'org': []}
        #     app_context.merge_list.append(url_dic)
        if not app_context.is_api_base_data:
            dict2 = {'count': 0, 'status': 0, 'id': ''}
            for item in dic.get('api_list'):
                # 处理带参数的情况
                if '?' in item['url']:
                    path = item['url'].split('?')[0].lower()
                    params = item['url'].split('?')[1].split('&')
                    param_dic = {}
                    for i in params:
                        key = i.split('=')[0]
                        val = i.split('=')[1]
                        param_dic[key] = val

                    if app_context.path_param_dic.get(path):
                        app_context.path_param_dic[path].append({'url': item['url'], 'params': param_dic,
                                                                'url_base': format_url.format_api_source(
                                                                    item.get('url')).lower()})
                    else:
                        app_context.path_param_dic[path] = [{'url': item['url'], 'params': param_dic,
                                                            'url_base': format_url.format_api_source(
                                                                item.get('url')).lower()}]
                # format base源 同时变成大小写归一化，变小写
                item['url'] = format_url.format_api_source(
                    item.get('url')).lower()
                item.update(dict2)
                app_context.merge_list.append(item)
        else:
            # 如果接口获取base数据，同步merge_list内容
            app_context.merge_list = dic.get('api_list')

    def merge_handler_new(self, user_url, path_id, category):
        """
        status=0 base中包含未覆盖，status=1 base中包含已覆盖，status=2 base中不包含且覆盖到的;
        path_id表示URL的handler_context的唯一标识，查看详情用
        """

        # 在list中筛选出想要的数据,筛选结果直接取0即可
        specific_filter_list = list(
            filter(lambda x: x.get('url') == user_url, app_context.merge_list))

        # 判断筛选出来的list是否为空,即是否在list中存在
        if specific_filter_list:
            specific_dic = specific_filter_list[0]
            # 移除掉对应的数据为插入index0的位置做前置处理
            app_context.merge_list.remove(specific_dic)
            # 根据数据源,进行业务处理
            if not app_context.is_api_base_data:
                # 非接口获取base数据
                if specific_dic['status'] == 0:
                    specific_dic['status'] = 1
                    # 把首次覆盖到的API,放入user_list里面
                    app_context.user_list.append(user_url)
                # count +1
                # 插入原始url  # specific_dic['org'].append(org_url)
                specific_dic['count'] += 1
                specific_dic['id'] = path_id
            else:
                category_dic = specific_dic.get('category')
                for p in category_dic:
                    if category == p['name'] and p['status'] == 0:
                        p['status'] = 1
                        p['count'] += 1
                        p['id'] = path_id
                        if specific_dic['status'] == 0:
                            specific_dic['status'] = 1
                    elif category == p.get('mpId') and p['status'] == 0:
                        p['status'] = 1
                        p['count'] += 1
                        p['id'] = path_id
                        if specific_dic['status'] == 0:
                            specific_dic['status'] = 1

                # 把首次覆盖到的API,放入user_list里面
                app_context.user_list.append(user_url)
                specific_dic['count'] += 1
                specific_dic['status'] = 1
        else:
            if app_context.is_api_base_data == False:
                # specific_dic = {'url': user_url, 'desc': '', 'priority': '', 'count': 1, 'status': 2, 'org': [org_url]}
                specific_dic = {'url': user_url, 'desc': '',
                                'priority': None, 'count': 1, 'status': 2, 'id': path_id}
            else:
                specific_dic = {'url': user_url, 'desc': '', 'priority': None,
                                'count': 1, 'online': None, 'remark': None, 'status': 2, 'category': []}
                specific_dic.get('category').append(
                    {'id': None, 'name': category, 'status': 2, 'count': 1})
        # 插入到 index=0 的位置
        app_context.merge_list.insert(0, specific_dic)

    def coverage_handler(self):
        """
        总体覆盖率
        """
        # 获取handle前的历史覆盖率为做对比用
        history_coverage = app_context.coverage['total']
        test_len = len(
            list(filter(lambda x: x.get('status') == 1, app_context.merge_list)))
        if app_context.coverage['len'] == 0:
            coverage = 0
        else:
            coverage = round(test_len / app_context.coverage['len'] * 100, 2)
        # 为了传给Overbridge的socket信息format数据格式
        app_context.coverage['total'] = coverage
        # 覆盖率有变化才emit & publish 覆盖率的变化消息给API-Coverage前端，overbridge前端，和消息总线
        if not history_coverage == coverage:
            handler_time = time.time()
            # 限制频繁emit io msg，在两次之间大于指定时间间隔才会emit
            if handler_time - app_context.covtime > app_context.SOCKET_PUSH_INTERVAL:
                lyrebird.emit('coverage message', app_context.coverage.get(
                    'total'), namespace='/api_coverage')
                app_context.covtime = handler_time
            by_priority = [p.get('value')
                           for p in app_context.coverage['priorities']]
            lyrebird.publish('coverage',
                             dict(
                                 name='coverage',
                                 value=app_context.coverage.get('total'),
                                 by_priority=by_priority)
                             )
        app_context.coverage['test_len'] = test_len
        # 各优先级对应覆盖率
        for item_dic in app_context.coverage.get('priorities'):
            item_length = item_dic.get('len')
            test_item_length = len(list(
                filter(lambda x: x.get('priority') == item_dic.get('label') and x.get('status') == 1,
                       app_context.merge_list)))
            if item_length == 0:
                coverage = 0
            else:
                coverage = round(test_item_length / item_length * 100, 2)
            item_dic['value'] = coverage
            item_dic['test_len'] = test_item_length

    def init_resume_data(self, dic):
        app_context.user_list = []
        app_context.base_list = []
        for k, v in dic.items():
            if v['status'] == 1:
                app_context.user_list.append(k)
                app_context.base_list.append(k)
            elif v['status'] == 0:
                app_context.base_list.append(k)

    # 获取优先级初始info，优先级分几个，以及各个优先级的list长度,传入的也是conf文件
    def coverage_arithmetic(self, dic):
        url_info_list = dic.get('api_list')
        # 获取优先级list，非空
        priority_list = list(
            set(list(map(lambda x: x.get('priority'), url_info_list))))
        # 去除空值
        if list(filter(lambda x: x == '', priority_list)):
            priority_list.remove('')
        # 排序
        app_context.priority_list = sorted(priority_list)
        # init coverage 原始数据结构 total总体数据
        app_context.coverage['name'] = 'coverage'
        app_context.coverage['total'] = 0
        app_context.coverage['len'] = len(url_info_list)
        app_context.coverage['test_len'] = 0
        app_context.coverage['priorities'] = []
        # 各个优先级的init数据
        for item in app_context.priority_list:
            item_length = len(
                list(filter(lambda x: x.get('priority') == item, url_info_list)))
            coverage = 0
            app_context.coverage['priorities'].append(
                {'label': item, 'value': coverage, 'len': item_length, 'test_len': 0})

    # 对import的打算resume的result和 缓存里面的测试结果进行merge
    def merge_resume(self, result_list):
        # 在list中筛选出url,筛选结果直接取0即可
        cache_list = app_context.merge_list
        # 取出url信息，组成list
        cache_url_list = list(map(lambda x: x.get('url'), cache_list))
        result_url_list = list(map(lambda x: x.get('url'), result_list))
        # 找到交集
        intersection_list = list(
            set(cache_url_list).intersection(set(result_url_list)))
        # 对交集进行处理
        for url in intersection_list:
            cache_spec = list(
                filter(lambda x: x.get('url') == url, cache_list))[0]
            result_spec = list(
                filter(lambda x: x.get('url') == url, result_list))[0]
            spec_dict = list(filter(lambda x: x.get('url') ==
                             url, app_context.merge_list))[0]
            app_context.merge_list.remove(spec_dict)
            # 修改count status org_url
            spec_dict['count'] = cache_spec.get(
                'count') + result_spec.get('count')
            if spec_dict['status'] == 0 and spec_dict['count'] != 0:
                spec_dict['status'] = 1
            app_context.merge_list.insert(0, spec_dict)
        # 找到差集
        diff_url_list = list(set(result_url_list) - set(cache_url_list))
        # 差集处理（对result中存在，但cache不存在的）status=2的情景进行extend处理
        diff_list = list(filter(lambda x: True if x.get(
            'url') in diff_url_list else False, result_list))
        app_context.merge_list.extend(diff_list)
        # 重新计算覆盖率
        self.coverage_handler()


mergeAlgorithm = MergeAlgorithm()
