var lang;
$(function(){
    jQuery.i18n.properties({
        name : 'strings',
        path : _path+'/style/i18n/',
        mode : 'map',
        language : getCookie("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE"),
        callback : function() {
        	lang = getCookie("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE");
        	var cla = $("body").attr("class");
        	if (lang) {
        		if (lang && lang == "zh_CN") lang = "zh";
        		if (cla) {
    				$("body").attr("class",cla+" "+lang);
    			} else {
    				$("body").attr("class",lang);
    			}
        	}
        }
    });
});

function getCookie(name)
{
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
    if(arr=document.cookie.match(reg)){
        return unescape(arr[2]);
    }
    else{
        return "zh";
    }
}