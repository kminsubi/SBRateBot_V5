
<!DOCTYPE html>
<html>
<head>











        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">  
        <!-- /* SR-250730-02752 구글 검색 영역 노출을 위한 HTML 태그 삽입 요청의 건(MO) START */ -->
        <!-- <meta name="robots" content="noindex">
        <meta name="googlebot" content="noindex"> -->
        <meta name="google-site-verification" content="iyWxyP4koMDPecZHC3UI2kDfAPrfHLbb4ZwV7gZxnSw" />
        <!-- /* SR-250730-02752 구글 검색 영역 노출을 위한 HTML 태그 삽입 요청의 건(MO) END */ -->  
            
        <meta name="naver-site-verification" content="3b79af2acd5d18b48bc58e099afea2a100bf260a"/> 
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no, target-densitydpi=medium-dpi">
        <meta name="format-detection" content="telephone=no">
        
<!--         <script src="https://developers.kakao.com/sdk/js/kakao.min.js"></script> --> 

		
        <!-- AS-IS script Start -->



         <script type="text/javascript" src="/mobweb/lib/js/view.js?ver=20260716"></script> 

        <!-- AS-IS script End -->
        
        <!-- TO-BE script Start -->
        <meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">
		<link rel="icon" href="/mobweb/images_kiwi/favicon.png" sizes="48x48" >
		<link rel="shortcut icon" type="image/x-icon" href="/mobweb/images_kiwi/favicon_192.png?ver=20260716">
		<link rel="apple-touch-icon" size="192x192" href="/mobweb/images_kiwi/favicon_192.png?ver=20260716">
		<link rel="apple-touch-icon-precomposed" size="192x192" href="/mobweb/images_kiwi/favicon_192.png?ver=20260716">

		<link rel="stylesheet" href="/mobweb/css_kiwi/mobiscroll/mobiscroll.custom-2.15.1.css?ver=20260716" />
		<link rel="stylesheet" href="/mobweb/css_kiwi/netfunnel.css?ver=20260716" />
		<link rel="stylesheet" href="/mobweb/css_kiwi/kiwibanking.css?ver=20260716">
		        
        <script type="text/javascript" src="/mobweb/js_kiwi/jquery-3.3.1.min.js?ver=20260716"></script>
		<script type="text/javascript" src="/mobweb/js_kiwi/jquery-ui.min.js?ver=20260716"></script>
		<script type="text/javascript" src="/mobweb/js_kiwi/jquery.scrollLock.js?ver=20260716"></script>
		<script type="text/javascript" src="/mobweb/js_kiwi/mobiscroll/mobiscroll.custom-2.15.1.min.js?ver=20260716"></script>
		<script type="text/javascript" src="/mobweb/js_kiwi/mobiscroll/mobiscroll.i18n.ko.js?ver=20260716"></script>
		<script type="text/javascript" src="/mobweb/js_kiwi/swiper.min.js?ver=20260716"></script>
		
		<script type="text/javascript" src="/mobweb/js_kiwi/lottie.min.js?ver=20260716"></script> 
		<script type="text/javascript" src="/mobweb/js_kiwi/ui-script.js?ver=20260716"></script>
		
		<script type="text/javascript" src="/mobweb/js_kiwi/common.js?ver=20260716"></script>
		<script type="text/javascript" src="/mobweb/js_kiwi/appBridge_PC.js?ver=20260716"></script>
		<script type="text/javascript" src="/mobweb/js_kiwi/kiwiSavingsCommon.js?ver=20260716"></script>
		<script type="text/javascript" src="/mobweb/js_kiwi/kds_hybrid_lib.js?ver=20260716"></script>

		
		<script type="text/javascript" src="/mobweb/js_kiwi/netfunnel/netfunnel.js?ver=20260716"></script>
		<script type="text/javascript" src="/mobweb/js_kiwi/netfunnel/netfunnel_skin.js?ver=20260716"></script>
		<script type="text/javascript" src="/mobweb/js_kiwi/maxy.js?ver=20260716"></script>

 		<script src="https://developers.kakao.com/sdk/js/kakao.js?ver=20260716"></script> 
		<!-- <script async src="https://www.googletagmanager.com/gtag/js?id=UA-74551103-10"></script> -->
<!-- 		<script async src="https://www.googletagmanager.com/gtag/js?id=G-6FT9Q4HYE0"></script> -->
		
		<script type="text/javascript" src="/mobweb/lib/js/common.js?ver=20260716"></script>
		
		
		<script type="application/ld+json">
		{
			"@context" : "https://schema.org",
			"@type" : "WebSite",
			"name" : "KB저축은행",
			"url" : "https://m.kbsavings.com"
		}
		</script>

<script>
        var ctx			= "/mobweb";
        
        var CUR_PAGE = '';
        var BACK_PAGE = '';
        var NEXT_PAGE = '';
        var BACK_YN = '';
        
		</script>


	    <!-- TO-BE script End -->
	    	    
        <script type="text/javascript">
      		//뒤로가기 버튼
        	function goBack() {
        		history.go(-1);	
        	}
        </script>
        
		<!-- /* 20181112 Emforce 김창석 Start */ -->
		
		
		<!-- /* 20181112 Emforce 김창석 End */ -->
        <script type="text/javascript">
		//앱다운 페이지 web일 경우 안보이도록	        
	    var mobileCheck = getMobile();
		if(!mobileCheck) {
			//PC
			$("#appDownLoad").hide();
			$("#appDownLoad1").hide();				
		} else {
			//모바일				
			if(iosCheck()) {
				//IOS
				$("#appDownLoad").prop('href',"https://itunes.apple.com/kr/app/kbchaghandaechul/id1006543056?mt=8");
				$("#appDownLoad1").prop('href',"https://itunes.apple.com/kr/app/kbchaghandaechul/id1006543056?mt=8");				
			} else {
				//Android
				$("#appDownLoad").prop('href',"https://play.google.com/store/apps/details?id=com.kbsavings.android");
				$("#appDownLoad1").prop('href',"https://play.google.com/store/apps/details?id=com.kbsavings.android");				
			}
		}
		function Firebase(temp){
			var phone_gb = "";
			var appUrl = "NONE";
			appUrl = appUrl.replace(".do","");
			var userAgent = navigator.userAgent;
			if(userAgent.match(/Android/)) phone_gb = "1";
			else if (userAgent.match(/iPhone|iPad|Macintosh|iPod/)) phone_gb="2";

			
			var url = "kbsavings://kbcert?target_url=/"+appUrl+".do";
			//var url = "kbsavings://kbcert?target_url=https://www.naver.com&urlparam=aabbccc";
			var androidStoreUrl = "https://play.google.com/store/apps/details?id=com.kbsavings.android";
			var iosStoreUrl = "https://itunes.apple.com/kr/app/kbchaghandaechul/id1006543056?mt=8";
			if(phone_gb =="1") {    
			    if(userAgent.match(/Chrome/)) {
			        location.href="intent://kbcert?target_url=/"+appUrl+".do#Intent;scheme=kbsavings;package=com.kbsavings.android;end;";
			        //location.href="intent://kbcert?target_url=https://www.naver.com&urlparam=aabbccc#Intent;scheme=kbsavings;package=com.kbsavings.android;end;";
			    }else{        
			        setTimeout(function(){
			            location.href = androidStoreUrl
			        },1500);
			        var iframe = document.createElement('iframe');
			        iframe.style.visivility = 'hidden';
			        iframe.src = url;
			        documentbody.appendChild(iframe);
			        documentbody.removeChild(iframe); //back호출 시 캐싱될 수 있으므로 제거.
			    }
			//IOS
			}else if(phone_gb =="2") {
				setTimeout(function(){
			    	UI.alert({
		    			text : 'KB저축은행(키위뱅크) 설치 페이지로 이동하시겠습니까?',
		    			cancel : true, /* 취소 버튼 있을시 true , 기본은 확인 버튼만 있는 구조 */
		    			cancelTxt : '아니요', /* 취소 버튼 텍스트 변경시 사용 */
		    			confirmTxt : '예', /* 컨펌 버튼 텍스트 변경시 사용 */
		    			onCancel : function(){
		    			},
		    			onConfirm : function(){
		    				location.href =iosStoreUrl;
		    			}
		    		});
			            
			    },500);
			    location.href = url;
			}
		}
		
		function lonFirebase(goUrl){
			var phone_gb = "";
			var appUrl =goUrl;
			appUrl = appUrl.replace(".do","");
			var userAgent = navigator.userAgent;
			if(userAgent.match(/Android/)) phone_gb = "1";
			else if (userAgent.match(/iPhone|iPad|Macintosh|iPod/)) phone_gb="2";

			
			var url = "kbsavings://kbcert?target_url=/"+appUrl+".do";
			//var url = "kbsavings://kbcert?target_url=https://www.naver.com&urlparam=aabbccc";
			var androidStoreUrl = "https://play.google.com/store/apps/details?id=com.kbsavings.android";
			var iosStoreUrl = "https://itunes.apple.com/kr/app/kbchaghandaechul/id1006543056?mt=8";
			if(phone_gb =="1") {    
			    if(userAgent.match(/Chrome/)) {
			        location.href="intent://kbcert?target_url=/"+appUrl+".do#Intent;scheme=kbsavings;package=com.kbsavings.android;end;";
			        //location.href="intent://kbcert?target_url=https://www.naver.com&urlparam=aabbccc#Intent;scheme=kbsavings;package=com.kbsavings.android;end;";
			    }else{        
			        setTimeout(function(){
			            location.href = androidStoreUrl
			        },1500);
			        var iframe = document.createElement('iframe');
			        iframe.style.visivility = 'hidden';
			        iframe.src = url;
			        documentbody.appendChild(iframe);
			        documentbody.removeChild(iframe); //back호출 시 캐싱될 수 있으므로 제거.
			    }
			//IOS
			}else if(phone_gb =="2") {
				setTimeout(function(){
			    	UI.alert({
		    			text : 'KB저축은행(키위뱅크) 설치 페이지로 이동할까요?',
		    			cancel : true, /* 취소 버튼 있을시 true , 기본은 확인 버튼만 있는 구조 */
		    			cancelTxt : '아니요', /* 취소 버튼 텍스트 변경시 사용 */
		    			confirmTxt : '예', /* 컨펌 버튼 텍스트 변경시 사용 */
		    			onCancel : function(){
		    			},
		    			onConfirm : function(){
		    				location.href =iosStoreUrl;
		    			}
		    		});
			            
			    },500);
			    location.href = url;
			}
		}		
		

		function insDefect(){
			var protocol = window.location.protocol;
			var hostname = window.location.hostname;
			
			var url   = protocol + "//" + hostname;
            openPopupByGet(url + '/mobweb/common/insDefect.do?bgno=2&urlinfo='+$(location).attr("href")+'','insDefect',400,400);
		}
		
		var doubleSubmitFlag = false;
		function doubleSubmitCheck() {
			if(doubleSubmitFlag){
				return doubleSubmitFlag;
			} else {
				doubleSubmitFlag = true;

				return false;
			}
		}
		
		function setEnableSubmitFlag() {
			doubleSubmitFlag = false;
		}
		
/**
 * 이전 화면 이동
 */
function goBackWEBkiwi() {
    
	var iLen = 0;
    
    iLen = arguments.length;
	
    if (iLen > 0) {
    	
    	if ( isNotEmpty( arguments[0] ) ) {
    		
    		//alert("TEST arguments [0] [" + arguments[0] + "] ctx [" + ctx + "]");
    		
    		location.href= ctx + arguments[0];
    		
    		
    	}
    	
    }
    
	history.go(-1);
    
}

function copyLoanShareUrl(){
	var rcmrUrl = location.href;
	console.log(rcmrUrl);
	
	var _url = encodeURI(rcmrUrl); // 'encodeURIComponent' -> 'encodeURI'로 변경 (SR-250725-02672 [모바일Web] 추천인코드 공유하기 개선) 

	console.log(_url);
	try {
		window.Clipboard = (function(win, doc, nav){
			var textArea, copy;
			
			function isIos() {
				return navigator.userAgent.match(/iPhone|iPad/i);
			}
			
			function createTextArea(text) {
				textArea = document.createElement('textArea');
				textArea.value = text;
				document.body.appendChild(textArea);
			}
			
			function selectText() {
				var range, selection;
				
				if (isIos()) {
					range = document.createRange();
					range.selectNodeContents(textArea);
					selection = window.getSelection();
					selection.removeAllRanges();
					textArea.setSelectionRange(0, 999999);
				} else {
					textArea.select();
				}
			}
			
			function copyToClipboard() {
				document.execCommand('copy');
				document.body.removeChild(textArea);
			}
			
			copy = function(text) {
				createTextArea(text);
				selectText();
				copyToClipboard();
			};
			
			return {
				copy : copy
			};
		})(window, document, navigator);
		
		Clipboard.copy(_url);	
		UI.toast('복사 되었습니다.');
	} catch(e) {
		alert(e);
	}
}

