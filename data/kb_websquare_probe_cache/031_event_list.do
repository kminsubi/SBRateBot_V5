
<!DOCTYPE html>
<html lang="ko">

<head>
<title>이벤트</title>











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

<!-- header Start -->	

		<!-- header에 표시-->
      <!-- header에 뒤로가기가 필요 없을 시 N 셋팅 (디폴트 Y 는 뒤로가기 보임)-->
    	
	
<header class="fixed">
	<div class="inner-wrap">
		<h1 class="sr-only">이벤트</h1>
		<h2 class="page-title" id="pa2">이벤트</h2>
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
		if ('Y' === 'Y' || existNull('')) {
			location.href = ctx + '/main.do';
		} else {
			UI.layerPop('#backPage');
		}
	}
	function goBackProd() {
		location.href = '' == '' ? ctx + '/main.do' : '';
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

<!-- header End -->	
	
	
	<script type="text/javascript" src="../../js_kiwi/jquery.scrollLock.js"></script>
	
	
<script type="text/javascript">

$(document).ready(function(){
	//AppAlert("");
	if("" == 2){
		$('#closeEvent').click();
	}
	
	$('#tab_type1').addClass('active');
	
}); //end ready
$(window).scroll(function() {
	
	var currentPage = 1;
	var _height = $(document).height() - $(window).height();			
	var _top = parseInt($(window).scrollTop());
	var _gap = _height - _top;
	
	if(_gap <= 56   && !$("body").hasClass('modal-open')){
	//if(parseInt($(window).scrollTop()) == $(document).height() - $(window).height()){
		if($("#type").val() == 2){
			if(parseInt($('#dpageNum').val()) < parseInt($('#dTOT_PAGE_NUM').val())){
				goMoreDeadEventDet();	
			}
		}else{
			if(parseInt($('#lpageNum').val()) < parseInt($('#lTOT_PAGE_NUM').val())){
				goMoreLiveEventDet();	
			}
		}
	}
});

function goMoreLiveEventDet(){
	var nextpage = $("#lpageNum").val();
	if( nextpage == "0"){
		nextpage = "1";
	}else{
		nextpage = parseInt(nextpage) + 1;
	}
	$("#lpageNum").val(nextpage);
	$("#lpageSize").val("20");
	$.ajax({
		url : ctx + "/kiwicustomer/getLiveEventListAjax.do",
		type : "post",
		async : true,
		data : $("#livefrm").serialize(),
		dataType : 'json',
		success : function( res) {
			var html = "";
			if(res.liveEvent.length != 0){
				var today = new Date();
				var todayN = textDate2(dateadd(today, -7, "d"));
				var regDttiN = "";
				var regDtti = "";
				for (var i = 0; i < res.liveEvent.length; i++) {
					regDttiN = res.liveEvent[i].MOD_DTTI;
					regDtti = regDttiN;		
					html += '<li> ';
					html += '<div class="event-wrap">';
					html += '<a href="/mobweb/kiwicustomer/event_detail.do?type=1&EVT_NO=' + res.liveEvent[i].EVT_NO + '" class="btn-detail-view">';
					html += '<span class="sr-only">상세보기</span>';
					html += ' <div class="text-info">';
					html += '<p class="text-desc">' + res.liveEvent[i].EVT_TTL_NM + '</p>';
					html += '<span class="text-date">' + res.liveEvent[i].EVT_ST_DT + ' ~ ' + res.liveEvent[i].EVT_ED_DT + '</span>';
					if (todayN <= regDttiN) {
						html += '<small>';
						html += '<span class="event-new">';
						html += '</small>';
					}
					html += '</div>';
					html += '<div class="img">';
					html += '<img src="/mobweb' + res.liveEvent[i].CONN_URL_ADDRB + res.liveEvent[i].FILE_NMB + '" alt="' + res.liveEvent[i].EVT_TTL_NM + '">';
					html += '</div>';
					html += '</a>';
					html += '</div>';
					html += '</li>';
				}
			}
			$("#live_list").append(html);
		},
		error : function(data, status, err) {
			//setEnableSubmitFlag();
			alert("시스템 또는 네트워크 오류로 \n실패하였습니다.");
			return false;
		}
	});
}

function goMoreDeadEventDet(){
	var nextpage = $("#dpageNum").val();
	if( nextpage == "0"){
		nextpage = "1";
	}else{
		nextpage = parseInt(nextpage) + 1;
	}
	$("#dpageNum").val(nextpage);
	$("#dpageSize").val("20");
	$.ajax({
		url : ctx + "/kiwicustomer/getDeadEventListAjax.do",
		type : "post",
		async : true,
		data : $("#deadfrm").serialize(),
		dataType : 'json',
		success : function( res) {
			var html = "";
			if(res.deadEvent.length != 0){
				var today = new Date();
				var todayN = textDate2(dateadd(today, -7, "d"));
				var regDttiN = "";
				var regDtti = "";
				
				for (var i = 0; i < res.deadEvent.length; i++) {
					html += '<li class="per-end">';
					html += '<div class="event-wrap">';
					html += '<a href="/mobweb/kiwicustomer/event_detail.do?type=2&EVT_NO=' + res.deadEvent[i].EVT_NO + '" class="per-end-text">이벤트가 종료되었어요';
					html += '<a  class="bgcolor-1">';
					html += '<span class="sr-only">상세보기</span>';
					html += '<div class="text-info">';
					html += '<p class="text-desc">' + res.deadEvent[i].EVT_TTL_NM;
					html += '<span class="text-date">';
					html += res.deadEvent[i].EVT_ST_DT + ' ~ ' + res.deadEvent[i].EVT_ED_DT + '</span>';
					html += '</p>';
					html += '</div>';
					html += '<div class="img">';
					html += '<img src="/mobweb' + res.deadEvent[i].CONN_URL_ADDRB + res.deadEvent[i].FILE_NMB + '" alt="' + res.deadEvent[i].EVT_TTL_NM + '">';
					html += '</div>';
					html += '</a>';
					html += '</a>';
					html += '</div>';

					if (res.deadEvent[i].PRZ_EXPR_YN == 'Y') {
						html += '<div class="contents-btns">';
						html += '<a class="winner-view" href="/mobweb/kiwicustomer/event_result.do?type=2&EVT_NO=' + res.deadEvent[i].EVT_NO + '">당첨자 확인</a>';
						html += '</div>';
					}
					html += '</li>';

				}
			}
			$("#dead_list").append(html);
		},
		error : function(data, status, err) {
			//setEnableSubmitFlag();
			alert("시스템 또는 네트워크 오류로 \n실패하였습니다.");
			return false;
		}
	});
}

function setType(type){
	$("#type").val(type);
}

function getNews(url){

	location.href = ctx + url;
}

</script>
<!-- header End -->	
</head>
<body>
	<div class="wrapper" id="wrapper">
		<!-- container -->
		<div id="container">
			<div id="contents" class="event-page fixed-bottom">
				<section class="pd-h">
					<h1 class="head-copy">이벤트</h1>
					<!-- 배너 소스 -->
					 <div class="event-banner-wrap">
						<section class="swiper-container event-swiper-banner" data-autoplay="true" data-arrow="false">
							<!-- 2020-03-31 data-arrow="false" data-paging="true" 삭제 -->
							<!-- 배너 본문 -->
							<div class="swiper-wrapper">
								
									
										<div class="swiper-slide">
											<div class="event-section">
												<span class="event-img">
													<img src="/mobweb/images_kiwi/bnr/9cec824b72e647468dd92442a7a4acf8.png"
														alt="KB저축은행 팡팡KB체크카드<br> 2만원 캐시백 이벤트">
												</span>
												<div class="event-detail sr-only">
													<small>2026.07.01 ~ 2026.08.31
														
													</small>
													<!-- 2020-06-10 new 아이콘 추가 -->
													
														<p class="text">KB저축은행 팡팡KB체크카드<br> 2만원 캐시백 이벤트</p>
													
												</div>

												<a href="/mobweb/kiwicustomer/event_detail.do?type=1&EVT_NO=1241"
													class="btn-detail-view">
													<span class="sr-only">상세보기</span>
												</a>

											</div>
											<!-- //event-section -->
										</div>
									
								
									
										<div class="swiper-slide">
											<div class="event-section">
												<span class="event-img">
													<img src="/mobweb/images_kiwi/bnr/f26b0b90bcfd4bfb97ba8e7f7c469421.jpg"
														alt="kiwi멤버십 이벤트">
												</span>
												<div class="event-detail sr-only">
													<small>2026.01.01 ~ 2027.01.31
														
													</small>
													<!-- 2020-06-10 new 아이콘 추가 -->
													
														<p class="text">kiwi멤버십 이벤트</p>
													
												</div>

												<a href="/mobweb/kiwicustomer/event_detail.do?type=1&EVT_NO=1225"
													class="btn-detail-view">
													<span class="sr-only">상세보기</span>
												</a>

											</div>
											<!-- //event-section -->
										</div>
									
								
								<!-- //swiper-slide -->

							</div>
							<!-- //배너 본문 -->
						</section>
					</div>
					<!-- //배너 소스 -->
					<div class="ui-tab ">
						<div class="tab-menu type2 sticky-top">
							<ul>
								
								
									<li id="tab_type1" class="active">
								
								<button type="button" onclick="setType(1)">
									<span>진행중인 이벤트</span>
								</button>
								</li>
								
								
									<li>
								
								<button type="button" id="closeEvent" onclick="setType(2)">
									<span>종료된 이벤트</span>
								</button>
								</li>
							</ul>
						</div>
						<div class="tab-container type2">
							<div class="tab-contents active ">
								<div class="event-list">
									<ul class="event-item" id="live_list">
										
											<li>
												<div class="event-wrap">
													<a href="/mobweb/kiwicustomer/event_detail.do?EVT_NO=1241&type=1" class="bgcolor-1">
														<span class="sr-only">상세보기</span>
													<div class="text-info">
														
														
														
															<!-- 2020-06-10 new 아이콘 추가 -->
															<p class="text-desc">KB저축은행 팡팡KB체크카드<br> 2만원 캐시백 이벤트</p>
														
														<span class="text-date">2026.07.01 ~ 2026.08.31</span>
													</div>
													<div class="img">
														<img src="/mobweb/images_kiwi/bnr/011647a74d8c4bdbb069635ab4b08f19.png"
															alt="KB저축은행 팡팡KB체크카드<br> 2만원 캐시백 이벤트">
													</div>
													</a>
												</div>
											</li>
										
											<li>
												<div class="event-wrap">
													<a href="/mobweb/kiwicustomer/event_detail.do?EVT_NO=1225&type=1" class="bgcolor-2">
														<span class="sr-only">상세보기</span>
													<div class="text-info">
														
														
														
															<!-- 2020-06-10 new 아이콘 추가 -->
															<p class="text-desc">kiwi멤버십 이벤트</p>
														
														<span class="text-date">2026.01.01 ~ 2027.01.31</span>
													</div>
													<div class="img">
														<img src="/mobweb/images_kiwi/bnr/f36ea564ec644032b458078fb79b0645.png"
															alt="kiwi멤버십 이벤트">
													</div>
													</a>
												</div>
											</li>
										
									</ul>
								</div>
								<!-- //event-list -->
							</div>

							<div class="tab-contents">
								<div class="event-list">
									<ul class="event-item" id="dead_list">
										
											<li class="per-end">
												<div class="event-wrap">
													<a href="/mobweb/kiwicustomer/event_detail.do?EVT_NO=1235&type=2" class="per-end-text">이벤트가 종료되었어요
														<a
															class="bgcolor-1">
															<span class="sr-only">상세보기</span>
													<div class="text-info">
														
														
															<!-- 2020-06-10 new 아이콘 추가 -->
															<p class="text-desc">대출한도조회 참여만해도<br>네이버페이 2만원권 증정!<br>(추첨 100명)</p>
														
														<span class="text-date">2026.06.15 ~ 2026.07.31</span>
													</div>
													<div class="img">
														<img src="/mobweb/images_kiwi/bnr/0dbce4c5709e4838b7d59a3de9a47914.png"
															alt="대출한도조회 참여만해도<br>네이버페이 2만원권 증정!<br>(추첨 100명)">
													</div>
													</a>
													</a>
												</div>
												<!-- 2020.04.27 부모요소 추가 및 버튼 수정-->
												
											</li>
										
											<li class="per-end">
												<div class="event-wrap">
													<a href="/mobweb/kiwicustomer/event_detail.do?EVT_NO=1229&type=2" class="per-end-text">이벤트가 종료되었어요
														<a
															class="bgcolor-2">
															<span class="sr-only">상세보기</span>
													<div class="text-info">
														
														
															<!-- 2020-06-10 new 아이콘 추가 -->
															<p class="text-desc">KB저축은행 팡팡KB체크카드<br>최대 3만원 캐시백 이벤트</p>
														
														<span class="text-date">2026.05.04 ~ 2026.06.30</span>
													</div>
													<div class="img">
														<img src="/mobweb/images_kiwi/bnr/011647a74d8c4bdbb069635ab4b08f19.png"
															alt="KB저축은행 팡팡KB체크카드<br>최대 3만원 캐시백 이벤트">
													</div>
													</a>
													</a>
												</div>
												<!-- 2020.04.27 부모요소 추가 및 버튼 수정-->
												
											</li>
										
											<li class="per-end">
												<div class="event-wrap">
													<a href="/mobweb/kiwicustomer/event_detail.do?EVT_NO=1232&type=2" class="per-end-text">이벤트가 종료되었어요
														<a
															class="bgcolor-3">
															<span class="sr-only">상세보기</span>
													<div class="text-info">
														
														
															<!-- 2020-06-10 new 아이콘 추가 -->
															<p class="text-desc">kiwi팡팡통장 신규 가입하면<br>네이버페이 1만원권 증정!<br>(추첨 200명)</p>
														
														<span class="text-date">2026.06.01 ~ 2026.06.30</span>
													</div>
													<div class="img">
														<img src="/mobweb/images_kiwi/bnr/d9ac37a3413d4916883fa42bb7697bb6.png"
															alt="kiwi팡팡통장 신규 가입하면<br>네이버페이 1만원권 증정!<br>(추첨 200명)">
													</div>
													</a>
													</a>
												</div>
												<!-- 2020.04.27 부모요소 추가 및 버튼 수정-->
												
											</li>
										
											<li class="per-end">
												<div class="event-wrap">
													<a href="/mobweb/kiwicustomer/event_detail.do?EVT_NO=1223&type=2" class="per-end-text">이벤트가 종료되었어요
														<a
															class="bgcolor-4">
															<span class="sr-only">상세보기</span>
													<div class="text-info">
														
														
															<!-- 2020-06-10 new 아이콘 추가 -->
															<p class="text-desc">KB저축은행에서 대출받으면<br>팡팡포인트 3만P 드려요!<br>(추첨100명)</p>
														
														<span class="text-date">2026.02.09 ~ 2026.03.31</span>
													</div>
													<div class="img">
														<img src="/mobweb/images_kiwi/bnr/7c276c5df1fb42f0a712e93e0207a5f6.png"
															alt="KB저축은행에서 대출받으면<br>팡팡포인트 3만P 드려요!<br>(추첨100명)">
													</div>
													</a>
													</a>
												</div>
												<!-- 2020.04.27 부모요소 추가 및 버튼 수정-->
												
											</li>
										
									</ul>
								</div>
							</div>
						</div>
					</div>
				</section>
			</div>
		</div>
	</div>
	<!-- 레이어 팝업 -->
	<!-- //레이어 팝업 -->
	<input type="hidden" id="type" 		name="type" value=""/>
	<form id="livefrm" method="POST">
		<input type="hidden" id="lpageNum" 		name="pageNum" value="1"/>
		<input type="hidden" id="lpageSize"		name="pageSize" />	
		<input type="hidden" id="lTOT_PAGE_NUM" 		name="TOT_PAGE_NUM" value="1"/>	
	</form>
	<form id="deadfrm" method="POST">
		<input type="hidden" id="dpageNum" 		name="pageNum" value="1"/>
		<input type="hidden" id="dpageSize"		name="pageSize" />	
		<input type="hidden" id="dTOT_PAGE_NUM" 		name="TOT_PAGE_NUM" value="3"/>	
	</form>
</body>


</html>