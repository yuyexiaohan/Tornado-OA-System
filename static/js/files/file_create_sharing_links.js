//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}


//添加分類的函數
$(document).ready(function(){
    var links = $('#sharing_links').attr('data-id');
    var password = $('#sharing_links').attr('data-password');
    swal({
        'title': '请复制下面链接',
        'text': '链接：'+links+',密码：'+ password,
        'type':'success',
        'animation': 'slide-from-top',
        'closeOnConfirm': false,
        'showLoaderOnConfirm': true,
        'confirmButtonText': '确定'
    },function () {
        window.location = '/files/files_page_list/1'
    });
});