$(document).ready(function() {
	try{
		var $formControl = $('.form-control-group');
		var MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
		var myObserver = new MutationObserver(mutationHandler);
		var obsConfig = {
				attributes : true,
				childList : true,
				characterData : true,
				subtree : true,
				attributeOldValue : true
		};
		
		$formControl.each(function(){
			myObserver.observe(this,obsConfig);
		});
		
		
		function mutationHandler(mutationRecords){
			try{
				mutationRecords.forEach(function(mutation){
					if(mutation.type=='childList' && mutation.oldValue == null){
						$(mutation.target).closest('.form-control-group').addClass("valued");
						$(mutation.target).closest('.form-control-group').find('button').removeClass('placeholder');
					}
				});
			}catch(e){
				//암것도안함
			}
		}
		
		
		
		var $uiSelControl = $('.ui-select').find('select');
		var MutationObserverUi = window.MutationObserver || window.WebKitMutationObserver;
		var myObserverUi = new MutationObserverUi(mutationHandlerUi);
		
		$uiSelControl.each(function(){
			myObserverUi.observe(this,obsConfig);
		});
		
		function mutationHandlerUi(mutationRecords){
			try{
				mutationRecords.forEach(function(mutation){
					if(mutation.type=='attributes' && mutation.oldValue == null){
						var $select = $(mutation.target).closest('.ui-select').find('select');
						var $button = $(mutation.target).closest('.ui-select').find('.form-control.select');
						var $buttonTxt = $(mutation.target).closest('.ui-select').find('.value');
						var $formControl = $(mutation.target).closest('.ui-select').closest('.form-control-group');
						
						
						if( !$select.length && $formControl.length ) {
							$button.removeClass('placeholder');
							$formControl.addClass('valued');
							return;
						}
						
						UI._afterRun(function(){
							$select.find('option').each(function(index){
								if( $(this).attr('selected') == 'selected' && $buttonTxt.text() != $(this).text() ){
									$formControl.addClass('valued');
									$button.removeClass('placeholder');
									$buttonTxt.text( $(this).text() );
								}
							});
						},0);
					}
				});
			}catch(e){
				//암것도안함
			}
		}
	}catch(e){
		//암것도안함
		console.log("EEEEEEEEEEEEEEEEEEEEEEEE" + e);
	}
});

// 뒤로가기/캐시 복원 시 자동 실행
window.addEventListener('pageshow', function(){
	UI.removeLoading();
});
//페이지 이탈 시 상태 정리
window.addEventListener('beforeunload', function(){
	UI.removeLoading();
});
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-6FT9Q4HYE0"></script>
<script type="text/javascript">
    try {
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-6FT9Q4HYE0');

		function gaEvent(f_category, f_action, f_label){
			gtag('event',f_action,{
				'event_category':f_category,
				'event_label':f_label
			});
			(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
				(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
					m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
			})(window,document,'script','http://www.google-analytics.com/analytics.js','ga');
		}
	} catch(e) {}
</script>
	<script type="text/javascript" src="https://static.kbdmp.com/ma/kb_v0.01.js"></script><!-- 테스트 : https://static-dev.kbdmp.com/ma/kb_dev_v0.01.js -->
	<script type="text/javascript">
		ma.config('client_id', 'WA-1014');
		ma.config('isCookie', true); // 1사 쿠키 허용 유무 - 기본 true로설정
		ma.init(); // 데이터 수집 요청 
	</script>
<!-- 공유 레이어 -->
	<div class="layer bottom-sheet" id="share">
		<div class="layer-header">
			<h1 class="layer-title">공유하기</h1>
			<button type="button" class="layer-close cancel">
				<span class="sr-only">레이어 닫기</span>
			</button>
		</div>
		<div class="layer-contents type2">
				<div class="favorite-wrap center">
					<button type="button" class="send-kakao" onclick="sandLoanKakaoLink();UI.layerPopClose('#share');">
						<span class="">카카오톡</span>
					</button>
					<button type="button" class="send-sms" onclick="sendLoanSmsLink();UI.layerPopClose('#share');">
						<span class="">SMS</span>
					</button>
					<button type="button" class="send-more" onclick="copyLoanShareUrl();UI.layerPopClose('#share');">
						<span class="">더보기</span>
					</button>
			</div>
		</div>
	<!--<div class="share-list">
		<button type="button" class="send-kakao" onclick="sendKakaoLink();UI.layerPopClose('#share');">
            <span class="">카카오톡</span>
        </button>
        <button type="button" class="send-sms" onclick="sendSmsLink();UI.layerPopClose('#share');">
            <span class="">SMS</span>
        </button>
        <button type="button" class="send-more" onclick="copyShareUrlCheck();UI.layerPopClose('#share');">
            <span class="">더보기</span>
        </button>
	    <button type="button" class="share-ico kakao" onclick="sharedsns('twitter');UI.layerPopClose('#share');">
			<span class="sr-only">트위터</span>
		</button> 
		<button type="button" class="share-ico kakao" onclick="KakaoLink();UI.layerPopClose('#share');">
			<span class="sr-only">카카오톡</span>
		</button>
		<button type="button" class="share-ico facebook" onclick="sharedsns('facebook');UI.layerPopClose('#share');">
			<span class="sr-only">페이스북</span>
		</button>
		<button type="button" class="share-ico etc" onclick="sharedsns('blog');UI.layerPopClose('#share');">
			<span class="sr-only">기타</span>
		</button>
		<button type="button" class="share-ico kakao" onclick="sharedsns('blog');UI.layerPopClose('#share');">
			<span class="sr-only">블로그</span>
		</button> -->
	</div>
</div>

<input type="hidden" id="kakaoLinkBtnReal" />

				<!-- <section class="pd-all">
                    <div class="page-btns">
                        <button type="button" class="btn-sm-func3" onclick="UI.layerPop('#anti-pop-up');">본인확인-종료안내</button>
                    </div>
				</section> -->
				
<!-- layer popup -->
	<section class="layer bottom-sheet" id="anti-pop-up">
		<div class="layer-header">
			<h1 class="layer-title sr-only">종료안내</h1>
			<button type="button" class="layer-close">
				<span class="sr-only">레이어 닫기</span>
			</button>
		</div>
        <!-- 팝업 내용 -->
		<div class="layer-contents">
            <div class="request-state ager1-s ta-c">
				<i class="ico"></i>
				<!-- 25.09.19 문구수정 -->
				<p class="head-copy">본인확인을 진행중이예요<br>지금 멈추면 다시 신분증 인증부터<br>다시 진행해야 해요</p>
                <!-- 25.09.12 mt12를 mt8로 변경-->
				<div class="light mt8">본인인증을 종료하시겠어요?</div>
			</div>
            <div class="layer-btns">
                <!-- <button type="button" class="btn-lg-func1">이전 단계로 가기</button>	 2025-10-29 버튼명 변경 -->
                <button type="button" class="btn-lg-func1" onclick="javascript:location.href=('');">이전 단계로 가기</button>	<!-- 2025-10-29 버튼명 변경 -->
                <!-- <button type="button" class="btn-lg-primary">계속하기</button> -->
                <button type="button" class="btn-lg-primary" onclick="UI.layerPopClose('#anti-pop-up');">계속하기</button>
            </div>
		</div>
	</section>
   
   <!-- header에 표시-->




<header class="fixed">
	<div class="inner-wrap">
		<h1 class="sr-only">카드안내/신청</h1>
		<h2 class="page-title" id="pa2">카드안내/신청</h2>
		<!-- back버튼 노출시 -->
		<button type="button" class="btn-back" onclick="confirmBackPage();" >
			<span class="sr-only">뒤로 이동</span>
		</button>
	


<script type="text/javascript" src="/mobweb/js_kiwi/common.js"></script>
<script>
function goPage(url){		
	location.href = ctx + "/" + url + ".do";
}

	function openChatBotPop(){
		if(iosCheck()){
			$("#deviceGb").val("1");
			$("#deviceOs").val("IOS");
		}else{
			$("#deviceGb").val("2");
			$("#deviceOs").val("Android");
		}
		const title = "chatbotPopup";
		const width = 450;
		const height = 600;
		const leftMargin = (window.screen.width / 2) - (width / 2) + "px";
		const topMargin = (window.screen.height / 2) - (height / 2) + "px";
      
		const formObj = document.querySelector('#chatbotForm');
		var popupChecked = window.open("", title);
    
		formObj.target = title;
		formObj.method = "post";
		formObj.submit();   
    
		if(popupChecked == null){
			//kbc.alert('팝업차단설정이 되어있습니다. 브라우져 설정에서 팝업차단을 풀어주세요.');
		}
	}
	
	let scrollTimeout;
    function goMenuScroll(menuId) {
    	var userAgent = navigator.userAgent.toLowerCase();   	
    	if (userAgent.indexOf('whale') > -1) {
    		UI.isScrollByClick = true;

    		//var activeIndex = menuId + 1;
    		var $tabWrap = $('.fullmenu.tab-menu.type2');
    		var currentScrollLeft = $tabWrap.scrollLeft(); // 가로 위치 저장

            $('.fullmenu.tab-menu.type2 ul li').removeClass('active'); 
            $('.fullmenu.tab-menu.type2 ul li').eq(menuId).addClass('active');
            
            // 실제 스크롤 컨테이너
            var $scrollEl = $('.layer-contents.up');
            // 이동할 타겟
            var $targetEl = $('#menu' + menuId);
            
            if($scrollEl.length && $targetEl.length){
            	
            	//상단 고정 영역 높이
            	var fixedTopHeight = $('header').outerHeight() || 0;

            	var targetTop = $targetEl.offset().top - $scrollEl.offset().top + $scrollEl.scrollTop() - fixedTopHeight;
            	
            	$scrollEl.stop().animate(
            		{ scrollTop : targetTop },
            		600
            	);
            	
            	clearTimeout(scrollTimeout);

                scrollTimeout = setTimeout(function(){
                	$tabWrap.scrollLeft(currentScrollLeft);
                    UI.isScrollByClick = false;
                }, 1500);
            }
    	} else {
    		UI.isScrollByClick = true;

            $('.fullmenu.tab-menu.type2 ul li').removeClass('active'); 
            $('.fullmenu.tab-menu.type2 ul li').eq(menuId).addClass('active');

            var targetEl = $('nav#menu' + menuId + '.menu-lists');
            if(targetEl.length){
                targetEl[0].scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                clearTimeout(scrollTimeout);

                scrollTimeout = setTimeout(function(){
                    UI.isScrollByClick = false;
                }, 1000);
            }
    	}       
    }
