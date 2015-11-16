// Initialize your app
var myApp = new Framework7({
    modalTitle: 'WebCam',
    modalButtonOk: '确定',
    modalButtonCancel: '取消',
    animateNavBackIcon: true,
    cache: false,
    cacheIgnore: [],
    onAjaxStart: function (xhr) {
        myApp.showIndicator();
    },
    onAjaxComplete: function (xhr) {
        myApp.hideIndicator();
    },
    onAjaxError: function (xhr) {
        myApp.hideIndicator();
        myApp.alert('网络故障 请检查网络连接!');
    }
});

jQuery.ajaxSetup({
    beforeSend: function (xhr) {
        xhr.setRequestHeader('x-json', 'true');
    }
});

// Export selectors engine
var $$ = Dom7;

// Add view
var mainView = myApp.addView('.view-main', {
    // Because we use fixed-through navbar we can enable dynamic navbar
    dynamicNavbar: true
});

//导入其他js
$$(document).on('pageInit', function (e) {
    var page = e.detail.page;
    console.log(e);
    $$(page.container).find("script").each(function (el) {
        if ($(this).attr('src')) {
            jQuery.getScript($(this).attr('src'));
        } else {
            eval($(this).text());
        }
    });
});

function goBack() {
    $$(".back").click();
}

function refreshBack(page, redirect) {
    page.view.router.back({
        url: redirect,
        force: true,
        ignoreCache: true
    })
}

function error(msg) {
    myApp.alert(msg, "出错啦");
}
function ok(msg) {
    myApp.alert(msg);
}

myApp.onPageInit('login-page', function (page) {
    var redirect = $("#form_login").data('redirect');
    $$("#btn_login").on("click", function (e) {
        $("#btn_login").attr("disabled", true);
        $('#form_login').submit();
    });

    $("#form_login").ajaxForm({
        success: function (resp) {
            $("#btn_login").attr("disabled", false);
            console.log(resp);
            if (resp.status == 1) {
                ok('登录成功');
                refreshBack(page, redirect);
            } else {
                error(resp.message);
            }
        },
        error: function (resp) {
            $("#btn_login").attr("disabled", false);
            ok('网络故障 请检查网络连接!');
        }
    });

});
myApp.onPageInit('register-page', function (page) {
    var redirect = $("#form_register").data('redirect');
    $$("#btn_register").on("click", function (e) {
        $("#btn_register").attr("disabled", true);
        $('#form_register').submit();
    });

    $("#form_register").ajaxForm({
        success: function (resp) {
            $("#btn_register").attr("disabled", false);
            console.log(resp);
            if (resp.status == 1) {
                ok('注册成功');
                refreshBack(page, redirect);
            } else {
                error(resp.message);
            }
        },
        error: function (resp) {
            $("#btn_register").attr("disabled", false);
            ok('网络故障 请检查网络连接!');
        }
    });

});

