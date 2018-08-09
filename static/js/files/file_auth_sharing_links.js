//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}


//添加分類的函數
$(document).ready(function(){
    var username = $('#sharing_username_uuid').attr('data-id');
    var uuid = $('#sharing_username_uuid').attr('data-uuid');
    var msg = $('#sharing_username_uuid').attr('data-msg');
    if(msg == ''){
        var titile1 = username + '：给您加密分享了文件';
        var msg1 = '请输入分享密码';
    }else{
        var titile1 = msg;
        var msg1 = '请输重新获取分享密码'
    }
    swal({
        'title': titile1,             //提示框标题
        'text': msg1,            //提示内容
        'type':'input',            //提示类型，有：success（成功），error（错误），warning（警告），input（输入）
        'showCancelButton': true,       //是否显示“取消”按钮。
        'animation': 'slide-from-top',  //提示框弹出时的动画效果，如slide-from-top（从顶部滑下）等
        'closeOnConfirm': false,        //确认按钮被关闭后，Alert也被关闭，设为false将自动调用下面的函数——也就是启动后续Alert。
        'showLoaderOnConfirm': true,        //
        'inputPlaceholder': '输入密码',  //
        'confirmButtonText': '确定',      //定义确定按钮文本内容
        'cancelButtonText': '取消'        //定义取消按钮文本内容
    },function (inputValue) {
        if(inputValue == ''){
            swal.showInputError('输入框不能为空！');
            return false;
        }
        $.ajax({
            'url': '/files/files_auth_sharing_links',
            'type': 'post',
            'data': {
               'password': inputValue,
               'uuid': uuid
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
                    'timer': 2000
                   },function () {
                       window.location = data['links']
                   });
               }else {
                    swal({
                    'title': '错误',
                    'text': data['msg'],
                    'type': 'error',
                    'showCancelButton': false,
                    'showConfirmButton': false,
                    'timer': 2000
                    },function () {
                       location.reload();
                   });
               }
            }
        });
    });
});