</script>
<button type="button" class="btn-nav" onclick="UI.layerPop('#fullMenu');"><span class="sr-only">메뉴</span></button>
<section class="layer fullmenu web active" id="fullMenu">
	<div class="layer-header">
		<div class="layer-title">
			<h1 class="sr-only">전체메뉴</h1>
			<button type="button" class="layer-logo">
				<span class="sr-only">KB 저축은행</span>
			</button>
		</div>
		<button type="button" class="layer-home" onclick="location.href='/mobweb/main.do'">
			<span class="sr-only">홈</span>
		</button>
		<button type="button" class="layer-close cancel">
			<span class="sr-only">레이어 닫기</span>
		</button>
	</div>
	<div class="layer-contents">
		<!-- 앱다운로드 배너 -->
		<div class="app-download">
			<a href="/mobweb/customer/appdown.do"> 
				<span class="app-ico">
					<i class="ico"></i>
				</span>
				<div>
					<span class="txt-tit">출첵하고 포인트 받아가세요</span>
					<!-- TODO : 앱다운로드 연결 -->
					<span class="text-13 light">KB저축은행 앱 다운로드 바로가기</span>
				</div>
			</a>
		</div>   
         
		<!-- 추천메뉴 영역 -->
		<div class="special-menu">
			<h2 class="sr-only">추천메뉴</h2>
			<!-- 2025-10-21 아이콘 수정 //-->
			<a href="/mobweb/kiwiloan/LonTotalInqIntro.do"><img class="ico" src="/mobweb/images_kiwi/main/img-search.png" /> 통합한도조회</a>
			<a href="/mobweb/kiwiintro/guide_brnc_info.do"><img class="ico" src="/mobweb/images_kiwi/main/img-kb-office.png" /> 영업점안내</a>
			<a href="/mobweb/kiwicustomer/cust_view.do"><img class="ico" src="/mobweb/images_kiwi/main/img-counsel.png" /> 상담예약</a>
			<a href="/mobweb/kiwisavings/liivSavingsProd2.do?KIWI_GOODS_CODE=kiwiPAK"><img class="ico" src="/mobweb/images_kiwi/main/img-kiwi.png" /> kiwi팡팡통장</a>
			<!--// 2025-10-21 아이콘 수정 -->
		</div>

		<hr class="divider" />

		<div class="ui-tab">
			<!-- 탭메뉴 -->
			<div class="tab-menu type2">
				<ul>
					<li class="active">
						<button type="button" aria-controls="menu01" onclick="goMenuScroll('01');">
							<span>대출</span>
						</button>
					</li>
					<li class="">
						<button type="button" aria-controls="menu02" onclick="goMenuScroll('02');">
							<span>예금</span>
						</button>
					</li>
					<li class="">
						<button type="button" aria-controls="menu03" onclick="goMenuScroll('03');">
							<span>적금</span>
						</button>
					</li>
					<li class="">
						<button type="button" aria-controls="menu04" onclick="goMenuScroll('04');">
							<span>입출금</span>
						</button>
					</li>
					<li class="">
						<button type="button" aria-controls="menu05" onclick="goMenuScroll('05');">
							<span>카드</span>
						</button>
					</li>
					<li class="">
						<button type="button" aria-controls="menu06" onclick="goMenuScroll('06');">
							<span>혜택</span>
						</button>
					</li>
					<li class="">
						<button type="button" aria-controls="menu07" onclick="goMenuScroll('07');">
							<span>고객센터</span>
						</button>
					</li>
				</ul>
			</div>

			<!-- 대출 -->
			<nav class="menu-lists" id="menu01">
				<h2><a href="/mobweb/kiwiloan/LON100000M.do"><img class="ico" src="/mobweb/images_kiwi/main/icon-loan.svg" alt="" />대출</a></h2>      <!-- 2025.10.23 아이콘 변경 -->
				<ul>
					<!-- SR-260521-01937 [WEB] 생활안정자금대출 신상품 개발 요청 Start -->
                    <li>
                        <div class="divider"><span>중금리 생활안정대출</span></div>
                            <ul>
			                    <li>
			                        <a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=1380&entryType=02">KB저축은행 중금리 생활안정대출</a>
			                    </li>
                            </ul>
                    </li>
					<!-- SR-260521-01937 [WEB] 생활안정자금대출 신상품 개발 요청 End -->
				    <!-- SR-260306-00931 [web]kiwi 다이렉트 채널 전용 상품 개발 요청 Start -->
                    <li>
                        <div class="divider"><span>다이렉트 대출</span></div>
                            <ul>
			                    <li>
			                        <a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=1378&entryType=02">KB다이렉트(신용대출)</a>
			                    </li>
			                    <li>
			                        <a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=1379&entryType=02">KB다이렉트(비상금대출)</a>
			                    </li>
                            </ul>
                    </li>
                    <li>
                        <div class="divider"><span>신용대출</span></div>
                            <ul>
			                    <li>
			                        <a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=122&entryType=02">kiwi신용대출</a>
			                    </li>
			                    <li>
			                        <a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=121&entryType=02">kiwi전환대출</a>
			                    </li>
			                    <li>
			                        <a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=970&entryType=02">kiwi마이홈신용대출</a>
			                    </li>
			                    <li>
			                        <a href="/mobweb/kiwiloan/LON400011M.do?lonGdsNo=506&type=2">KB고객우대신용대출</a>
			                    </li>
			                    <li>
			                        <a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=120&entryType=02">kiwi비상금대출</a>
			                    </li>
			                    <li>
			                        <a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=971&entryType=02">kiwi여성비상금대출</a>
			                    </li>
			                    <li>
			                        <a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=69&entryType=02">사잇돌2대출(표준형)</a>
			                    </li>
                            </ul>
                    </li>
                    <!-- SR-260306-00931 [web]kiwi 다이렉트 채널 전용 상품 개발 요청 End -->
					<li>
						<div class="divider"><span>햇살론</span></div>
							<ul>
								<!-- 
								<li><a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNoE=57&entryType=02">(온라인)햇살론 생계자금</a></li>
								<li><a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=64&entryType=02">햇살론대환자금</a></li>
								<li><a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=66&entryType=02">햇살론운영자금</a></li>
								--> 
								<!-- [SR-251002-03761] [웹] 햇살론통합(신상품) 프로세스 개발 요청의 건 START -->
								<li><a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNoE=57&entryType=02">햇살론일반보증</a></li>
								<!-- 
								<li><a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=66&entryType=02">햇살론운영자금</a></li>
								<li><a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=64&entryType=02">햇살론대환자금</a></li>
								 -->
								<li><a href="/mobweb/kiwiloan/LON400010M.do?lonGdsNo=1230&entryType=02">햇살론특례보증</a></li>
								<!-- [SR-251002-03761] [웹] 햇살론통합(신상품) 프로세스 개발 요청의 건 END -->
							</ul>
					</li>
					<!--  SR-260316-01083 (모바일웹) 외국인대출_kiwi Dream Loan_판매종료 요청의 건 START -->
					
					<!--  SR-260316-01083 (모바일웹) 외국인대출_kiwi Dream Loan_판매종료 요청의 건 END -->
					<li>
						<div class="divider"><span>기업/PF대출</span></div>
						<ul>
							<li><a href="/mobweb/kiwiloan/LON400011M.do?lonGdsNo=391&type=2">부동산담보대출</a></li>
							<li><a href="/mobweb/kiwiloan/LON400011M.do?lonGdsNo=520&type=2">사업자아파트담보대출</a></li>
							<li><a href="/mobweb/kiwiloan/LON400011M.do?lonGdsNo=529&type=2">경락잔금대출</a></li>
							<li><a href="/mobweb/kiwiloan/LON400011M.do?lonGdsNo=530&type=2">건축자금대출</a></li>
							<li><a href="/mobweb/kiwiloan/LON400011M.do?lonGdsNo=531&type=2">PF대출</a></li>
							<li><a href="/mobweb/kiwiloan/LON400011M.do?lonGdsNo=89&type=2">집단(중도금)대출</a></li>
							<li><a href="/mobweb/kiwiloan/LON400011M.do?lonGdsNo=533&type=2">자산유동화(ABL)대출</a></li>
							<li><a href="/mobweb/kiwiloan/LON400011M.do?lonGdsNo=534&type=2">담보부NPL대출</a></li>
							<li><a href="/mobweb/kiwiloan/LON400011M.do?lonGdsNo=535&type=2">주식담보대출</a></li>
						</ul>
					</li>
				</ul>
			</nav>
	
			<!-- 예금 -->
			<nav class="menu-lists" id="menu02">
				<h2><span class="s-tit"><img class="ico" src="/mobweb/images_kiwi/main/icon-deposit.svg" alt="" />예금</span></h2>      <!-- 2025.10.23 아이콘 변경 -->
				<ul>
					<li>
						<a href="/mobweb/kiwisavings/kiwiRotarySavings2Prod.do">플러스회전식정기예금</a>
					</li>
                     <li>
                         <a href="/mobweb/kiwisavings/eplusSavingsProd.do">KB e-plus정기예금</a>
                     </li>
					<li>
						<a href="/mobweb/kiwisavings/kiwi369RotarySavingsProd.do">KB369회전식 정기예금</a>
					</li>
                     <li>
                         <a href="/mobweb/savings/savingInfo.do?SAVINGS_GOODS_CODE=3">자유적립예금</a>
                     </li>
				</ul>
			</nav>
	
			<!-- 적금 -->
			<nav class="menu-lists" id="menu03">
				<h2><span class="s-tit"><img class="ico" src="/mobweb/images_kiwi/main/icon-savings.svg" alt="" />적금</span></h2>      <!-- 2025.10.23 아이콘 변경 -->
				<ul>
					
					<li>
						<a href="/mobweb/kiwisavings/firstKiwiSavingsProd.do">첫kiwi적금</a>
					</li>
					<li>
						<a href="/mobweb/kiwisavings/kindEplusSavingsProd.do">KB착한e-plus정기적금</a>
					</li>
					<!-- SR-260311-01008 예/적금 상품공시 목록 삭제 요청 START -->
	 				
					<!-- SR-260311-01008 예/적금 상품공시 목록 삭제 요청 END -->					
					<!-- SR-260602-02076 [모바일웹] 플러스kiwi적금 모바일웹 예적금 상품공시 목록 삭제 요청 START -->
					
					<!-- SR-260602-02076 [모바일웹] 플러스kiwi적금 모바일웹 예적금 상품공시 목록 삭제 요청 END -->
					<li>
						<a href="/mobweb/kiwisavings/installmentSavingsProd.do">KB일반e-plus정기적금</a>
					</li>
					<li>
						<a href="/mobweb/savings/savingInfo.do?SAVINGS_GOODS_CODE=10">KB착한누리적금</a>
	 				</li>
				</ul>
			</nav>
	
			<!-- 입출금 -->
			<nav class="menu-lists" id="menu04">
				<h2><span class="s-tit"><img class="ico" src="/mobweb/images_kiwi/main/icon-checking.svg" alt="" />입출금</span></h2>      <!-- 2025.10.23 아이콘 변경 -->
				<ul>
					
					<li>
						<a href="/mobweb/kiwisavings/liivSavingsProd2.do?KIWI_GOODS_CODE=kiwiPAK">kiwi팡팡통장</a>
					</li>
					<li>
						<a href="/mobweb/kiwisavings/liivSavingsProd2.do?KIWI_GOODS_CODE=kiwiNOR">kiwi입출금통장</a>
					</li>
				</ul>
			</nav>
	
			<!-- 카드 -->
			<nav class="menu-lists" id="menu05">
				<h2><span class="s-tit"><img class="ico" src="/mobweb/images_kiwi/main/icon-card.svg" alt="" />카드</span></h2>      <!-- 2025.10.23 아이콘 변경 -->
				<ul>
					<li>
						<a href="/mobweb/kiwicard/CAR100000M.do">팡팡KB체크카드</a>
					</li>
				</ul>
			</nav>
	
			<!-- 혜택 -->
			<nav class="menu-lists" id="menu06">
				<h2><span class="s-tit"><img class="ico" src="/mobweb/images_kiwi/main/icon-benefit.svg" alt="" />혜택</span></h2>      <!-- 2025.10.23 아이콘 변경 -->
				<ul>
					<li>
						<a href="/mobweb/kiwiintro/membership.do">kiwi멤버십</a>
					</li>
					<li>
						<a href="/mobweb/kiwicustomer/event_list.do">이벤트</a>
					</li>
				</ul>
			</nav>
	
			<!-- 고객센터 -->
			<nav class="menu-lists" id="menu07">
				<h2><span class="s-tit"><img class="ico" src="/mobweb/images_kiwi/main/icon-cscenter.svg" alt="" />고객센터</span></h2>      <!-- 2025.10.23 아이콘 변경 -->
				<ul>
					<li>
						<a href="/mobweb/kiwicustomer/rept_qust.do">자주하는 질문</a>
					</li>
					<li>
						<a href="/mobweb/kiwicustomer/notice_list.do">공지사항/새소식/금융팁</a>
						<ul>
							<li><a href="/mobweb/kiwicustomer/notice_list.do">공지사항</a></li>
							<li><a href="/mobweb/kiwicustomer/news_list.do">새소식</a></li>
							<li><a href="/mobweb/kiwicustomer/bankTip_list.do">금융팁</a></li>
						</ul>
					</li>
					<li>
						<a href="/mobweb/kiwicustomer/tms_view.do">약관자료실</a>
					</li>
					<li>
						<a href="/mobweb/kiwiintro/privacy_policy.do">개인정보보호정책</a>
						<ul>
							<li><a href="https://www.kbsavings.com/websquare/websquare.jsp?w2xPath=/jsp/consumerCenter/myPage/personInfoPolicy.xml">개인정보처리방침</a></li>
							<li><a href="https://www.kbsavings.com/websquare/websquare.jsp?w2xPath=/jsp/consumerCenter/myPage/personInfoProtectPolicy.xml&OFF_CODE=2502">신용정보활용체제</a></li>
							<li><a href="https://www.kbsavings.com/websquare/websquare.jsp?w2xPath=/jsp/consumerCenter/myPage/personInfoProtectPolicy.xml&OFF_CODE=2503">(그룹)고객정보취급방침</a></li>
							<li><a href="https://www.kbsavings.com/websquare/websquare.jsp?w2xPath=/jsp/consumerCenter/myPage/personInfoProtectPolicy.xml&OFF_CODE=2504">고정형 영상정보처리기기 운영관리지침</a></li>
						</ul>
					</li>
<!--
					<li>
						<a href="/mobweb/kiwicustomer/cust_view.do">상담예약</a>
					</li>
