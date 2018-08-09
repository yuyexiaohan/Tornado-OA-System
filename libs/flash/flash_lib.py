#coding=utf-8

# 消息弹框处理功能

def flash(self, message, category='message'):
    """先调用flash"""
    flashes = self.session.get('_flashes', []) # 将flashes赋值一个列表
    #列表内部结构： [('error', '保存失败'),('ok', '分类保存了')]
    flashes.append((category, message))
    self.session.set('_flashes', flashes) # 将flashes存入session中


def get_flashed_messages(self, with_categories=False, category_filter=[]):
    """后调用get_flashed_messages
     {% for category, message in get_flashed_messages(with_categories=True) %}
     {% if category == 'error' %}

    """
    flashes = self.flashes
    # 根据最开始对flashes赋值，在BaseHandler中定义self.flashes = None
    if flashes is None:
        # 按照self.flashes= flashes = xxx中，将数据不仅存在了flashes中，
        # 也存在了self.flashes中(self.flashes时在BaseHandler中的)，这样在后面 del 删除session中的flashes时，
        # 还可以通过self.flashes获取该值。
        # 这里函数'get_flashed_messages()'是在在执行中被调用了两次，这样就可以保证
        self.flashes = flashes = self.session.get('_flashes', [])
        del self.session['_flashes']
    if category_filter:
        flashes = list(filter(lambda f: f[0] in category_filter, flashes))
    if not with_categories:
        return [x[1] for x in flashes]
    return flashes #[('error', '保存失败')]


#html页面代码与flask相同
#普通闪现
# {% for message in get_flashed_messages() %}
#     <p style="background-color: #bce8f1">{{ message }}</p>
# {% end %}
#
# 分类闪现
# {% for  category, message in get_flashed_messages(with_categories=True) %}
#     {% if category == 'error' %}
#         <p style="background-color: red">{{ message }}</p>
#     {% elif category == 'success'%}
#         <p style="background-color: green">{{ message }}</p>
#     {% end %}
# {% end %}

#过滤闪现
# <!--  过滤闪现 -->
#        {% for  message in get_flashed_messages(category_filter=["error"]) %}
#            <p style="background-color: red">{{ message }}</p>
#        {% end %}
#
#        {% for  message in get_flashed_messages(category_filter=["success"]) %}
#            <p style="background-color: #bce8f1">{{ message }}</p>
#        {% end %}

#弹窗
# { %
# for category, message in get_flashed_messages(with_categories=True) %}
# { % if category == 'error' %}
# < script
# type = "text/javascript" >
# swal({
#     'title': '错误',
#     'text': '{{ message }}',
#     'type': 'error',
#     'showCancelButton': false,
#     'showConfirmButton': false,
#     'timer': 2000
# });
# < / script >
# { % elif category == 'success' %}
# < script
# type = "text/javascript" >
# swal({
#     'title': '正确',
#     'text': '{{ message }}',
#     'type': 'success',
#     'showCancelButton': false,
#     'showConfirmButton': false,
#     'timer': 2000,
# })
# < / script >
# { % end %}
# { % end %}
