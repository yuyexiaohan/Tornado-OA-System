//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}



//点击提交评论按钮函数
$(document).ready(function () {
    $('#comment-add').click(function () {
        event.preventDefault();
        var comment_content = $('#comment-content').val();
        var article_id = $('#comment-add').attr("data-id");
        $.ajax({
            'url': '/article/addcomment',
            'type': 'post',
            'data': {
                'content': comment_content,
                'id': article_id
            },
            'headers':{
              "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
                if(data['status'] == 200){
                     swal({
                            'title': '添加评论成功',
                            'text': data['msg'],
                            'type': 'success',
                            'showCancelButton': false,
                            'showConfirmButton': false,
                            'timer': 1000,
                     },function () {
                         //window.location = '/article/article?id='+ article_id;
                         location.reload();
                     })
                }
            }
        })
    })
});

//点击点赞按钮函数
$(document).ready(function () {
    $('#like-btn').click(function () {
        event.preventDefault();
        var article_id = $('#comment-add').attr("data-id");
        var like = $('#like').attr("data");
        if(like=='yes'){
            var like_text = '确定要点赞吗';
            var like_title = '点赞成功';
        }else{
            var like_text = '要取消点赞吗';
            var like_title = '取消点赞成功';
        }
        swal({
              'title': '提示',
              'text': like_text,
              'type': 'info',
              'showCancelButton': true,
              'closeOnConfirm': false,
              'confirmButtonText': '确定',      //定义确定按钮文本内容
              'cancelButtonText': '取消'
        },function () {
            $.ajax({
                'url': '/article/addlike',
                'type': 'post',
                'data': {
                    'article_id': article_id
                },
                'headers': {
                  'x-xsrftoken': get_cookie('_xsrf')
                },
                'success': function (data) {
                    if(data['status'] == 200){
                        swal({
                              'title': like_title,
                              'text': data['msg'],
                              'type': 'success',
                              'showCancelButton': false,
                              'showConfirmButton': false,
                              'timer': 1500,
                        },function () {
                            location.reload();
                        });
                    }else{
                         swal({
                                'title': '提示',
                                'text': data['msg'],
                                'type': 'info',
                                'showCancelButton': false,
                                'showConfirmButton': false,
                                'timer': 1500,
                         })
                    }
                }
            })
        });
    })
});

//显示评论框
$(document).ready(function () {
    $('.second-commend-btn').click(function () {
        event.preventDefault();
        var id = "#"+$(this).attr("data-id"); //'#5'
        $(id).toggle(500);
    });
});

//二级评论按钮函数
$(document).ready(function () {
    $('.seconde-comment-add').click(function () {
        event.preventDefault();
        var commont_id = $(this).attr("d-id");
        var se = '.seconde-comment-content'+commont_id;
        var comment_content = $(se).val();
        //var article_id = $('#comment-add').attr("data-id");
        $.ajax({
            'url': '/article/addsecondcomment',
            'type': 'post',
            'data': {
                'id': commont_id,
                'content': comment_content
            },
            'headers':{
              'X-XSRFTOKEN': get_cookie('_xsrf')
            },
            'success': function (data) {
                if(data['status'] == 200){
                     swal({
                            'title': '添加二级评论成功',
                            'text': data['msg'],
                            'type': 'success',
                            'showCancelButton': false,
                            'showConfirmButton': false,
                            'timer': 1000,
                     },function () {
                         location.reload();
                     })
                }else{
                    swal({
                            'title': '添加二级评论失败',
                            'text': data['msg'],
                            'type': 'error',
                            'showCancelButton': false,
                            'showConfirmButton': false,
                            'timer': 1000,
                     },function () {
                         location.reload();
                     })
                }

            }
        })
    });
});