-->
					<li>
						<a href="/mobweb/kiwicustomer/prt_fnce_prd_regt.do">보호금융상품등록부</a>
					</li>
					<li>
						<span class="s-tit">이용안내</span>
						<ul>
							<li><a href="/mobweb/kiwiintro/guide_brnc_info.do">영업점안내</a></li>
							<li><a href="/mobweb/kiwiintro/guide_use_time.do">이용시간안내</a></li>
							<li><a href="/mobweb/kiwiintro/guide_use_pee.do">수수료안내</a></li>
							<li><a href="/mobweb/kiwiintro/guide_trns_limt.do">이체한도안내</a></li>
						</ul>
					</li>
					<li>
						<a href="#">은행소개</a>
						<ul>
							<li><a href="/mobweb/kiwiintro/kiwiceo.do">CEO인사말</a></li>
							<li><a href="/mobweb/kiwiintro/management_phil.do">경영이념</a></li>
						</ul>
					</li>
				</ul>
			</nav>
		</div>
	
		<hr class="divider" />
	
		<!-- 소셜 서비스 -->
		<div class="social-service">
			<h2>KB저축은행 소셜 서비스</h2>
			<div class="favorite-wrap">
				<button type="button" class="send-blog" onclick="location.href='https://m.blog.naver.com/kbsavingsbk?tab=1'">
					<span class="">네이버<br/>블로그</span>
				</button>
				<button type="button" class="send-insta" onclick="location.href='https://www.instagram.com/kb.savings_bank'">
					<span class="">인스타<br/>그램</span>
				</button>
				<button type="button" class="send-facebook" onclick="location.href='https://www.facebook.com/KBSavingsBankOfficial/'">
					<span class="">페이스북</span>
				</button>
				<button type="button" class="send-youtube" onclick="location.href='https://www.youtube.com/@KB-oy2ro'">
					<span class="">유튜브</span>
				</button>
				<button type="button" class="send-kakao" onclick="location.href='https://pf.kakao.com/_Vhxfexb'">
					<span class="">카카오톡</span>
				</button>
			</div>
		</div>
	</div>

	<form id="chatbotForm" action="https://dchatbot.kbonefcc.com:6443/kbchatbot/chatSavings/mnChatbotWindow_M.do" target="chatbotPopup" method="post"> 
		<input type = "hidden"	id = "userName"			name = "userName"		value = ""/>
		<input type = "hidden"	id = "ciNo"				name = "ciNo"			value = ""/>
		<input type = "hidden"	id = "afitGroupDstCd"	name = "afitGroupDstCd"	value = "KM0"/>
		<input type = "hidden"	id = "channelId"		name = "channelId"		value = "02"/>
		<input type = "hidden"	id = "userId"			name = "userId"			value = ""/>
		<input type = "hidden"	id = "deviceGb"			name = "deviceGb"		value = ""/>
		<input type = "hidden"	id = "deviceOs"			name = "deviceOs"		value = ""/>
		<input type = "hidden"	id = "isLogin"			name = "isLogin"		value = "false"/>
		<input type = "hidden"	id = "LoginType"		name = "LoginType"		value = "00"/> <!-- 00 : 비로그인   01 : ID/PW  02 : 공동인증서   03 : 국민인증서 -->
	</form>
</section>
	</div>
</header>

<script language="javascript">
	function confirmBackPage() {
		if ('Y' === 'Y' || existNull('/mobweb/kiwicard/CAR100000M.do')) {
			location.href = ctx + '/main.do';
		} else {
			UI.layerPop('#backPage');
		}
	}
	function goBackProd() {
		location.href = '/mobweb/kiwicard/CAR100000M.do' == '' ? ctx + '/main.do' : '/mobweb/kiwicard/CAR100000M.do';
	}
</script>

<body>
	<form id="frmStep" method="get">
		<input type="hidden" id="authType" name="authType" value="" />
	</form>
	<!-- layer popup -->
	<section class="layer bottom-sheet" id="backPage">
		<div class="layer-header">
			<h1 class="layer-title sr-only">종료안내</h1>
			<button type="button" class="layer-close">
				<span class="sr-only">레이어 닫기</span>
			</button>
		</div>
		<!-- 팝업 내용 -->
		<div class="layer-contents">
			<div class="request-state ager1-s ta-c">
				<i class="ico"></i>
				<!-- 25.09.19 문구수정 -->
				<p class="head-copy">
					상품 개설이 완료되지 않았습니다.<br/>
					개설을 중단하시겠습니까?
				</p>
				<!-- 25.09.12 mt12를 mt8로 변경-->
				<!-- <div class="light mt8">이전 단계로 이동 하시겠어요?</div> -->
			</div>
			<div class="layer-btns">
				<button type="button" class="btn-lg-func1" onclick="goBackProd();">중단하기</button>
				<button type="button" class="btn-lg-primary" onclick="UI.layerPopClose('#backPage');">계속하기</button>
			</div>
		</div>
	</section>
</body>






<script type="text/javascript">

$(document).ready(function() {
	var $slideItems = $('.benefits-list li');
	var $listBtn = $slideItems.find('button');

	$listBtn.on('click', function(){
		var listIndex = $(this).parent('li').index();
		//console.log(listIndex);
		UI.layerPop('#send-sms', swiper.slideTo(listIndex));
	})

	var swiper = new Swiper('.benefit-swiper', {
		slidesPerView: '1',
		spaceBetween: 0,
		slidesOffsetBefore: 0,
		slidesOffsetAfter: 0,
		observeParents: true,
		observer: true,
		pagination: {
			el: '.swiper-pagination',
			// dynamicBullets: true
		},
		on: {
			slideChange: function () {
				$('.card-benefit-info').removeClass('visible').addClass('hidden');
				$('.card-benefit-info').eq(this.activeIndex).removeClass('hidden').addClass('visible');
				
			}
		}
	})	
});

var serverMod = "";
 serverMod = "REAL";

	// 신청하기
	function goNext() {
		//SR-260521-01928 (웹)체크카드 발급신청 프로세스 변경  START
		//카드사 페이지 이동하도록 변경  결정26.6.1
    	window.location.href = 'https://m.kbcard.com/c/09582';
        /* var data = {
	            "yesUrl" : "kiwisavingsDeposit/savingsCheckInfo.do",
                "noUrl" : "",
                "backwardUrl" : "CAR100000M.do",
                "etcValue1" : "kiwicard/CAR100011M.do",
                "prodTypeGb": "05"
        } */
        
		/* SR-250704-02362 본인확인 프로세스 개선 
		신규 본인확인 페이지(SEU900110M)로 연결
		*/
        //submitFormUrl(data, ctx + "/SEU900110M.do", 'post');
		//SR-260521-01928 (웹)체크카드 발급신청 프로세스 변경  END
	}
/*
	// 혜택 클릭
	function benfPopOpen( svcGb ){
	    if( svcGb == null || svcGb == "" || svcGb == undefined ) return;
	    var headerHtml = "";
	    var bodyHtml = "";
	    
	    // bodyTxt 공통 문구 세팅
	    bodyHtml += "<ul class='list-bullet-dot mt10'>";
	    
	    // Open:오픈마켓, OpenKbPay:오픈마켓KbPay, Coffee:커피, BigMart:대형마트, OTT:OTT, Movie:영화, Family:패밀리레스토랑, CmncAuto:통신자동납부, Park:놀이공원
	    switch(svcGb){
	        case "Open":
	            headerHtml += "<p>[오픈마켓] 11번가, G마켓, SSG.COM 10% 환급할인</p>";
	            headerHtml += "<div class='top-btn'><button type='button' class='pl10' onclick='' style='color:#ffd338;'>&lt</button>";
	            headerHtml += "<button type='button' class='pr10' onclick='benfPopOpen(\"OpenKbPay\")'>&gt</button></div>";
	            headerHtml += "<div><p>1 / 9</p></div>";
	            $("#amtDcTxt").text("할인율");
	            $("#bodyTable #gubun").text("11번가, G마켓, SSG.COM");
	            $("#bodyTable #amtDc").text("10%");
	            $("#bodyTable #limitDc").text("7천원");
	            break;
	        case "OpenKbPay":
	            headerHtml += "<p>[오픈마켓] KB Pay 결제 시 11번가, G마켓, SSG.COM 10% 추가 환급할인</p>";
	            headerHtml += "<div class='top-btn'><button type='button' class='pl10' onclick='benfPopOpen(\"Open\")'>&lt</button>";
	            headerHtml += "<button type='button' class='pr10' onclick='benfPopOpen(\"Coffee\")'>&gt</button></div>";
	            headerHtml += "<div><p>2 / 9</p></div>";
	            $("#amtDcTxt").text("할인율");
	            $("#bodyTable #gubun").text("[11번가, G마켓, SSG.COM] KB Pay 결제 시");
	            $("#bodyTable #amtDc").text("10%");
	            $("#bodyTable #limitDc").text("3천원");
	            break;
	        case "Coffee":
	            headerHtml += "<p>[커피] 스타벅스(사이렌오더 포함), 커피빈(퍼플오더 제외) 10% 환급할인</p>";
	            headerHtml += "<div class='top-btn'><button type='button' class='pl10' onclick='benfPopOpen(\"OpenKbPay\")'>&lt</button>";
	            headerHtml += "<button type='button' class='pr10' onclick='benfPopOpen(\"BigMart\")'>&gt</button></div>";
	            headerHtml += "<div><p>3 / 9</p></div>";
	            $("#amtDcTxt").text("할인율");
	            $("#bodyTable #gubun").text("스타벅스(사이렌오더 포함), 커피빈(퍼플오더 제외)");
	            $("#bodyTable #amtDc").text("10%");
	            $("#bodyTable #limitDc").text("4천원");
	            break;
	        case "BigMart":
	            headerHtml += "<p>[대형마트] 이마트, 롯데마트, 홈플러스 10% 환급할인</p>";
	            headerHtml += "<div class='top-btn'><button type='button' class='pl10' onclick='benfPopOpen(\"Coffee\")'>&lt</button>";
	            headerHtml += "<button type='button' class='pr10' onclick='benfPopOpen(\"OTT\")'>&gt</button></div>";
	            headerHtml += "<div><p>4 / 9</p></div>";
	            $("#amtDcTxt").text("할인율");
	            $("#bodyTable #gubun").text("이마트, 롯데마트, 홈플러스");
	            $("#bodyTable #amtDc").text("10%");
	            $("#bodyTable #limitDc").text("3천원");
	            break;
	        case "OTT":
	            headerHtml += "<p>[OTT구독] 넷플릭스, 유튜브 20% 환급할인</p>";
	            headerHtml += "<div class='top-btn'><button type='button' class='pl10' onclick='benfPopOpen(\"BigMart\")'>&lt</button>";
	            headerHtml += "<button type='button' class='pr10' onclick='benfPopOpen(\"Movie\")'>&gt</button></div>";
	            headerHtml += "<div><p>5 / 9</p></div>";
	            bodyHtml   += "<li>이용금액 건당 1만원 이상 이용 시 적용</li>";
	            bodyHtml   += "<li>유튜브 프리미엄, 넷플릭스 공식 홈페이지/앱을 통한 정기결제 시 할인</li>";
	            $("#amtDcTxt").text("할인율");
	            $("#bodyTable #gubun").text("넷플릭스, 유튜브");
	            $("#bodyTable #amtDc").text("20%");
	            $("#bodyTable #limitDc").text("2천원");
	            break;
	        case "Movie":
	            headerHtml += "<p>[영화] CGV, 롯데시네마, 메가박스 최대 8,000원 환급할인</p>";
	            headerHtml += "<div class='top-btn'><button type='button' class='pl10' onclick='benfPopOpen(\"OTT\")'>&lt</button>";
	            headerHtml += "<button type='button' class='pr10' onclick='benfPopOpen(\"Family\")'>&gt</button></div>";
	            headerHtml += "<div><p>6 / 9</p></div>";
	            bodyHtml   += "<li>이용금액 건당 1만원 이상 이용 시 제공</li>";
	            bodyHtml   += "<li>월 할인횟수 2회</li>";
	            bodyHtml   += "<li>매점∙관람권∙상품권 및 예매대행 사이트 이용 제외</li>";
	            $("#amtDcTxt").text("할인금액");
	            $("#bodyTable #gubun").text("CGV, 롯데시네마, 메가박스");
	            $("#bodyTable #amtDc").text("건당 4천원");
	            $("#bodyTable #limitDc").text("8천원");
	            break;
	        case "Family":
	            headerHtml += "<p>[패밀리레스토랑] 패밀리레스토랑 업종 4,000원 환급할인</p>";
	            headerHtml += "<div class='top-btn'><button type='button' class='pl10' onclick='benfPopOpen(\"Movie\")'>&lt</button>";
	            headerHtml += "<button type='button' class='pr10' onclick='benfPopOpen(\"CmncAuto\")'>&gt</button></div>";
	            headerHtml += "<div><p>7 / 9</p></div>";
	            bodyHtml   += "<li>이용금액 건당 5만원 이상 이용 시 제공</li>";
	            bodyHtml   += "<li>월 할인횟수 1회</li>";
	            $("#amtDcTxt").text("할인금액");
	            $("#bodyTable #gubun").text("패밀리레스토랑 업종");
	            $("#bodyTable #amtDc").text("건당 4천원");
	            $("#bodyTable #limitDc").text("4천원");
	            break;
	        case "CmncAuto":
	            headerHtml += "<p>[통신 자동납부]SKT, KT, LG U+, Liiv M 3,000원 환급할인";
	            headerHtml += "<div class='top-btn'><button type='button' class='pl10' onclick='benfPopOpen(\"Family\")'>&lt</button>";
	            headerHtml += "<button type='button' class='pr10' onclick='benfPopOpen(\"Park\")'>&gt</button></div>";
	            headerHtml += "<div><p>8 / 9</p></div>";
	            bodyHtml += "<li>이용금액 건당 5만원 이상 이용 시 제공</li>";
	            bodyHtml += "<li>월 할인횟수 1회</li>";
	            $("#amtDcTxt").text("할인금액");
	            $("#bodyTable #gubun").text("SKT, KT, LG U+, Liiv M");
	            $("#bodyTable #amtDc").text("건당 3천원");
	            $("#bodyTable #limitDc").text("3천원");
	            break;
	        case "Park":
	            headerHtml += "<p>[놀이공원] 에버랜드, 롯데월드 15,000원 환급할인</p>";
	            headerHtml += "<div class='top-btn'><button type='button' class='pl10' onclick='benfPopOpen(\"CmncAuto\")'>&lt</button>";
	            headerHtml += "<button type='button' class='pr10' onclick='UI.layerPopClose(\"#benfPop\")'>&gt</button></div>";
	            headerHtml += "<div><p>9 / 9</p></div>";
	            bodyHtml   += "<li>이용금액 건당 3만원 이상 이용 시 제공</li>";
	            bodyHtml   += "<li>월 할인횟수 1회</li>";
	            bodyHtml   += "<li>티켓 요금(입장권, 이용권) 결제 시 할인 제공하며, 상품권 구매 및 매점 이용분 할인 불가</li>";
	            $("#amtDcTxt").text("할인금액");
	            $("#bodyTable #gubun").text("에버랜드, 롯데월드");
	            $("#bodyTable #amtDc").text("건당 1만5천원");
	            $("#bodyTable #limitDc").text("1만5천원");
	            break;
	    }
	    
	    // bodyTxt 공통 문구 세팅
	    bodyHtml += "<li>전월 이용실적 조건: KB저축은행 팡팡 KB체크카드로 전월 실적 20만원 이상 시 제공</li>";
	    bodyHtml += "<li>본인 회원기준으로 전표매입순서대로 월간 통합할인한도 내에서 혜택 제공됩니다.</li>";
	    bodyHtml += "</ul>";
	    
	    $("#headerTxt").html(headerHtml);
	    $("#bodyTxt").html(bodyHtml);
	    UI.layerPop("#benfPop");
	}
*/

	function benfPopOpen( svcGb ){
		console.log("svcGb",svcGb);
		UI.layerPop("#send-sms");
	}

    //약관다운로드를 위한 처리
    function downPDFtoTMS(){    
        var pData = "";
        if( serverMod == "DEV" || serverMod == "TEST" ) { // 개발
            pData = "tmsId=2046";
        } else { // 운영
            pData = "tmsId=1436";
        }
        UI.addLoading();
        E2EWrapper.ajax({       
            type            : 'POST'        
            , async         : true      
            , url           : ctx + '/kiwicard/carGetTmsDown.do'     
            , data          : pData     
            , dataType      : "json"        
            , contentType   : "application/x-www-form-urlencoded;charset=UTF-8"     
            , success : function(sResult) {
            	UI.removeLoading();

                for(var i=0; sResult.listMap.length > i; i++){
                    var dwnpath = sResult.listMap[0].TMS_FILE_ADDR;
                    var dwnFile = sResult.listMap[0].TMS_FILE_NM;
                    var folder  = dwnFile.replace(".pdf","");
                    var fullPath = ctx + dwnpath + folder + "/" + dwnFile;
                    
                    window.location.assign(fullPath);
                    break;
                }
            }
            , error : function(data, stateus, err){ 
            	UI.removeLoading();
                AppAlert("시스템 또는 네트워크 오류로 \n 인증에 실패하였습니다.\n"+data + stateus + err);
            }
        });
    }
