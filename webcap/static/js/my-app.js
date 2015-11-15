// Initialize your app
var myApp = new Framework7({
    modalTitle: '马上兼职',
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

function my_error(msg) {
    myApp.alert(msg, "出错啦");
}
function my_alert(msg) {
    myApp.alert(msg);
}

myApp.onPageInit('about', function (page) {

});

