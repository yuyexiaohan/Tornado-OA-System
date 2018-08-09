

//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}


//simditor编辑器官网:http://simditor.tower.im/
// 初始化simditor的函数
$(document).ready(function() {
    var editor,toolbar;
    //编辑器工具栏里显示哪些工具
    toolbar = ['title', 'bold', 'italic', 'underline', 'strikethrough',
                'fontScale', 'color', '|', 'ol', 'ul', 'blockquote', 'code',
                'table', '|', 'link', 'image', 'hr', '|', 'indent', 'outdent', 'alignment'];
    //编辑器简体中文
    Simditor.locale = 'zh-CN';
    //初始化simditor
    editor = new Simditor({
        textarea: $('#simditor'),//获取在哪个div上显示编辑器
        toolbar: toolbar,   //编辑器的工具栏
        pasteImage: true   //支持复制粘贴
    });
    // 加到window上去,其他地方才能访问到editor这个变量
    window.editor = editor;
});


//点击提交文档按钮函数
$(document).ready(function () {
    $('#submit-article-btn').click(function () {
        //获取输入函数
        var title = $('#title-input').val();
        var article = window.editor.getValue();
        var desc = $('#desc-input').val();
        var category = $('#category-select').val();
        var thumbnail = $('#thumbnail-input').val();
        var tags = [];//[1,3,5]
        $('.tag-checkbox').each(function () {
            if ($(this).is(':checked')) {
                var tagId = $(this).val();
                tags.push(tagId);
            }
        });
        $.ajax({
            'url': '/article/add_article',
            'type': 'post',
            'data': {
                'title': title,
                'article': article,
                'desc': desc,
                'category': category,
                'thumbnail': thumbnail,
                'tags': JSON.stringify(tags),
                'article_id': $('#title-input').attr('data-article-id')
            },
            'headers': {
                "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
                if (data['status'] == 200) {
                    swal({
                        'title': '正确',
                        'text': data['msg'],
                        'type': 'success',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1000,
                    },function () {
                       window.location = '/article/article_list';
                    });
                }else{
                    swal({
                        'title': '错误',
                        'text': data['msg'],
                        'type': 'error',
                        'showCancelButton': false,
                        'showConfirmButton': false,
                        'timer': 1000,
                    })
                }
            }
        })
    });
});

$(document).ready(function () {
    var show = document.getElementById('show');
    //定义初始化函数入口判断浏览器是否支持filereader，函数中调用files_change()
    function init() {
        if (!(window.FileReader && window.File && window.FileList && window.Blob)) {
            show.innerHTML = '浏览器不支持fileReader';
            img_id.setAttribute('disabled', 'disabled');
            return false;
        }
        files_change();
    }
    init();

    //监控文件表单是否发生change事件
    function files_change() {
        $('#input_files_id').change(function () {
            console.log(this);
            console.log(this.files);
            var files = this.files;
            if (files) {
                for (var i = 0; i < files.length; i++) {
                    showfiles(this.files[i]);  //显示每一个选中的图片
                }
            }
        });
    }

    //显示每一个选中的图片
    function showfiles(f) {
        var html = '';
        if (f) {
            //创建FileReader对象
            var fr = new FileReader();
            //读取文件数据
            fr.readAsDataURL(f);
            //数据读取完成回调onload，e封装了读取文件的信息
            fr.onload = function (e) {
                html += '<div class="images item ">';
                html += '<div class="item"><img src="' + e.target.result + '" alt="img"></div>';
                html += '<p>' + f.name + '</p>';
                show.innerHTML += html
            };
        } else {
            show.innerHTML += html;
        }
    }
});