</script>
</head>
<body>
	<!-- 체크카드 발급 메인 화면 Start -->
	<div class="wrapper" id="wrapper">
		<div id="container">
			<div id="contents" class="prd-detail fixed-bottom">
				<section class="pd-h mt35">
					<div class="card-area mt20">
						<div class="card-img">
							<div class="img">
								<img src="/mobweb/images_kiwi/ncontents/Img-card-s-02.png" alt="KB국민 kiwibank 체크카드">
							</div>
							<h3 class="title-d">
								KB저축은행 팡팡KB 체크카드
								<small>KB저축은행 결제계좌 전용상품</small>
							</h3>
							<span class="type">
								<i class="i-txt"><span>국내</span></i>
								<i class="t-txt"><span>후불교통</span></i>
								<i class="txt"><span>연회비무료</span></i>
							</span>
						</div>
					</div>

					<div class="benefits-wrap">
						<!-- 2026-07-06 수정 시작 -->
                        <ul class="benefits-list">
                            <li>
                                <button type="button" class="ico-1" onclick="UI.layerPop('#send-sms');">
                                    <span class="info">
                                        <span class="subject">[오픈마켓] <em>10% 할인</em></span>
                                        <span class="options">11번가,  G마켓, SSG.COM</span>
                                    </span>
                                </button>
                            </li>
                            <li>
                                <button type="button" class="ico-2">
                                    <span class="info">
                                        <span class="subject">[오픈마켓] KB Pay 추가 <em>10%할인</em></span>
                                        <span class="options">11번가,  G마켓, SSG.COM</span>
                                    </span>
                                </button>
                            </li>
                            <li>
                                <button type="button" class="ico-3">
                                    <span class="info">
                                        <span class="subject">[커피] <em>10% 할인</em></span>
                                        <span class="options">스타벅스(사이렌오더 포함), 커피빈(퍼플오더 제외)</span>
                                    </span>
                                </button>
                            </li>
                            <li>
                                <button type="button" class="ico-4">
                                    <span class="info">
                                        <span class="subject">[대형마트] <em>10% 할인</em></span>
                                        <span class="options">이마트, 롯데마트, 홈플러스</span>
                                    </span>
                                </button>
                            </li>
                            <li>
                                <button type="button" class="ico-5">
                                    <span class="info">
                                        <span class="subject">[OTT 구독] <em>20% 할인</em></span>
                                        <span class="options">넷플릭스, 유튜브 자동납부</span>
                                    </span>
                                </button>
                            </li>
                            <li>
                                <button type="button" class="ico-6">
                                    <span class="info">
                                        <span class="subject">[영화] <em>최대 8,000원 할인</em></span>
                                        <span class="options">CGV, 롯데시네마, 메가박스</span>
                                    </span>
                                </button>
                            </li>
                            <li>
                                <button type="button" class="ico-7">
                                    <span class="info">
                                        <span class="subject">[패밀리레스토랑] <em>4,000원 할인</em></span>
                                        <span class="options">패밀리레스토랑 업종</span>
                                    </span>
                                </button>
                            </li>
                            <li>
                                <button type="button" class="ico-8">
                                    <span class="info">
                                        <span class="subject">[통신 자동납부] <em>3,000원 할인</em></span>
                                        <span class="options">SKT, KT, LG U+, Live M</span>
                                    </span>
                                </button>
                            </li>
                            <li>
                                <button type="button" class="ico-9">
                                    <span class="info">
                                        <span class="subject">[놀이공원] <em>15,000원 할인</em></span>
                                        <span class="options">에버랜드, 롯데월드</span>
                                    </span>
                                </button>
                            </li>
                        </ul>
                        <!-- //2026-07-06 수정 끝 -->
					</div>
					
					<div class="mt8 download-file">
						<a href="#none" class="btn-download2" id="cardPdfDown" onclick="javascript:downPDFtoTMS()">
							<span>
								상품설명서 안내 PDF다운로드
							</span>
							<i class="ico-download"></i>
						</a>
					</div>
				</section>
<!--
                <section class="pd-all">
                    <dl class="download-info">
                        <dt>상품설명서 안내</dt>
                        <dd>
                            <a href="javascript:downPDFtoTMS()" class="btn-md-func3" id="cardPdfDown">
                                <span>PDF다운로드</span><i class="ico-download"></i>
                            </a>
                        </dd>
                    </dl>
                </section>
