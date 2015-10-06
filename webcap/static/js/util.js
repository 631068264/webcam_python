/**
 * Created by wyx<wyx@youjianghr.com> on 2015/8/8.
 */
function getRoot() {
    return window.location.protocol + "//" + window.location.host;
}

function getAppPath() {
    return getRoot() + window.location.pathname;
}