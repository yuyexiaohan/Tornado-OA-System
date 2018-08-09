//获取图形验证码
var code = "";
function get_image_code() {
    var d = new Date().getTime();
    var pre_code = code;
    code = d;
    $(".get_image_code").attr("src", "/auth/captcha?pre_code="+pre_code+"&code="+code);
    $(".captcha-code").attr("value",code);
}


$(document).ready(function(){
    get_image_code();
    //点击获取图形验证码
    $('#a_code').click(function () {
        get_image_code();
    });
});
