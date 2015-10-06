var time = null;
var display = null;

function Toast(id, msg, dur) {
    dur = isNaN(dur) || dur <= 0 ? 3 : dur;
    var node = $("#" + id);
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
        "z-index":"1000"
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
        display = setTimeout(function () {
            node.css("display", "none");
        }, 1000);
    }, 1000 * dur);

}





