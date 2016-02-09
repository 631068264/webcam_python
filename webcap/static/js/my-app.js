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

var app_location = "/webcam";

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
    $$(page.container).find("script").each(function (el) {
        if ($(this).attr('src')) {
            jQuery.getScript($(this).attr('src'));
        } else {
            eval($(this).text());
        }
    });
});
//首页js
$$(document).on('click', '#btn_logout', function () {
    $.get(app_location + "/logout", function (ret) {
        window.location.reload();
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
    myApp.alert(msg, "请注意！");
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
            if (resp.status == 1) {
                ok('登录成功');
                window.location.href = redirect;
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
            if (resp.status == 1) {
                ok('注册成功');
                window.location.href = redirect;
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

myApp.onPageInit('device_list', function (page) {
    var ptrContent = $$('#device-list-pull-to-refresh-content');

    //refresh 监听器
    ptrContent.on('refresh', function (e) {
        $.ajax({
            url: app_location + "/device/list/load?type=block",
            type: "get",
            success: function (data) {
                $("#device_list_container").html(data);
                myApp.pullToRefreshDone();
            },
            error: function (data) {
                error("刷新失败");
                myApp.pullToRefreshDone();
            }
        });
    });
    //删除设备
    ptrContent.on('click', 'a[btn_type="cancel"]', function () {
        var device_id = $(this).attr("device_id");
        var device_name = $(this).attr("device_name");
        myApp.modal({
            text: '<div>你要删除的设备：</div><br><div>设备号：' + device_id + '</div><br><div>设备名：' + device_name + '</div><br>',
            buttons: [{
                text: '好的',
                blod: true,
                onClick: function () {
                    $(this).addClass('disabled');
                    $.post(
                        app_location + "/device/cancel",
                        {device_id: device_id},
                        function (resp) {
                            if (resp.status == 1) {
                                $(this).removeClass('disabled');
                                myApp.pullToRefreshTrigger(ptrContent);
                                ok('删除成功');
                            } else {
                                error(resp.message);
                            }
                        }
                    ).fail(function () {
                            $(this).removeClass('disabled');
                            error('网络故障 请检查网络连接!');
                        });
                }
            }, {
                text: '取消',
                blod: true
            }]
        });
    });

    $$('#device_add').on('click', function () {
        myApp.prompt('请输入设备名', function (device_name) {
            $.post(
                '/webcam/device/add',
                {device_name: device_name},
                function (resp) {
                    if (resp == 1) {
                        ok('创建设备成功');
                    } else {
                        error(resp.message);
                    }
                }
            ).fail(
                function () {
                    error('网络故障 请检查网络连接!');
                }
            );
        });
    });
});

myApp.onPageInit('task_list', function (page) {
    var ptrContent = $$('#task-list-pull-to-refresh-content');

    //refresh 监听器
    ptrContent.on('refresh', function (e) {
        $.ajax({
            url: app_location + "/task/list/load?type=block",
            type: "get",
            success: function (data) {
                $("#task_list_container").html(data);
                myApp.pullToRefreshDone();
            },
            error: function (data) {
                error("刷新失败");
                myApp.pullToRefreshDone();
            }
        });
    });

    //删除任务
    ptrContent.on('click', 'a[btn_type="delete"]', function () {
        var task_id = $(this).attr("task_id");

        myApp.modal({
            text: '<div>你要删除的任务：</div><br><div>任务号：' + task_id + '</div><br>',
            buttons: [{
                text: '好的',
                blod: true,
                onClick: function () {
                    $(this).addClass('disabled');
                    $.post(
                        app_location + "/task/cancel",
                        {task_id: task_id},
                        function (resp) {
                            if (resp.status == 1) {
                                $(this).removeClass('disabled');
                                myApp.pullToRefreshTrigger(ptrContent);
                                ok('删除成功');
                            } else {
                                error(resp.message);
                            }
                        }
                    ).fail(function () {
                            $(this).removeClass('disabled');
                            error('网络故障 请检查网络连接!');
                        });
                }
            }, {
                text: '取消',
                blod: true
            }]
        });
    });

    //改变设备
    $('select[select_type="change_device"]').change(function () {
        var task_id = $(this).attr('task_id');
        var device_id = $(this).val();
        var device_name = this.options[this.selectedIndex].text;

        myApp.modal({
            text: '<div>你确定要把执行设备改为：</div><br><div>设备名：' + device_name + '</div><br>',
            buttons: [{
                text: '好的',
                blod: true,
                onClick: function () {
                    $.post(
                        app_location + "/task/change/device",
                        {task_id: task_id, device_id: device_id},
                        function (resp) {
                            if (resp.status == 1) {
                                myApp.pullToRefreshTrigger(ptrContent);
                                ok('修改成功');
                            } else {
                                error(resp.message);
                            }
                        }
                    ).fail(function () {
                            error('网络故障 请检查网络连接!');
                        });
                }
            }, {
                text: '取消',
                blod: true
            }]
        });
    });
});

myApp.onPageInit('device_info', function (page) {
    var redirect = $("#form_device_info").data('redirect');
    $$("#btn_device_info").on("click", function (e) {
        $("#btn_device_info").attr("disabled", true);
        $('#form_device_info').submit();
    });

    $("#form_device_info").ajaxForm({
        success: function (resp) {
            $("#btn_device_info").attr("disabled", false);
            console.log(resp);
            if (resp.status == 1) {
                ok('修改成功');
                refreshBack(page, redirect);
            } else {
                error(resp.message);
            }
        },
        error: function (resp) {
            $("#btn_device_info").attr("disabled", false);
            ok('网络故障 请检查网络连接!');
        }
    });
});


myApp.onPageInit('task_add', function (page) {
    //日常任务
    var redirect = $("#form_add_common_task").data('redirect');
    $$("#btn_add_common_task").on("click", function (e) {
        $("#btn_add_common_task").attr("disabled", true);
        $('#form_add_common_task').submit();
    });

    $("#form_add_common_task").ajaxForm({
        success: function (resp) {
            $("#btn_add_common_task").attr("disabled", false);
            console.log(resp);
            if (resp.status == 1) {
                ok('新增日常任务成功');
                refreshBack(page, redirect);
            } else {
                error(resp.message);
            }
        },
        error: function (resp) {
            $("#btn_add_common_task").attr("disabled", false);
            ok('网络故障 请检查网络连接!');
        }
    });

    //循环任务
    var redirect = $("#form_add_common_task").data('redirect');
    $$("#btn_add_cycle_task").on("click", function (e) {
        $("#btn_add_cycle_task").attr("disabled", true);
        $('#form_add_cycle_task').submit();
    });

    $("#form_add_cycle_task").ajaxForm({
        success: function (resp) {
            $("#btn_add_cycle_task").attr("disabled", false);
            console.log(resp);
            if (resp.status == 1) {
                ok('新增循环任务成功');
                refreshBack(page, redirect);
            } else {
                error(resp.message);
            }
        },
        error: function (resp) {
            $("#btn_add_cycle_task").attr("disabled", false);
            ok('网络故障 请检查网络连接!');
        }
    });


    //页面设置
    $("input:checkbox[name = 'now']").change(function () {
        var now = $(this).val();
        $('#form_task_dates').toggle(now);
        $('#form_execute_time').toggle(now);
    });
    $("input:radio[name = 'type']").change(function () {
        var flag = $(this).val();
        console.log(flag);
        $('.form_duration').toggle(flag);
    });

});

myApp.onPageInit('src_list', function (page) {
    var ptrContent = $$('#src-list-pull-to-refresh-content');

    //refresh 监听器
    ptrContent.on('refresh', function (e) {
        $.ajax({
            url: app_location + "/src/list/load?type=block",
            type: "get",
            success: function (data) {
                $("#src_list_container").html(data);
                myApp.pullToRefreshDone();
            },
            error: function (data) {
                error("刷新失败");
                myApp.pullToRefreshDone();
            }
        });
    });


});