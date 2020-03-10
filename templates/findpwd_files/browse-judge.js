//判断操作系统和浏览器类型，需要判断的页面加上detectOS()；
(function detectOS() { 
	var sUserAgent = navigator.userAgent; 
	var isWin = (navigator.platform == "Win32") || (navigator.platform == "Windows");
	
	if (isWin) { 
		var isWin2K = sUserAgent.indexOf("Windows NT 5.0") > -1 || sUserAgent.indexOf("Windows 2000") > -1; 
		var isWinXP = sUserAgent.indexOf("Windows NT 5.1") > -1 || sUserAgent.indexOf("Windows XP") > -1; 
		var isWin2003 = sUserAgent.indexOf("Windows NT 5.2") > -1 || sUserAgent.indexOf("Windows 2003") > -1; 
		var isWinVista= sUserAgent.indexOf("Windows NT 6.0") > -1 || sUserAgent.indexOf("Windows Vista") > -1; 
		var isWin7 = sUserAgent.indexOf("Windows NT 6.1") > -1 || sUserAgent.indexOf("Windows 7") > -1; 
		
		 if(navigator.userAgent.indexOf("MSIE 8.0")>0 || navigator.userAgent.indexOf("MSIE 6.0")>0 || navigator.userAgent.indexOf("MSIE 7.0")>0){//IE8.0
			if (isWin2K  || isWinXP || isWin2003 || isWinVista){ //xp系统和其他低版本系统
				$(document.body).append("<div class='tips_top' style='z-index:9999;'><div class='w_1000'><span>亲爱的用户，为了达到最优的网站体验效果，我们建议您安装/使用下列最新版本浏览器：</span><ul class='browser_list'><li><a href='http://www.google.cn/intl/zh-CN/chrome/browser/' target='_blank'><i class='ico_browser c'></i>chrome</a></li><li><a  href='http://www.firefox.com.cn/download/' target='_blank'><i class='ico_browser f'></i>Firefox</a></li><li><a href='http://support.apple.com/kb/DL1531?viewlocale=zh_CN' target='_blank'><i class='ico_browser s'></i>safari</a></li></ul><a href='javascript:;' class='close'><i class='ico_browser'></i></a></div></div>");
				$(".tips_top .close").click(function(){
					$(".tips_top").animate({top:"-35px"},function(){$(".tips_top").remove()});
				});
			}
			else if (isWin7) //w7系统
			{
				$(document.body).append("<div class='tips_top' style='z-index:9999;'><div class='w_1000'><span>亲爱的用户，为了达到最优的网站体验效果，我们建议您安装/使用下列最新版本浏览器：</span><ul class='browser_list'><li><a  href='http://windows.microsoft.com/zh-cn/internet-explorer/download-ie' target='_blank'><i class='ico_browser i'></i>Internet Explorer 11</a></li><li><a href='http://www.google.cn/intl/zh-CN/chrome/browser/' target='_blank'><i class='ico_browser c'></i>chrome</a></li><li><a  href='http://www.firefox.com.cn/download/' target='_blank'><i class='ico_browser f'></i>Firefox</a></li><li><a href='http://support.apple.com/kb/DL1531?viewlocale=zh_CN' target='_blank'><i class='ico_browser s'></i>safari</a></li></ul><a href='javascript:;' class='close'><i class='ico_browser'></i></a></div></div>");
				$(".tips_top .close").click(function(){
					$(".tips_top").animate({top:"-35px"},function(){$(".tips_top").remove()});
				});
			}
		}
		
	}
})();