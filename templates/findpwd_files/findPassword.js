var min_passwd_len = 6;
/**
 * 页面加载时获取公钥，提高表单提交速率
 */
$(document).ready(function() {
	refreshCode();
	getMmclsm() ;
	$.ajax({ url: "getPublicKey.zf",async:false, cache: false}).done(function (rd){
		if(rd!=null){
			//加密模
			Modulus = rd.split(';')[0];
			//公钥指数
			public_exponent = rd.split(';')[1];
		}
	});
	
	$("input[name='radioInline']").each(
			function(){
				$(this).click(
						function(){
								$("#bdyz").html("");
								if($(this).val()=="byPhone.zf"){
									$("#byphoneMessage").css("display","");
									$("#bymailMessage").css("display","none");
									$("input[name='mailLine']").removeAttr('checked');
								}else if($(this).val()=="byMail.zf"){
									$("#byphoneMessage").css("display","none");
									$("#bymailMessage").css("display","");
									$("input[name='phoneLine']").removeAttr('checked');
								}else{
									$("#byphoneMessage").css("display","none");
									$("#bymailMessage").css("display","none");
									$("input[name='phoneLine']").removeAttr('checked');
									$("input[name='mailLine']").removeAttr('checked');
								}
								
								
									}
							)
					}
			)
			
		$("input[name='phoneLine']").each(
			function(){
				$(this).click(
						function(){
								if("(无数据)"==$("#"+$(this).val()).text()){
									$(this).removeAttr('checked');
								}
									}
							)
					}
			)
			$("input[name='mailLine']").each(
			function(){
				$(this).click(
						function(){
								
							if("(无数据)"==$("#"+$(this).val()).text()){
								$(this).removeAttr('checked');
							}
									}
							)
					}
			)
			
});

var Modulus = null ;
var public_exponent = null ;

function refreshCode(){
//  document.getElementById("yzmPic").src = _path + '/xtgl/login_code.html?time=' + new Date().getTime();
	if ($("#yzm").size() > 0){
		$("#yzmPic").attr("src", _path + '/kapt?time=' + new Date().getTime());
	}
}

//添加元素
function createElement(eleType, id, name, value, isHidden, parentId) {
	var newElement = document.createElement(eleType);
	newElement.setAttribute("id", id);
	newElement.setAttribute("name", name);
	newElement.setAttribute("value", value);
	if (isHidden) {
		newElement.setAttribute("type", "hidden");
	}
	var parentEle = document.getElementById(parentId);
	parentEle.appendChild(newElement);
	return newElement;
}

function decideStep() {
	// var step = $("#step").value;
	var step = document.getElementById("step").value;
	/*
	 * if("step1" == step ){ return stepOne(); }else if("step2" == step){ return
	 * stepTwo(); }else if("step3" == step){ return stepThree(); }else
	 * if("step4" == step){ return stepFour(); }
	 */
	switch (step) {
	case "step1":
		return stepOne();
		break;
	case "step2":
		return stepTwo();
		break;
	case "step3":
		return stepThree();
		break;
	case "step4":
		return stepFour();
		break;
	}
}
function nosfyz(){
	showMessage("sfyz", "", "none");
	showMessage("yzmyz", "", "none");
	
}
function stepOne() {
	var result = false;
	var nextURL = document.getElementById("step1URL").value;
	var userName = document.getElementById("userName").value;
	var idCard = document.getElementById("idCard").value;
	var yzm=document.getElementById("yzm").value;
	var key = new RSAUtils.getKeyPair(public_exponent, "", Modulus);
	//颠倒密码的顺序，要不然后解密后会发现密码顺序是反的
	idCard= idCard.split("").reverse().join("");
	//对密码进行加密传输 
	var idCard = RSAUtils.encryptedString(key,idCard);
	showMessage("sfyz", "", "none");
	showMessage("yzmts","", "none");
	if (userName == "" || idCard == "") {
		showMessage("sfyz", $.i18n.prop('securitycenter.findpassword.Username.identification.number.blank'), "");
		return false;
	}
	$.ajax({
		url : nextURL,
		async : false,
		cache : false,
		data : {
			'username' : userName,
			'idCard' : idCard,
			'yzm' : yzm
		}
	}).done(function(data) {
		refreshCode();
		if ("success" != data.code) {
			if("yzmfaliure"==data.code){
				showMessage("yzmts",data.message, "");
				return ;
			}
			showMessage("sfyz",data.message, "");
		} else {
			document.getElementById("returnUsername").value = data.username;
			document.getElementById("step").value = data.step;
			showMessage("sfyz", "", "none");
			$("#sjhm").html(data.yhxx.sjhm);
			$("#lxdh").html(data.yhxx.lxdh);
			$("#dzyx").html(data.yhxx.dzyx);
			$("#yxdz").html(data.yhxx.yxdz);
			result = true;
		}
	});
	return result;
}

/**
 * 找回密码第二部，用户选择找回方式。
 * 
 * @returns
 */
