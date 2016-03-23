/**
 * Created by wyx<wyx@youjianghr.com> on 2015/8/8.
 */

function getRoot() {
    return window.location.protocol + "//" + window.location.host;
}

function getAppPath() {
    return getRoot() + window.location.pathname;
}

function goTo(href) {
    if (href != null) {
        window.location.href = href
    }
}

//返回顶部
function GoUp(dom, image_path, min_height) {
    //预定义返回顶部的html代码，它的css样式默认为不显示
    var gotoTop_dom = '<img src="' + image_path + '" id="gotoTop" title="回到顶部" style="display:none;">';
    //将返回顶部的html代码插入页面上id为page的元素的末尾
    $(dom).html(gotoTop_dom);
    $('#gotoTop').css({
        "position": "fixed",
        "cursor": "pointer",
        "top": "77%",
        "left": "92%",
        "width": "34px"
    });
    $("#gotoTop").click(//定义返回顶部点击向上滚动的动画
        function () {
            $('html,body').animate({scrollTop: 0}, 700);
        }).hover(//为返回顶部增加鼠标进入的反馈效果，用添加删除css类实现
        function () {
            $(this).addClass("hover");
        },
        function () {
            $(this).removeClass("hover");
        });
    //获取页面的最小高度，无传入值则默认为600像素
    min_height ? min_height = min_height : min_height = 600;
    //为窗口的scroll事件绑定处理函数
    $(window).scroll(function () {
        //获取窗口的滚动条的垂直位置
        var s = $(window).scrollTop();
        //当窗口的滚动条的垂直位置大于页面的最小高度时，让返回顶部元素渐现，否则渐隐
        if (s > min_height) {
            $("#gotoTop").fadeIn(100);
        } else {
            $("#gotoTop").fadeOut(200);
        }

    });
}


//Toast消息
var time = null;
var display = null;

function Toast(dom, msg, location, dur) {
    //默认显示秒数
    dur ? dur = dur : dur = 2;

    var node = $(dom);
    node.css({
        "font-family": "微软雅黑",
        "font-size": "12px 1.37em",
        "position": "fixed",
        "bottom": "25%",
        "width": "100%",
        "opacity": "0",
        "height": "24px",
        "display": "none",
        "transition": "opacity 1s ease-out",
        "text-align": "center",
        "z-index": "1000"
    });

    //消息div
    var mdiv = $('<div></div>');
    mdiv.css({
        "color": "#fff",
        "background": "rgba(0, 0, 0, 0.5)",
        "border-radius": "5px",
        "padding": "5px",
        "margin": "0 auto",
        "display": "inline"
    });
    mdiv.html(msg);

    if (time != null) {
        clearTimeout(time);
        clearTimeout(display);
    }

    node.css({"display": "block", "opacity": "1"});
    node.html(mdiv);
    time = setTimeout(function () {
        node.css("opacity", "0");
        console.log("1");
        display = setTimeout(function () {
            node.css("display", "none");
            console.log("3");
            //延时跳转
            location ? window.location.href = location.split('#')[0] : location = null;
            console.log(location);
        }, 1000);
        console.log("2");
    }, 1000 * dur);

}


function ok(msg) {
    Toast("#msg", msg, null, 2);
}
function error(msg) {
    Toast("#msg", msg, null, 3);
}

function redirect(msg, location) {
    if (location == null) {
        location = window.location.href;
    }
    Toast('#msg', msg, location, 1);
}

function refresh() {
    window.location.href = window.location.href.split('#')[0];
}

function log(msg) {
    console.log(msg);
}