-->

				<section class="layer fullpage" id="send-sms">  
					<div class="layer-header">
						<h1 class="layer-title">주요혜택</h1>
						<button type="button" class="layer-close cancel">
							<span class="sr-only">레이어 닫기</span>
						</button>
					</div>
					<div class="layer-contents type1">
						<div class="mb20  benefit-swiper"  id="cardBenefit">
							<div class="swiper-wrapper">
								<div class="swiper-slide">
									<div class="img-benefit b1">
										<span class="label">오픈마켓</span>
										<p>11번가, G마켓, SSG.COM</p>
										<small>10% 환급할인</small>
										<img src="/mobweb/images_kiwi/ncontents/card-benefit-01.png" alt="" />
									</div>
								</div>
								<div class="swiper-slide">
									<div class="img-benefit b2">
										<span class="label">오픈마켓</span>
										<p>KB Pay 결제 시 11번가, <br>G마켓, SSG.COM</p>
										<small>10% 추가 환급할인</small>
										<img src="/mobweb/images_kiwi/ncontents/card-benefit-01.png" alt="" />
									</div>
								</div>
								<div class="swiper-slide">
									<div class="img-benefit b3">
										<span class="label">커피</span>
										<p>스타벅스(사이렌오더 포함), <br>커피빈(퍼플오더 제외)</p>
										<small>10% 환급할인</small>
										<img src="/mobweb/images_kiwi/ncontents/card-benefit-02.png" alt="" />
									</div>
								</div>
								<div class="swiper-slide">
									<div class="img-benefit b4">
										<span class="label">대형마트</span>
										<p>이마트, 롯데마트, 홈플러스</p>
										<small>10% 환급할인</small>
										<img src="/mobweb/images_kiwi/ncontents/card-benefit-03.png" alt="" />
									</div>
								</div>
								<div class="swiper-slide">
									<div class="img-benefit b5">
										<span class="label">OTT구독</span>
										<p>넷플릭스, 유튜브</p>
										<small>20% 환급할인</small>
										<img src="/mobweb/images_kiwi/ncontents/card-benefit-04.png" alt="" />
									</div>
								</div>
								<div class="swiper-slide">
									<div class="img-benefit b6">
											<span class="label">영화</span>
											<p>CGV, 롯데시네마, 메가박스</p>
											<small>8,000원 환급할인</small>
										<img src="/mobweb/images_kiwi/ncontents/card-benefit-05.png" alt="" />
									</div>
								</div>
								<div class="swiper-slide">
									<div class="img-benefit b7">
										<span class="label">패밀리레스토랑</span>
										<p>패밀리레스토랑 업종</p>
										<small>4,000원 환급할인</small>
										<img src="/mobweb/images_kiwi/ncontents/card-benefit-06.png" alt="" />
									</div>
								</div>
								<div class="swiper-slide">
									<div class="img-benefit b8">
										<span class="label">통신 자동납부</span>
										<p>SKT, KT, LG U+, Liiv M</p>
										<small>3,000원 환급할인</small>
										<img src="/mobweb/images_kiwi/ncontents/card-benefit-07.png" alt="" />
									</div>
								</div>
								<div class="swiper-slide">
									<div class="img-benefit b9">
										<span class="label">놀이공원</span>
										<p>에버랜드, 롯데월드</p>
										<small>15,000원 환급할인</small>
										<img src="/mobweb/images_kiwi/ncontents/card-benefit-08.png" alt="" />
									</div>
								</div>
							</div>
							<div class="swiper-pagination msg-card-indicator"></div>
						</div>

						<!-- 1. 오픈마켓 : 11번가, G마켓, SSG  -->
						<div class="card-benefit-info visible" id="Open">
							<table class="data-table">
								<caption>오픈마켓 할인율</caption>
								<colgroup>
									<col width="33%">
									<col>
									<col>
								</colgroup>
								<thead>
									<tr>
										<th scope="col">구분</th>
										<th scope="col">할인율</th>
										<th scope="col">월 할인한도</th>
									</tr>
								</thead>
							<tbody>
							<tr>
								<td>11번가, G마켓, SSG.COM</td>
								<td>10%</td>
								<td>7천원</td>
							</tr>
						</tbody>
					</table>
					<p class="mt12 light">전월 이용실적 조건 : KB저축은행 팡팡 KB체크카드로 전월 실적 20만원 이상 시 제공</p>
					<p class="mt6 light">본인 회원 기준으로 전표매입순서대로 월간 통합할인 한도 내에서 혜택 제공됩니다.</p>
					<h3 class="text-lightgray mt28">통합할인한도</h3>
					<table class="data-table mt12">
						<caption>통합할인한도</caption>
						<colgroup>
							<col>
							<col>
						</colgroup>
						<thead>
							<tr>
								<th scope="col">전월 이용실적</th>
								<th scope="col">월간 통합할인</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>20만원 이상 시</td>
                                <td>2만원</td>
                            </tr>
                            <tr>
                                <td>40만원 이상 시</td>
                                <td>3만원</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="bg-gray-box type01 round-8 mt28">
                        <p class="text">전월 이용실적 기준</p>
                        <ul class="list-bullet-dot mt16">
                            <li>전월 1일 ~ 말일까지 KB저축은행 팡팡 KB체크카드 승인(이용)금액</li>
                            <li>취소금액은 취소전표가 KB국민카드에 접수된 월의 실적에서 차감</li>
                        </ul>
                    </div>
                    <div class="bg-gray-box type01 round-8 mt12">
                        <p class="text">전월 이용실적 제외 대상</p>
                        <ul class="list-bullet-dot mt16">
                            <li>후불교통요금, 무승인 금액(자판기, 터널통행료, 유료도로, 기차/고속버스 취소 반환수수료 등), 
                                정부지원금 이용금액 (보육료, 유치원 보조비, 바우처 이용금액 등), 포인트리 충전금액, 대학(대학원) 등록금,
                                상품권 및 선불카드(선불전자지금수단 포함) 구입(충전)금액, 연체료, 지방세(상하수도, 세외수입 등), 취소금액,
                                각종 수수료 및 이자
                            </li>
                        </ul>
                    </div>
                </div>
                <!-- 2. 오픈마켓 : KB Pay 결제 시  -->
                
                <div class="card-benefit-info hidden" id="OpenKbPay">
                    <table class="data-table">
                        <caption>할인율</caption>
                        <colgroup>
                            <col width="45%">
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">구분</th>
                                <th scope="col">할인율</th>
                                <th scope="col">월 할인한도</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>[11번가, G마켓, SSG.COM]<br> KB Pay 결제 시</td>
                                <td>10%</td>
                                <td>3천원</td>
                            </tr>
                        </tbody>
                    </table>
                    <p class="mt12 light">전월 이용실적 조건 : KB저축은행 팡팡 KB체크카드로 전월 실적 20만원 이상 시 제공</p>
                    <p class="mt6 light">본인 회원 기준으로 전표매입순서대로 월간 통합할인 한도 내에서 혜택 제공됩니다.</p>
                    <h3 class="text-lightgray mt28">통합할인한도</h3>
                    <table class="data-table mt12">
                        <caption>통합할인한도</caption>
                        <colgroup>
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">전월 이용실적</th>
                                <th scope="col">월간 통합할인</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>20만원 이상 시</td>
                                <td>2만원</td>
                            </tr>
                            <tr>
                                <td>40만원 이상 시</td>
                                <td>3만원</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="bg-gray-box type01 round-8 mt28">
                        <p class="text">전월 이용실적 기준</p>
                        <ul class="list-bullet-dot mt16">
                            <li>전월 1일 ~ 말일까지 KB저축은행 팡팡 KB체크카드 승인(이용)금액</li>
                            <li>취소금액은 취소전표가 KB국민카드에 접수된 월의 실적에서 차감</li>
                        </ul>
                    </div>
                    <div class="bg-gray-box type01 round-8 mt12">
                        <p class="text">전월 이용실적 제외 대상</p>
                        <ul class="list-bullet-dot mt16">
                            <li>후불교통요금, 무승인 금액(자판기, 터널통행료, 유료도로, 기차/고속버스 취소 반환수수료 등), 
                                정부지원금 이용금액 (보육료, 유치원 보조비, 바우처 이용금액 등), 포인트리 충전금액, 대학(대학원) 등록금,
                                상품권 및 선불카드(선불전자지금수단 포함) 구입(충전)금액, 연체료, 지방세(상하수도, 세외수입 등), 취소금액,
                                각종 수수료 및 이자
                            </li>
                        </ul>
                    </div>
                </div>
                <!-- 3. 커피  -->
                <div class="card-benefit-info hidden" id="Coffee">
                    <table class="data-table">
                        <caption>할인율</caption>
                        <colgroup>
                            <col width="45%">
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">구분</th>
                                <th scope="col">할인율</th>
                                <th scope="col">월 할인한도</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>스타벅스(사이렌오더 포함), 커피빈(퍼플오더 제외)</td>
                                <td>10%</td>
                                <td>4천원</td>
                            </tr>
                        </tbody>
                    </table>
                    <p class="mt12 light">전월 이용실적 조건 : KB저축은행 팡팡 KB체크카드로 전월 실적 20만원 이상 시 제공</p>
                    <p class="mt6 light">본인 회원 기준으로 전표매입순서대로 월간 통합할인 한도 내에서 혜택 제공됩니다.</p>
                    <h3 class="text-lightgray mt28">통합할인한도</h3>
                    <table class="data-table mt12">
                        <caption>통합할인한도</caption>
                        <colgroup>
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">전월 이용실적</th>
                                <th scope="col">월간 통합할인</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>20만원 이상 시</td>
                                <td>2만원</td>
                            </tr>
                            <tr>
                                <td>40만원 이상 시</td>
                                <td>3만원</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="bg-gray-box type01 round-8 mt28">
                        <p class="text">전월 이용실적 기준</p>
                        <ul class="list-bullet-dot mt16">
                            <li>전월 1일 ~ 말일까지 KB저축은행 팡팡 KB체크카드 승인(이용)금액</li>
                            <li>취소금액은 취소전표가 KB국민카드에 접수된 월의 실적에서 차감</li>
                        </ul>
                    </div>
                    <div class="bg-gray-box type01 round-8 mt12">
                        <p class="text">전월 이용실적 제외 대상</p>
                        <ul class="list-bullet-dot mt16">
                            <li>후불교통요금, 무승인 금액(자판기, 터널통행료, 유료도로, 기차/고속버스 취소 반환수수료 등), 
                                정부지원금 이용금액 (보육료, 유치원 보조비, 바우처 이용금액 등), 포인트리 충전금액, 대학(대학원) 등록금,
                                상품권 및 선불카드(선불전자지금수단 포함) 구입(충전)금액, 연체료, 지방세(상하수도, 세외수입 등), 취소금액,
                                각종 수수료 및 이자
                            </li>
                        </ul>
                    </div>
                </div>
                <!-- 4. 대형마트  -->
                <div class="card-benefit-info hidden" id="BigMart">
                    <table class="data-table">
                        <caption>대형마트 할인율</caption>
                        <colgroup>
                            <col width="45%">
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">구분</th>
                                <th scope="col">할인율</th>
                                <th scope="col">월 할인한도</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>이마트, 롯데마트, 홈플러스</td>
                                <td>10%</td>
                                <td>3천원</td>
                            </tr>
                        </tbody>
                    </table>
                    <p class="mt12 light">전월 이용실적 조건 : KB저축은행 팡팡 KB체크카드로 전월 실적 20만원 이상 시 제공</p>
                    <p class="mt6 light">본인 회원 기준으로 전표매입순서대로 월간 통합할인 한도 내에서 혜택 제공됩니다.</p>
                    <h3 class="text-lightgray mt28">통합할인한도</h3>
                    <table class="data-table mt12">
                        <caption>통합할인한도</caption>
                        <colgroup>
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">전월 이용실적</th>
                                <th scope="col">월간 통합할인</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>20만원 이상 시</td>
                                <td>2만원</td>
                            </tr>
                            <tr>
                                <td>40만원 이상 시</td>
                                <td>3만원</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="bg-gray-box type01 round-8 mt28">
                        <p class="text">전월 이용실적 기준</p>
                        <ul class="list-bullet-dot mt16">
                            <li>전월 1일 ~ 말일까지 KB저축은행 팡팡 KB체크카드 승인(이용)금액</li>
                            <li>취소금액은 취소전표가 KB국민카드에 접수된 월의 실적에서 차감</li>
                        </ul>
                    </div>
                    <div class="bg-gray-box type01 round-8 mt12">
                        <p class="text">전월 이용실적 제외 대상</p>
                        <ul class="list-bullet-dot mt16">
                            <li>후불교통요금, 무승인 금액(자판기, 터널통행료, 유료도로, 기차/고속버스 취소 반환수수료 등), 
                                정부지원금 이용금액 (보육료, 유치원 보조비, 바우처 이용금액 등), 포인트리 충전금액, 대학(대학원) 등록금,
                                상품권 및 선불카드(선불전자지금수단 포함) 구입(충전)금액, 연체료, 지방세(상하수도, 세외수입 등), 취소금액,
                                각종 수수료 및 이자
                            </li>
                        </ul>
                    </div>
                </div>
                <!-- 5. OTT구독  -->
                <div class="card-benefit-info hidden" id="OTT">
                    <table class="data-table">
                        <caption>OTT구독 할인율</caption>
                        <colgroup>
                            <col width="45%">
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">구분</th>
                                <th scope="col">할인율</th>
                                <th scope="col">월 할인한도</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>넷플릭스, 유튜브</td>
                                <td>20%</td>
                                <td>2천원</td>
                            </tr>
                        </tbody>
                    </table>
                    <p class="mt12 light">이용금액 건당 1만원 이상 이용 시 적용</p>
                    <p class="mt6 light">유튜브 프리미엄, 넷플릭스 공식 홈페이지/앱을 통한 정기결제 시 할인</p>
                    <p class="mt6 light">전월 이용실적 조건: KB저축은행 팡팡 KB체크카드로 전월 실적 20만원 이상 시 제공</p>
                    <p class="mt6 light">본인 회원기준으로 전표매입순서대로 월간 통합할인 한도 내에서 혜택 제공됩니다.</p>
                    
                    <h3 class="text-lightgray mt28">통합할인한도</h3>
                    <table class="data-table mt12">
                        <caption>통합할인한도</caption>
                        <colgroup>
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">전월 이용실적</th>
                                <th scope="col">월간 통합할인</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>20만원 이상 시</td>
                                <td>2만원</td>
                            </tr>
                            <tr>
                                <td>40만원 이상 시</td>
                                <td>3만원</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="bg-gray-box type01 round-8 mt28">
                        <p class="text">전월 이용실적 기준</p>
                        <ul class="list-bullet-dot mt16">
                            <li>전월 1일 ~ 말일까지 KB저축은행 팡팡 KB체크카드 승인(이용)금액</li>
                            <li>취소금액은 취소전표가 KB국민카드에 접수된 월의 실적에서 차감</li>
                        </ul>
                    </div>
                    <div class="bg-gray-box type01 round-8 mt12">
                        <p class="text">전월 이용실적 제외 대상</p>
                        <ul class="list-bullet-dot mt16">
                            <li>후불교통요금, 무승인 금액(자판기, 터널통행료, 유료도로, 기차/고속버스 취소 반환수수료 등), 
                                정부지원금 이용금액 (보육료, 유치원 보조비, 바우처 이용금액 등), 포인트리 충전금액, 대학(대학원) 등록금,
                                상품권 및 선불카드(선불전자지금수단 포함) 구입(충전)금액, 연체료, 지방세(상하수도, 세외수입 등), 취소금액,
                                각종 수수료 및 이자
                            </li>
                        </ul>
                    </div>
                </div>
                <!-- 6. 영화  -->
                <div class="card-benefit-info hidden" id="Movie">
                    <table class="data-table">
                        <caption>영화 할인율</caption>
                        <colgroup>
                            <col width="45%">
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">구분</th>
                                <th scope="col">할인율</th>
                                <th scope="col">월 할인한도</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>CGV, 롯데시네마, 메가박스</td>
                                <td>건당 4천원</td>
                                <td>8천원</td>
                            </tr>
                        </tbody>
                    </table>
                    <p class="mt12 light">이용금액 건당 1만원 이상 이용 시 제공</p>
                    <p class="mt6 light">월 할인횟수 2회</p>
                    <p class="mt6 light">매점 &#183; 관람권 &#183; 상품권 및 예매대행 사이트 이용 제외</p>
                    <p class="mt6 light">전월 이용실적 조건: KB저축은행 팡팡 KB체크카드로 전월 실적 20만원 이상 시 제공</p>
                    <p class="mt6 light">본인 회원기준으로 전표매입순서대로 월간 통합할인 한도 내에서 혜택 제공됩니다.</p>
                    
                    <h3 class="text-lightgray mt28">통합할인한도</h3>
                    <table class="data-table mt12">
                        <caption>통합할인한도</caption>
                        <colgroup>
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">전월 이용실적</th>
                                <th scope="col">월간 통합할인</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>20만원 이상 시</td>
                                <td>2만원</td>
                            </tr>
                            <tr>
                                <td>40만원 이상 시</td>
                                <td>3만원</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="bg-gray-box type01 round-8 mt28">
                        <p class="text">전월 이용실적 기준</p>
                        <ul class="list-bullet-dot mt16">
                            <li>전월 1일 ~ 말일까지 KB저축은행 팡팡 KB체크카드 승인(이용)금액</li>
                            <li>취소금액은 취소전표가 KB국민카드에 접수된 월의 실적에서 차감</li>
                        </ul>
                    </div>
                    <div class="bg-gray-box type01 round-8 mt12">
                        <p class="text">전월 이용실적 제외 대상</p>
                        <ul class="list-bullet-dot mt16">
                            <li>후불교통요금, 무승인 금액(자판기, 터널통행료, 유료도로, 기차/고속버스 취소 반환수수료 등), 
                                정부지원금 이용금액 (보육료, 유치원 보조비, 바우처 이용금액 등), 포인트리 충전금액, 대학(대학원) 등록금,
                                상품권 및 선불카드(선불전자지금수단 포함) 구입(충전)금액, 연체료, 지방세(상하수도, 세외수입 등), 취소금액,
                                각종 수수료 및 이자
                            </li>
                        </ul>
                    </div>
                </div>
                <!-- 7. 패밀리레스토랑  -->
                <div class="card-benefit-info hidden" id="Family">
                    <table class="data-table">
                        <caption>패밀리레스토랑 할인율</caption>
                        <colgroup>
                            <col width="45%">
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">구분</th>
                                <th scope="col">할인율</th>
                                <th scope="col">월 할인한도</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>패밀리레스토랑 업종</td>
                                <td>건당 4천원</td>
                                <td>4천원</td>
                            </tr>
                        </tbody>
                    </table>
                    <p class="mt12 light">이용금액 건당 5만원 이상 이용 시 제공</p>
                    <p class="mt6 light">월 할인횟수 1회</p>
                    <p class="mt6 light">전월 이용실적 조건: KB저축은행 팡팡 KB체크카드로 전월 실적 20만원 이상 시 제공</p>
                    <p class="mt6 light">본인 회원기준으로 전표매입순서대로 월간 통합할인 한도 내에서 혜택 제공됩니다.</p>
                    
                    <h3 class="text-lightgray mt28">통합할인한도</h3>
                    <table class="data-table mt12">
                        <caption>통합할인한도</caption>
                        <colgroup>
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">전월 이용실적</th>
                                <th scope="col">월간 통합할인</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>20만원 이상 시</td>
                                <td>2만원</td>
                            </tr>
                            <tr>
                                <td>40만원 이상 시</td>
                                <td>3만원</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="bg-gray-box type01 round-8 mt28">
                        <p class="text">전월 이용실적 기준</p>
                        <ul class="list-bullet-dot mt16">
                            <li>전월 1일 ~ 말일까지 KB저축은행 팡팡 KB체크카드 승인(이용)금액</li>
                            <li>취소금액은 취소전표가 KB국민카드에 접수된 월의 실적에서 차감</li>
                        </ul>
                    </div>
                    <div class="bg-gray-box type01 round-8 mt12">
                        <p class="text">전월 이용실적 제외 대상</p>
                        <ul class="list-bullet-dot mt16">
                            <li>후불교통요금, 무승인 금액(자판기, 터널통행료, 유료도로, 기차/고속버스 취소 반환수수료 등), 
                                정부지원금 이용금액 (보육료, 유치원 보조비, 바우처 이용금액 등), 포인트리 충전금액, 대학(대학원) 등록금,
                                상품권 및 선불카드(선불전자지금수단 포함) 구입(충전)금액, 연체료, 지방세(상하수도, 세외수입 등), 취소금액,
                                각종 수수료 및 이자
                            </li>
                        </ul>
                    </div>
                </div>
                <!-- 8. 통신 자동납부  -->
                <div class="card-benefit-info hidden" id="CmncAuto">
                    <table class="data-table">
                        <caption>통신 자동납부 할인율</caption>
                        <colgroup>
                            <col width="45%">
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">구분</th>
                                <th scope="col">할인율</th>
                                <th scope="col">월 할인한도</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>SKT, KT, LG U+, Liiv M</td>
                                <td>건당 3천원</td>
                                <td>3천원</td>
                            </tr>
                        </tbody>
                    </table>
                    <p class="mt12 light">이용금액 건당 5만원 이상 이용 시 제공</p>
                    <p class="mt6 light">월 할인횟수 1회</p>
                    <p class="mt6 light">전월 이용실적 조건: KB저축은행 팡팡 KB체크카드로 전월 실적 20만원 이상 시 제공</p>
                    <p class="mt6 light">본인 회원기준으로 전표매입순서대로 월간 통합할인 한도 내에서 혜택 제공됩니다.</p>
                    
                    <h3 class="text-lightgray mt28">통합할인한도</h3>
                    <table class="data-table mt12">
                        <caption>통합할인한도</caption>
                        <colgroup>
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">전월 이용실적</th>
                                <th scope="col">월간 통합할인</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>20만원 이상 시</td>
                                <td>2만원</td>
                            </tr>
                            <tr>
                                <td>40만원 이상 시</td>
                                <td>3만원</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="bg-gray-box type01 round-8 mt28">
                        <p class="text">전월 이용실적 기준</p>
                        <ul class="list-bullet-dot mt16">
                            <li>전월 1일 ~ 말일까지 KB저축은행 팡팡 KB체크카드 승인(이용)금액</li>
                            <li>취소금액은 취소전표가 KB국민카드에 접수된 월의 실적에서 차감</li>
                        </ul>
                    </div>
                    <div class="bg-gray-box type01 round-8 mt12">
                        <p class="text">전월 이용실적 제외 대상</p>
                        <ul class="list-bullet-dot mt16">
                            <li>후불교통요금, 무승인 금액(자판기, 터널통행료, 유료도로, 기차/고속버스 취소 반환수수료 등), 
                                정부지원금 이용금액 (보육료, 유치원 보조비, 바우처 이용금액 등), 포인트리 충전금액, 대학(대학원) 등록금,
                                상품권 및 선불카드(선불전자지금수단 포함) 구입(충전)금액, 연체료, 지방세(상하수도, 세외수입 등), 취소금액,
                                각종 수수료 및 이자
                            </li>
                        </ul>
                    </div>
                </div>
                <!-- 9. 놀이공원  -->
                <div class="card-benefit-info hidden" id="Park">
                    <table class="data-table">
                        <caption>놀이공원 할인율</caption>
                        <colgroup>
                            <col width="45%">
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">구분</th>
                                <th scope="col">할인율</th>
                                <th scope="col">월 할인한도</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>에버랜드, 롯데월드</td>
                                <td>건당 1만5천원</td>
                                <td>1만5천원</td>
                            </tr>
                        </tbody>
                    </table>
                    <p class="mt12 light">이용금액 건당 3만원 이상 이용 시 제공</p>
                    <p class="mt6 light">월 할인횟수 1회</p>
                    <p class="mt6 light">티켓 요금(입장권, 이용권) 결제 시 할인 제공하며, 상품권 구매 및 매점 이용분 할인 불가</p>
                    <p class="mt6 light">전월 이용실적 조건: KB저축은행 팡팡 KB체크카드로 전월 실적 20만원 이상 시 제공</p>
                    <p class="mt6 light">본인 회원기준으로 전표매입순서대로 월간 통합할인 한도 내에서 혜택 제공됩니다.</p>
                    
                    <h3 class="text-lightgray mt28">통합할인한도</h3>
                    <table class="data-table mt12">
                        <caption>통합할인한도</caption>
                        <colgroup>
                            <col>
                            <col>
                        </colgroup>
                        <thead>
                            <tr>
                                <th scope="col">전월 이용실적</th>
                                <th scope="col">월간 통합할인</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>20만원 이상 시</td>
                                <td>2만원</td>
                            </tr>
                            <tr>
                                <td>40만원 이상 시</td>
                                <td>3만원</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="bg-gray-box type01 round-8 mt28">
                        <p class="text">전월 이용실적 기준</p>
                        <ul class="list-bullet-dot mt16">
                            <li>전월 1일 ~ 말일까지 KB저축은행 팡팡 KB체크카드 승인(이용)금액</li>
                            <li>취소금액은 취소전표가 KB국민카드에 접수된 월의 실적에서 차감</li>
                        </ul>
                    </div>
                    <div class="bg-gray-box type01 round-8 mt12">
                        <p class="text">전월 이용실적 제외 대상</p>
                        <ul class="list-bullet-dot mt16">
                            <li>후불교통요금, 무승인 금액(자판기, 터널통행료, 유료도로, 기차/고속버스 취소 반환수수료 등), 
                                정부지원금 이용금액 (보육료, 유치원 보조비, 바우처 이용금액 등), 포인트리 충전금액, 대학(대학원) 등록금,
                                상품권 및 선불카드(선불전자지금수단 포함) 구입(충전)금액, 연체료, 지방세(상하수도, 세외수입 등), 취소금액,
                                각종 수수료 및 이자
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
		</section>

				<!-- 2026-07-06 수정 시작 -->
                <section class="pd-h mt36">
					<div class="ui-accordion desc">
						<dl>
							<dt class="acc-title">
								<button type="button">
									<span class="title">이용 전 확인해주세요</span>
									<span class="sr-only">더보기</span>
								</button>
							</dt>
							<dd class="acc-cont">
								<h3 class="text-lightgray2">카드발급</h3>
								<ul class="list-bullet-dot">
									<li>후불교통 체크카드 인터넷 신청은 만 18세 이상부터 가능합니다.</li>
									<li>만7세~만13세(후불교통기능 탑재 상품은 만12세~만17세) 미성년자의 카드 발급은 KBpay(모바일웹 포함),고객센터에서 법정대리인이 대리 신청 가능합니다.</li>
									<li>외국인 고객은 고객센터(1588-1688)로 확인하여 주시기 바랍니다.
                                        <p class="bullet-dash">특수채권 잔액 보유 또는 은행연합회 신용관리 대상 등 일부 고객은 후불교통기능이 탑재된 KB국민 체크카드의 발급이 제한될 수 있습니다.</p>
                                    </li>
								</ul>
								
								<h3>전원 이용실적 기준</h3>
								<ul class="list-bullet-dot">
									<li>전월 1일~말일까지 KB저축은행 팡팡 KB체크카드 승인(이용)금액</li>
									<li>취소금액은 취소전표가 KB국민카드에 접수된 월의 실적에서 차감</li>
								</ul>

                                <h3>전월 이용실적 제외 대상</h3>
								<ul class="list-bullet-dot">
									<li>후불교통요금, 무승인 금액(자판기, 터널통행료, 유료도로, 기차/고속버스 취소 반환수수료 등), 정부지원금 이용금액(보육료, 유치원 보조비, 바우처 이용금액 등) , 포인트리 충전금액, 대학(대학원)등록금, 상품권 및 선불카드(선불전자 지급수단 포함) 구입(충전)금액, 연체료, 지방세(상하수도, 세외수입 등), 취소금액, 각종 수수료 및 이자</li>
								</ul>
								<h3>할인서비스 적용 안내</h3>
								<ul class="list-bullet-dot">
									<li>체크카드 환급할인은 이용전표가 매입처리 완료 된 후 할인금액을 카드 출금계좌로 환급하는 방식입니다.</li> 
									<li>본인 회원 기준으로 월간 할인한도가 제공되며, 할인한도는 매월 1일 ~ 말일까지(승인시점기준)이용금액으로 적용됩니다.</li> 
									<li>할인서비스는 전표매입 순서대로 월간 할인한도 내에서 적용되며, 잔여한도는 이월되지 않습니다.</li>
                                    <li>할인 받은 매출을 취소한 경우 취소 전표가 실시간 접수되지 않아 할인한도가 즉시 복원되지 않을 수 있습니다.</li> 
									<li>각 할인서비스는 해당 가맹점이 KB국민카드의 가맹점 업종코드(제휴업체코드)상 할인대상 가맹점 업종으로 등록된 경우에 한하여 제공됩니다.</li>
                                    <li>
                                        가맹점 정보가 해당 업체가 아닌 결제대행업체(PG) 또는 간편결제 전용 가맹점으로 확인되는 경우, '결제대행업체' 또는 '간편결제' 가맹점으로 분류되어 할인대상에서 제외됩니다.
                                        <br/>
                                        <p class="bullet-dash">예시) 커피업종에서 네이버페이로 결제 시 가맹점명이 ‘네이버페이’인 경우 커피 업종 가맹점이 아닌 ‘간편결제’ 가맹점으로 분류</p>
                                    </li>
                                    <li>호텔, 백화점, 대형마트, 철도/역사 등에 입점한 가맹점이나 상품권 구매시 할인 대상에서 제외됩니다.</li>
                                    <li>상품권 및 선불카드(선불전자지급수단 포함) 구입·충전 금액의 경우 할인에서 제외될 수 있습니다.</li>
                                    <li>자세한 사항은 KB국민카드 고객센터(1588-1688)에 문의하시기 바랍니다.</li>
								</ul>

                                <h3>체크카드 이용제한</h3>
								<ul class="list-bullet-dot">
									<li>KB저축은행 전산가동 중단 시 예금잔액을 즉시 확인할 수 없어 사용이 제한될 수 있습니다.</li>
								</ul>

								<h3 class="align-center">체크카드 직불이용한도
                                    <small class="text-12">카드발급 시 부여한도(기본한도)</small>
                                </h3>

								<table class="data-table mt12">
									<caption>카드발급 시 부여한도(기본한도)</caption>
									<colgroup>
										<col>
										<col>
										<col>
										<col>
									</colgroup>
									<thead>
										<tr>
											<th scope="col">구분</th>
											<th scope="col">1회</th>
											<th scope="col">1일</th>
											<th scope="col">월간</th>
										</tr>
									</thead>
									<tbody>
										<tr>
											<td>만7세<br/>~만13세</td>
											<td>3만원</td>
											<td>3만원</td>
											<td>30만원</td>
										</tr>
										<tr>
											<td>만14세 이상</td>
											<td>600만원</td>
											<td>600만원</td>
											<td>2천만원</td>
										</tr>
									</tbody>
								</table>
								<h3>※만14세가 경과하면 고객센터에 요청하여 상향가능</h3>

                                <h3>후불교통 기능 탑재</h3>
								<ul class="list-bullet-dot">
									<li>버스, 지하철 등 교통이용이 가능하고, 매월 체크카드 결제 계좌에서 지정된 결제일에 자동 출금됩니다.</li>
									<li>정상 출금되지 않은 경우 연체에 따른 교통기능 이용이 불가할 수 있으며, 미납금액에 대해서는 연체료가 부과됩니다.</li>
									<li>이용금액 출금 시 한도가 복원됩니다.</li>
								</ul>
                                <table class="data-table mt12">
									<caption>카드발급 시 부여한도(기본한도)</caption>
									<colgroup>
										<col style="width:106px;">
										<col style="width:auto;">
									</colgroup>
									<tbody>
										<tr>
                                            <th>이용일</th>
											<td>1일~말일</td>
										</tr>
										<tr>
                                            <th>출금일</th>
											<td>해당 제휴 체크카드 결제일</td>
										</tr>
									</tbody>
								</table>

                                <h3>미성년자 후불교통 체크카드 이용</h3>
								<ul class="list-bullet-dot">
									<li>만12세 이상 미성년자는 청소년 후불교통 체크카드를 발급받을 수 있습니다.</li>
									<li>만12세~만17세의 경우 법정대리인의 동의가 필요(만18세이상의 미성년자는 법정대리인 동의 불필요)하며, 전체 카드사 기준 1인 1매만 소지 가능합니다.</li>
									<li>만12세~만17세의 경우 월 이용한도는 10만원 이하이나, 교통카드 이용내역 및 금액 정산 체계로 일시적 이용한도 초과 사용이 가능합니다.</li>
								</ul>
                                <h3>영업 마감시간 이후 결제계좌 출금</h3>
								<ul class="list-bullet-dot">
									<li>결제계좌 개설기관의 영업 마감시간(16시) 이후 입금 된 금액에 대해서는 당일 출금되지 못하여 연체 처리 될 수 있으니 유의하시기 바랍니다. 자동이체 업무 마감시간 이후 KB국민카드 홈페이지/모바일*등에서 바로출금(즉시결제) 또는 가상계좌 입금(송금납부)을 통해 당일 결제가 가능합니다.</li>
                                    <li><em class="highlight">세부내용: KB국민카드 홈페이지 &gt; MY KB &gt; 바로출금 또는 가상계좌 참조</em></li>
								</ul>
                                <h3>부가서비스 변경 안내</h3>
								<ul class="list-bullet-dot">
									<li>KB저축은행 팡팡 KB체크카드(2025.03.26 출시)를 이용하는 경우 제공되는 할인혜택 등의 부가서비스는 다음 호를 제외하고는 변경 할 수 없습니다. (단, 회원의 권익을 증진하거나 부담을 완화하는 경우는 제외합니다.)
										<ul class="list-bullet-dash">
											<li>1. 카드사의 휴업·파산·경영상의 위기로 인해 불가피한 경우</li>
											<li>1의2. 제휴업체의 휴업·파산·경영상의 위기로 인해 불가피하게 부가서비스를 축소·변경하는 경우로서 다른 제휴업체를 통해 같은 종류의 유사한 부가서비스 제공이 불가한 경우</li>
											<li>2. 제휴업체가 카드사의 의사에 반하여 해당 부가서비스를 축소하거나 변경 시, 당초 부가서비스에 상응하는 다른 부가서비스를 제공하는 경우</li>
                                            <li>3. 부가서비스를 3년 이상 제공한 상태에서 해당 부가서비스로 인해 상품의 수익성이 현저히 낮아진 경우</li>
										</ul>
									</li>
									<li>카드사가 부가서비스를 변경하는 경우 변경 사유, 변경 내용 등을 사유 발생 즉시 서면교부, 우편 또는 전자우편, 전화 또는 팩스, 문자메시지(SMS) 또는 이에 준하는 전자적 의사표시 중 서로 다른 2가지 이상 방법으로 고지하여 드립니다. 다만, 상기 3호의 경우 부가서비스 변경일 6개월 이전부터 서면교부, 우편 또는 전자우편, 전화 또는 팩스, 문자메시지(SMS) 또는 이에 준하는 전자적 의사표시 중 서로 다른 2가지 이상의 방법으로 매월 고지하여 드립니다.</li>									
								</ul>
                                <h3>기타</h3>
								<ul class="list-bullet-dot">
									<li>금융소비자는 금소법 제19조 제 1항에 따라 해당 상품 또는 서비스에 대하여 설명을 받을 권리가 있으며, 그 설명을 듣고 내용을 충분히 이해한 후 거래하시기 바랍니다.</li>
									<li>신용카드 발급이 부적정한 경우(개인신용평점 낮음, 연체금 보유 등) 카드발급이 제한될 수 있습니다.</li>
									<li>카드이용대금과 이에 수반되는 모든 수수료를 지정된 대금 결제일에 상환합니다.</li>
									<li>KB국민카드 카드상품개발부:kkgc20163@kbfg.com</li>
								</ul>
							</dd>                            
						</dl>
					</div>
				</section>
                <!-- 2026-07-06 수정 끝 -->
                <!-- 2026-07-06 수정 시작 -->
                <section class="pd-h">
                    <div class="mt36">
                        <h3 class="text-lightgray">카드 공통 안내사항</h3>                       
                        <ul class="list-bullet-dot color-black mt12">
                            <li>
                                [연체이자율] 회원별/이용상품별 정상이자율 +3%p, 법정 최고금리 연 20%
                                <p class="mt8">※ 단, 연체발생시점에 정상이자율이 없는 경우 아래와 같이 적용함</p>
                                <p class="bullet-dash color-black mt8">
                                    일시불 거래 연체 시: 거래발생시점의 최소기간(2개월) 유이자 할부수수료율 적용
                                </p>
                                <p class="bullet-dash color-black mt8">
                                    무이자할부 거래 연체 시: 거래발생시점의 동일한 할부계약 기간의 유이자할부수수료율 적용
                                </p>
                                <p class="bullet-dash color-black mt8">
                                    그 외의 경우: 정상이자율은 상법상 상사법정이율과 상호금융 가계자금대출금리* 중 높은 금리 적용
                                    <span class="color-black mt6">※
                                        한국은행에서 매월 발표하는 가장 최근의 비은행 금융기관 가중평균대출금리(신규대출 기준)</span>
                                </p>
                            </li>
                            <li>카드 신청 전 상품설명서 및 약관을 반드시 확인하시기 바랍니다.</li>
                            <li>필요 이상의 신용카드 발급 및 사용은 개인신용평점이나 이용한도 등에 영향을 미칠 수 있습니다.</li>
                            <li>상품 관련 세부 사항은 홈페이지(www.kbcard.com)를 참조 또는 고객센터(1588-1688)로 문의하여 주시기 바랍니다.</li>
                            <li><em class="text-highlight">상환능력에 비해 신용카드 사용액이 과도할 경우 귀하의 신용평점이 하락할 수 있습니다.</em></li>
                            <li><em class="text-highlight">개인신용평점 하락 시 금융거래 관련된 불이익이 발생할 수 있습니다.</em></li>
                            <li><em class="text-highlight">일정기간 원리금을 연체할 경우, 모든 원리금을 변제할 의무가 발생할 수 있습니다.</em></li>
                        </ul>
                        <p class="text-14-lightgray2 mt28 light">KB국민카드 준법감시인심의필 제260701-02230-PIF (2026.07.01)</p>
                    </div>
                </section>
                <!-- 2026-07-06 수정 끝 -->

				<div class="page-btns fixed">
					<!-- <button type="button" class="btn-lg-primary" onclick="goNext();">카드신청</button> -->
					<!-- SR-260521-01928 (웹)체크카드 발급신청 프로세스 변경 START -->
					<button type="button" class="btn-lg-primary" onclick="goNext();">KB국민카드에서 신청</button>
					<!-- SR-260521-01928 (웹)체크카드 발급신청 프로세스 변경 END -->
				</div>
			</div>
		</div>
	</div>
	<!-- 체크카드 발급 메인 화면 End -->
    
	<!-- 주요 혜택 확인 Start -->
	<section class="layer fullpage" id="benfPop">
		<div class="layer-header">
			<h1 class="layer-title">주요혜택</h1>
			<button type="button" class="layer-close cancel">
				<span class="sr-only">레이어 닫기</span>
			</button>
		</div>

		<div class="layer-contents ml24 mr24">
			<div id="headerTxt" class="benfHead">
				<!-- 헤더내용 -->
			</div>
			<div id="bodyTable" class="benfBody mt10">
				<table class="data-table">
					<caption>주요혜택 테이블</caption>
					<colgroup>
						<col style="width: 50%;">
						<col>
						<col>
					</colgroup>
					<thead style="text-align: center;">
						<tr>
							<th scope="col">구분</th>
							<th id="amtDcTxt" scope="col">할인율</th>
							<th scope="col">월 할인한도</th>
						</tr>
					</thead>
					<tbody style="text-align: center;">
						<tr>
							<td id="gubun"></td>
							<td id="amtDc"></td>
							<td id="limitDc"></td>
						</tr>
					</tbody>
				</table>
			</div>
			<div id="bodyTxt" class="benfBody">
				<!-- 본문내용 -->
			</div>
			<div id="bottomTxt" class="benfBody mt10">
				<h3 class="title-d3">통합할인한도</h3>
				<table class="data-table">
					<caption>통합할인한도</caption>
					<colgroup>
						<col>
						<col>
					</colgroup>
					<thead style="text-align: center;">
						<tr>
							<th scope="col">전월 이용실적</th>
							<th scope="col">월간 통합할인한도</th>
						</tr>
					</thead>
					<tbody style="text-align: center;">
						<tr>
							<td>20만원 이상 시</td>
							<td>20,000원</td>
						</tr>
						<tr>
							<td>40만원 이상 시</td>
							<td>30,000원</td>
						</tr>
					</tbody>
				</table>
				<div class="bg-gray mt10" style="padding:5px 10px 20px 10px;">
					<h3 class="title-d3">전월 이용실적 기준</h3>
					<ul class="list-bullet-dot">
						<li>전월 1일 ~ 말일까지 KB저축은행 팡팡 KB체크카드 승인(이용)금액</li>
						<li>취소금액은 취소전표가 KB국민카드에 접수된 월의 실적에서 차감</li>
					</ul>
					<h3 class="title-d3 mt20">전월 이용실적 제외 대상</h3>
					<ul class="list-bullet-dot">
						<li>
							후불교통요금, 무승인 금액(자판기, 터널통행료, 유료도로, 기차/고속버스 취소 반환수수료 등), 정부지원금 이용금액
							(보육료, 유치원 보조비, 바우처 이용금액 등), 포인트리 충전금액, 대학(대학원)등록금, 
							상품권 및 선불카드(선불전자지급수단 포함) 구입(충전)금액, 연체료, 지방세(상하수도, 세외수입 등), 취소금액, 각종 수수료 및 이자
						</li>
					</ul>
				</div>
			</div>
		</div>
	</section>
    <!-- 주요 혜택 확인 End -->
    
