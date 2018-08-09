//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}

$(document).ready(function () {
    //上传文件
    $("#upload_btn").click(function () {
        event.preventDefault();
        console.log($('#input_files_id'))
        console.log('-------------------==================-----------------');
        var formdata = new FormData();
        var files_upload = $('#input_files_id')[0];
        for (var i = 0; i < files_upload.files.length; i++) {
            console.log(files_upload.files[i]);
            formdata.append("importfile", files_upload.files[i]);
        }
        console.log('-------------------==================-----------------');
        console.log(formdata);
        $.ajax({
            'url': "/files/files_upload",
            'type': "POST",
            'data': formdata,
            'headers':{
               'X-XSRFTOKEN': get_cookie('_xsrf')
            },
            'cache': false,
            'processData': false,
            'contentType': false,
            'success': function (data) {
                if (data['status'] != 200) {
                    alert(data['msg']);
                } else {
                    var show_path = document.getElementById('show_path');
                    show_path.innerHTML = '';
                    for (var i = 0; i < data['data'].length; i++) {
                        var filename = data['data'][i]['data'];
                        var msg = data['data'][i]['msg'];
                        var html = '';
                        html += '<div class="images item ">';
                        html += '<div class="item">' + filename + '</div><br/>';
                        html += '<p>' + msg + '</p>';
                        show_path.innerHTML += html;
                    }
                }
            }
        });
    });
});

/*
{
    'status': 200,
    'msg': '保存成功',
    'data':
            [
                {'status': False, 'msg': '文件格式不正确', 'data':''},
                {'status': True, 'msg': '文件保存成功(其实以前有人上传过了)', 'data':file_path}
                {'status': True, 'msg': '文件保存成功', 'data': file_path}
            ]

 }
*/