function stepTwo() {
	var result = false;
	var nextURL;
	var mbxx;
	var radio = document.getElementsByName("radioInline");
	for (i = 0; i < radio.length; i++) {
		if (radio[i].checked) {
			nextURL = radio[i].value;
		}
	}
	if(nextURL=="byPhone.zf"){
		mbxx=$("input[name='phoneLine']:checked").val();
	}else if(nextURL=="byMail.zf"){
		mbxx=$("input[name='mailLine']:checked").val();;
	}
	document.getElementById("retakeType").value = nextURL;
	var username = document.getElementById("returnUsername").value;
	$ .ajax({
		url : nextURL,
		async : false,
		cache : false,
		data : {
			'username' : username,
			'mbxx':mbxx
		}
	}).done(function(data) {
			if ("success" != data.code) {
					document.getElementById("bdyz").innerHTML = data.message;
			} else {
				document.getElementById("bdyz").innerHTML="";
				document.getElementById("step").value = data.step;
				$("#code").css('display',"");
				$("#byquestion").css('display',"none");
				$("#mobileMail").html("");
				document.getElementById("mobileMail").innerHTML="";
				if ("" != data.nextURL) {
				}
				if ("byPhone.zf" == document
						.getElementById("retakeType").value) {
					$("#mobileMail").html(data.message);
				} else if("byMail.zf" == document
						.getElementById("retakeType").value) {
					document.getElementById("mobileMail").innerHTML =$.i18n.prop('securitycenter.findpassword.reserved.secret.mailbox')+":<a href='#' >"
							+ data.returnMobile
							+ "</a>"+$.i18n.prop('securitycenter.findpassword.Send.the.verification.code');
				}else if("byQuestion.zf" == document
						.getElementById("retakeType").value){
					$("#byquestion").css('display',"");
					$("#mbbs1").find("option[value='"+data.mbbs1+"']").attr("selected",true);
					$("#mbbs2").find("option[value='"+data.mbbs2+"']").attr("selected",true);
					$("#code").css('display','none');  
				}
				result = true;
			}
		});
	return result;
}

function stepThree() {

	var result = false;
	var username = document.getElementById("returnUsername").value;
	var code = document.getElementById("code").value;
	var retakeType = document.getElementById("retakeType").value;
	var nextURL = document.getElementById("step3" + retakeType).value;
	var question1 = document.getElementById("question1").value;
	var question2 = document.getElementById("question2").value;
	var mbbs1 = document.getElementById("mbbs1").value;
	var mbbs2 = document.getElementById("mbbs2").value;
	if((code==''||code==null)&&(question1==''||question2=='')){
		showMessage("yzmyz", $.i18n.prop('securitycenter.findpassword.questionError'), "");
		return false;
	}
	$.ajax({
		url : nextURL,
		async : false,
		cache : false,
		data : {
			'username' : username,
			'code' : code,
			'mbbs1':mbbs1,
			'mbbs2':mbbs2,
			'question1':question1,
			'question2':question2
		}
	}).done(function(data) {
			var jsonObject = eval("(" + data + ")");
			if ("success" != jsonObject.code) {
				if ("030" == jsonObject.errorCode) {
					showMessage("yzmyz", $.i18n.prop('securitycenter.findpassword.Invalid.authentication.code'), "");
				} else if ("031" == jsonObject.errorCode) {
					showMessage("yzmyz", $.i18n.prop('securitycenter.findpassword.verification.code.has.expired'), "");
				} else if ("033" == jsonObject.errorCode) {
					showMessage("yzmyz", $.i18n.prop('securitycenter.findpassword.questionError'), "");
				}else if ("034" == jsonObject.errorCode) {
					showMessage("yzmyz", $.i18n.prop('securitycenter.findpassword.questionfailed'), "");
					}
			} else {
				document.getElementById("step").value = jsonObject.step;
				if (!document.getElementById("validateID")) {
					createElement("input", "validateID","validateID", jsonObject.validateID,"true", "example-advanced-form");
				} else {
					document.getElementById("validateID").value = jsonObject.validateID;
				}
				
				result = true;
				$("#mmclsmDiv").show() ;
			}
		});
	return result;
}

function stepFour() {
	var result = false;
	var retakeType = document.getElementById("retakeType").value;
	var nextURL = document.getElementById("step4" + retakeType).value;
	var username = document.getElementById("returnUsername").value;
	var newPassword = document.getElementById("newPassword").value;
	var validateID = document.getElementById("validateID").value;
	//通过模和公钥参数获取公钥
	var key = new RSAUtils.getKeyPair(public_exponent, "", Modulus);
	//颠倒密码的顺序，要不然后解密后会发现密码顺序是反的
	var subNewPwd = newPassword.split("").reverse().join("");
	//对密码进行加密传输 
	var encrypedNewPwd = RSAUtils.encryptedString(key,subNewPwd);
	$('#subNewPwd').val(encrypedNewPwd);
	$("#newPassword").val(encrypedNewPwd);
	$("#repeatPassword").val(encrypedNewPwd);
	document.getElementById("example-advanced-form").action = nextURL;
	document.getElementById("example-advanced-form").submit();
	return result;
}

