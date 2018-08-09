
//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}


//添加分類的函數
$(document).ready(function(){
    $('#category-btn').click(function () {
        swal({
            'title': '请输入分类',             //提示框标题
            'text': '输入文章的分类',            //提示内容
            'type':'input',            //提示类型，有：success（成功），error（错误），warning（警告），input（输入）
            'showCancelButton': true,       //是否显示“取消”按钮。
            'animation': 'slide-from-top',  //提示框弹出时的动画效果，如slide-from-top（从顶部滑下）等
            'closeOnConfirm': false,        //确认按钮被关闭后，Alert也被关闭，设为false将自动调用下面的函数——也就是启动后续Alert。
            'showLoaderOnConfirm': true,        //
            'inputPlaceholder': '输入邮箱',  //
            'confirmButtonText': '确定',      //定义确定按钮文本内容
            'cancelButtonText': '取消'        //定义取消按钮文本内容
        },function (inputValue) {
            if(inputValue == ''){
                swal.showInputError('输入框不能为空！');
                return false;
            }
            $.ajax({
                'url': '/article/add_category_tag_list',
                'type': 'post',
                'data': {
                   'category_name': inputValue
                },
                'headers': {
                    "X-XSRFTOKEN":get_cookie("_xsrf")
                },
                'success': function (data) {
                   if(data['status'] == 200){
                       swal({
                        'title': '正确',
                        'text': data['msg'],
                        'type': 'success',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1000
                       },function () {
                           location.reload();
                       });
                   }else {
                        swal({
                        'title': '错误',
                        'text': data['msg'],
                        'type': 'error',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1000
                        });
                   }
                }
            });
        });
    });
});


//添加标签的函數
$(document).ready(function(){
    $('#tag-btn').click(function () {
        swal({
            'title': '请输入分类',             //提示框标题
            'text': '输入标签的分类',            //提示内容
            'type':'input',            //提示类型，有：success（成功），error（错误），warning（警告），input（输入）
            'showCancelButton': true,       //是否显示“取消”按钮。
            'animation': 'slide-from-top',  //提示框弹出时的动画效果，如slide-from-top（从顶部滑下）等
            'closeOnConfirm': false,        //确认按钮被关闭后，Alert也被关闭，设为false将自动调用下面的函数——也就是启动后续Alert。
            'showLoaderOnConfirm': true,        //
            'inputPlaceholder': '输入邮箱',  //
            'confirmButtonText': '确定',      //定义确定按钮文本内容
            'cancelButtonText': '取消'        //定义取消按钮文本内容
        },function (inputValue) {
            if(inputValue == ''){
                swal.showInputError('输入框不能为空！');
                return false;
            }
            $.ajax({
                'url': '/article/add_category_tag_list',
                'type': 'post',
                'data': {
                   'tag_name': inputValue
                },
                'headers': {
                    "X-XSRFTOKEN":get_cookie("_xsrf")
                },
                'success': function (data) {
                   if(data['status'] == 200){
                       swal({
                        'title': '正确',
                        'text': data['msg'],
                        'type': 'success',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1000,
                        'closeOnConfirm': false
                       },function () {
                           location.reload();
                       });
                   }else {
                        swal({
                        'title': '错误',
                        'text': data['msg'],
                        'type': 'error',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1000
                        });
                   }
                }
            });
        });
    });
});