/**
 * Created by sa on 16-12-17.
 */
var ajax = function (method,url,data) {
    var promise = new Promise(function (resolve,reject) {
        $.ajax({
            url:url,
            method:method,
            beforeSend:function () {
                $(".mask").show();
            },
            data:data,
            success:function (data) {
                $(".mask").hide();
                resolve(data);
            },
            error:function (e) {
                reject(e);
                $(".ajax_error").html("请求错误！");
                $(".mask").hide();
                $(".modal").modal("toggle");
            }
        });
    });
    return promise;
};
module.exports = {
    ajax:ajax
};