</body>

<style>
        .listgroup {
            margin-top: 14px;
        }

        .listgroup .benfLi
        {
            padding: 10px 16px;
            border-bottom: 1px solid #eee;
        }
        .listgroup .benfLi:last-child
        {
            border-bottom: 0;
        }
        .listgroup > li:not(.benfLi) > *:after {
            background: url('/mobweb/images_kiwi/icon/small_arrow.svg') no-repeat right 50%;
            content: "";
            display: inline-block;
            width: 24px;
            height: 24px;
        }
        .listgroup .benfLi > *:after {
            content: none !important;
        }
        .listgroup .benfLi .benfBtn
        {
            padding-left: 60px;
            background-repeat: no-repeat;
            background-image: url(/mobweb/images_kiwi/icon/ico_arr_r.svg);
            background-position: 100% 50%;
        }
        .listgroup .benfLi .benfBtn p
        {
            font-size: 14px;
        }
        .benfBtn>i
        {
            position: absolute;
            top: 50%;
            left: 0;
            width: 48px;
            height: 48px;
            background-repeat: no-repeat;
            background-size: cover;
            border-radius: 6px;
            -webkit-transform: translateY(-50%);
            transform: translateY(-50%);
        }
        .layer-btns>p
        {
            height: 2.75rem; 
            line-height: 2.75rem;
        }
        .layer-btns .move
        {
            width:calc((100% - 8px)/5); 
            float: left;
        }
        .benfHead
        {
            padding: 10px 0 0 0;
            text-align: center;
            font-size:1.125rem;
            background-color: #ffd338;
            color:#222222;
        }
        .benfHead>p
        {
            height: 2rem;
        }
        .benfBody
        {
            padding: 0 10px 0 10px;
            
        }
    
        .top-btn
        {
            display: flex;
            justify-content:space-between; 
        }
        .top-btn>button
        {
            width: 50px;
            height: 25px;
        }
</style>

</html>