function repeatPassword() {
	var newPassword = document.getElementById("newPassword").value;
	var repeatPwd = document.getElementById("repeatPassword").value;
	if ("" == newPassword) {
		showMessage("mmyz",$.i18n.prop('securitycenter.findpassword.Password.cannot.be.empty'), "");
		return false;
	}
	
	if (newPassword.indexOf(" ") > -1 ) {
		showMessage("mmyz",$.i18n.prop('securitycenter.findpassword.Passwords.cannot.contain.spaces'), "");
		return false;
	}
	
	if (newPassword != repeatPwd) {
		showMessage("mmyz", $.i18n.prop('securitycenter.findpassword.password.notsame'), "");
		return false;
	}

	var strong = checkPasswdRate(newPassword) ;
	if ("0"==checkMmcl(newPassword)) {
    	showMessage("mmyz",$.i18n.prop('securitycenter.findpassword.password.notconform.to.the.password.policy'),"");
    	return false ;
    }else if ("-1" == checkMmcl(newPassword) && strong <2) {
    	showMessage("mmyz",$.i18n.prop('securitycenter.findpassword.new.password.is.too.weak'),"");
    	return false ;
    }
	
	return true;
}

/**
 * 单击前一步触发事件
 * 
 * @returns
 */
function priviousStep() {
	var step = document.getElementById("step").value;
	if ("step1" != step) {
		document.getElementById("step").value = "step"
				+ (parseInt(step.substr(4)) - 1);
	}
}


if (document.getElementById("repeatedSend")) {
	document.getElementById("repeatedSend").onclick = function() {
		stepTwo();
	}
}

if (document.getElementById("heshi")) {
	document.getElementById("heshi").onclick = function() {
		document.getElementById("step").value = "step1";
	}
}
/**
 * 显示消息
 */
function showMessage(id, value, display) {
	if (document.getElementById(id)) {
		document.getElementById(id).value = value;
		document.getElementById(id).style.display = display
	}
};

/**
 * 验证密码策略
 * @param newPwd
 * @returns
 */
function checkMmcl(newPwd){
	
	//通过模和公钥参数获取公钥
	var key = new RSAUtils.getKeyPair(public_exponent, "", Modulus);
	//颠倒密码的顺序，要不然后解密后会发现密码顺序是反的
	var subNewPwd = newPwd.split("").reverse().join("");
	//对密码进行加密传输 
	var encrypedNewPwd = RSAUtils.encryptedString(key,subNewPwd);
	var res = "-1" ;
	$.ajax({ url: "checkMmcl.zf",async:false, cache: false,data:{'subNewPwd':encrypedNewPwd}}).done(function (data){
		if ("false" == data){
			res = "0" ;
		}else if ("close" == data){
			res = "-1" ;
		}else {
			res = "1" ;
		}
	});
	return res ;
}

//CharMode函数 
//测试某个字符是属于哪一类. 
function CharMode(iN) {
	if (iN >= 48 && iN <= 57) //数字 
		return 1;
	if (iN >= 65 && iN <= 90) //大写字母 
		return 2;
	if (iN >= 97 && iN <= 122) //小写 
		return 4;
	else
		return 8; //特殊字符 
}
//bitTotal函数 
//计算出当前密码当中一共有多少种模式 
function bitTotal(num) {
	var modes = 0;
	for (i = 0; i < 4; i++) {
		if (num & 1)
			modes++;
		num >>>= 1;
	}
	return modes;
}
//checkStrong函数 
//返回密码的强度级别 
function checkPasswdRate(sPW) {
	if (sPW.length < min_passwd_len)
		return 0; //密码太短 
	var Modes = 0;
	for (i = 0; i < sPW.length; i++) {
		//测试每一个字符的类别并统计一共有多少种模式. 
		Modes |= CharMode(sPW.charCodeAt(i));
	}
	che=Modes;
	return bitTotal(Modes);
}

/**
 * 获取密码策略说明
 * @returns
 */
function getMmclsm(){
	var str = "" ;
	$.ajax({url:"getMmclsm.zf",async:false}).done(function(data){
		if ("-1" == data){
			$("#pwdLen").html($.i18n.prop('securitycenter.findpassword.Password.no.less.than.six.bits'));
			$("#pwdCha").html($.i18n.prop('securitycenter.findpassword.Password.rule'));
		}else {
			$("#pwdLen").html($.i18n.prop('securitycenter.findpassword.Password.length')+data.MINLENGTH+"--"+data.MAXLENGTH);
			if ("number" == data.CHNUMBER){
				str +=$.i18n.prop('securitycenter.findpassword.number');
			}
			if ("charcase" == data.CHARCASE) {
				str +=$.i18n.prop('securitycenter.findpassword.English.letter');
			}
			if ("specialchar" == data.SPECIALCHAR) {
				str += $.i18n.prop('securitycenter.findpassword.Special.characters');
			}
			str = str.substring(0,str.length-1) ;
			$("#pwdCha").html($.i18n.prop('securitycenter.findpassword.Must.contain')+":"+str);
		}
	});
}
/**
 * 显示密码策略
 * @param display
 * @returns
 */
function showMmcl(display) {
	document.getElementById("pass-tips").style.display = display ;
}