/**
 * SBRateBot V5 Executive Dashboard JS
 * Part 1/3
 *
 * KPI + Woori Market Position
 */



/* ==========================================================
   GLOBAL DASHBOARD DATA
========================================================== */

let dashboardKPIData = {};

let wooriMarketData = {};



console.log(
    "🔥 DASHBOARD JS LOADED"
);



document.addEventListener(
    "DOMContentLoaded",
    () => {


        console.log(
            "🔥 DOM CONTENT LOADED"
        );


        initDashboard();


    }
);



/* ==========================================================
   DASHBOARD INITIALIZE
========================================================== */


function initDashboard() {


    console.log(
        "🔥 SBRateBot V5 Dashboard START"
    );



    /*
        KPI DATA
    */

    fetchKPI();




    /*
        WOORI MARKET POSITION
    */

    fetchWooriData();




    /*
        HERO SECTION
    */

    loadHero();




    /*
        AI SUMMARY
    */

    fetchAISummary();



}


/* ==========================================================
   Common API Fetch
========================================================== */

async function apiFetch(url) {

    try {

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(
                `API Error : ${response.status}`
            );
        }

        return await response.json();


    } catch(error) {

        console.error(
            "API Fetch Error:",
            url,
            error
        );

        return null;
    }
}



/* ==========================================================
   KPI SECTION
   /api/kpi

   V5 Executive Dashboard KPI Rendering
========================================================== */


async function fetchKPI() {


    const data =
        await apiFetch(
            "/api/kpi"
        );


    if(!data){

        return;

    }


    console.log(
        "KPI DATA",
        data
    );


    renderKPI(
        data
    );


}

/* ==========================================================
   AI MARKET SUMMARY
   /api/ai

   V5 Executive Dashboard
   AI 시장분석 현황
========================================================== */


async function fetchAISummary(){


    const data =
        await apiFetch(
            "/api/ai"
        );



    if(!data){

        return;

    }



    console.log(
        "AI SUMMARY DATA",
        data
    );



    const target =
        document.getElementById(
            "executive-summary-mini"
        );



    if(!target){

        return;

    }



    if(

        !Array.isArray(
            data.summary
        )

    ){

        target.innerHTML =
            "시장 데이터를 분석하는 중입니다.";

        return;

    }



    const summary =
        data.summary;



    /*
        AI 의견
        summary 마지막 2개 문장 사용
    */


        const aiOpinion =

        summary
            .slice(6)
            .join("<br>")
            .replace(
                /은행별 금리 경쟁 차이가 큰 시장으로|평균금리는 3% 이상으로/g,
                ""
            )
            .trim();



/* ==========================================================
   AI DETAIL MODAL CONTENT (COMPACT EXECUTIVE STYLE)
========================================================== */


const detailContent = `


<div class="space-y-2">



<!-- 시장 흐름 분석 -->

<div
class="
bg-blue-50
border
border-blue-100
rounded-lg
px-3
py-2
"
>


<div
class="
font-bold
text-blue-700
text-xs
mb-1
"
>
📈 시장 흐름 분석
</div>


<div
class="
text-gray-600
leading-5
"
>

${

    aiOpinion

    ||

    "시장 분석 데이터가 없습니다."

}

</div>


</div>






        <!-- 시장 현황 -->

        <div
        class="border border-gray-100 rounded-xl p-3"
        >


            <div
            class="font-bold text-gray-800 mb-3 text-sm"
            >

                📊 시장 현황

            </div>



            <div
            class="grid grid-cols-5 gap-2 text-center"
            >



                <div
                class="bg-gray-50 rounded-lg p-2"
                >

                    <div
                    class="text-[10px] text-gray-400"
                    >
                        상품수
                    </div>

                    <div
                    class="text-sm font-bold text-gray-800"
                    >
                        299개
                    </div>

                </div>





                <div
                class="bg-gray-50 rounded-lg p-2"
                >

                    <div
                    class="text-[10px] text-gray-400"
                    >
                        평균금리
                    </div>

                    <div
                    class="text-sm font-bold text-blue-700"
                    >
                        3.83%
                    </div>

                </div>





                <div
                class="bg-gray-50 rounded-lg p-2"
                >

                    <div
                    class="text-[10px] text-gray-400"
                    >
                        최고금리
                    </div>

                    <div
                    class="text-sm font-bold text-blue-700"
                    >
                        4.20%
                    </div>

                    <div
                    class="text-[9px] text-gray-400"
                    >
                        조은
                    </div>

                </div>





                <div
                class="bg-gray-50 rounded-lg p-2"
                >

                    <div
                    class="text-[10px] text-gray-400"
                    >
                        최저금리
                    </div>

                    <div
                    class="text-sm font-bold text-gray-700"
                    >
                        2.00%
                    </div>

                    <div
                    class="text-[9px] text-gray-400"
                    >
                        조은
                    </div>

                </div>





                <div
                class="bg-gray-50 rounded-lg p-2"
                >

                    <div
                    class="text-[10px] text-gray-400"
                    >
                        금리 스프레드
                    </div>

                    <div
                    class="text-sm font-bold text-orange-600"
                    >
                        2.20%p
                    </div>

                </div>



            </div>


        </div>




<!-- 우리금융 경쟁력 -->

<div
class="
bg-blue-50
border
border-blue-100
rounded-lg
px-3
py-2
"
>


<div
class="
font-bold
text-blue-700
text-xs
mb-2
"
>
🏦 우리금융 경쟁력 분석
</div>



<div
class="
grid
grid-cols-3
gap-2
text-center
"
>


<!-- 시장순위 -->

<div
class="
bg-white
rounded-lg
py-2
"
>

<div
class="text-[10px] text-gray-400"
>
시장순위
</div>


<div
class="
font-bold
text-blue-700
text-sm
"
>
${
wooriPositionData.market_rank
?
wooriPositionData.market_rank + "위"
:
"-"
}
</div>


</div>






<!-- 현재금리 -->

<div
class="
bg-white
rounded-lg
py-2
"
>

<div
class="text-[10px] text-gray-400"
>
현재금리
</div>


<div
class="
font-bold
text-gray-800
text-sm
"
>
${
wooriPositionData.best_rate
?
Number(
    wooriPositionData.best_rate
)
.toFixed(2)
+
"%"
:
"-"
}
</div>


</div>







<!-- 평균금리 대비 -->

<div
class="
bg-white
rounded-lg
py-2
"
>

<div
class="text-[10px] text-gray-400"
>
평균금리 대비
</div>


<div
class="
font-bold
text-sm
"
>


${

Number(
    wooriPositionData.avg_gap || 0
)
>= 0

?

`
<span class="text-blue-600">
+${Number(
    wooriPositionData.avg_gap
)
.toFixed(2)}%p
</span>
`

:

`

<span class="text-red-600">
▲${Math.abs(
Number(
    wooriPositionData.avg_gap
)
)
.toFixed(2)}%p
</span>

`

}


</div>


</div>




</div>


</div>








<!-- 체크포인트 -->

<div
class="
bg-yellow-50
border
border-yellow-100
rounded-lg
px-3
py-2
"
>


<div
class="
font-bold
text-yellow-700
text-xs
mb-1
"
>
⚠️ 주요 체크포인트
</div>


<div
class="
text-gray-600
leading-5
"
>

• 경쟁사 최고금리 변화 모니터링

<br>

• 금리 상승 기관 발생 여부 확인

<br>

• 시장 평균 대비 경쟁력 점검

</div>


</div>








<!-- AI 대응 전략 -->

<div
class="
bg-gray-50
border
border-gray-100
rounded-lg
px-3
py-2
"
>


<div
class="
font-bold
text-gray-800
text-xs
mb-1
"
>
🎯 AI 대응 전략
</div>


<div
class="
text-gray-600
leading-5
"
>

• 금리 경쟁력 유지 및 시장 변화 대응

<br>

• 경쟁사 금리 조정 시 즉시 검토

<br>

• 신규 상품 출시 가능성 점검

</div>


</div>








<!-- AI 종합 판단 -->

<div
class="
bg-amber-50
border
border-amber-100
rounded-lg
px-3
py-2
"
>


<div
class="
font-bold
text-amber-800
text-xs
mb-1
"
>
🤖 AI 종합 판단
</div>


<div
class="
text-gray-700
leading-5
"
>

우리금융은 시장 내 안정적인 경쟁력을 유지하고 있습니다.

<br>

경쟁사 금리 조정 및 신규 상품 출시 여부를 지속적으로 모니터링할 필요가 있습니다.

</div>


</div>



</div>


`;



    /* ==========================================================
       모달 내용 갱신
    ========================================================== */

    const modal =

        document.getElementById(
            "ai-detail-content"
        );


    if (modal) {

        modal.innerHTML = detailContent;

    }



        /*
        시장 데이터
    */


    const marketData = `


        <div class="text-xs text-gray-700 leading-5">


            <div class="mb-1 text-xs font-bold text-gray-800">

                📊 시장 현황

            </div>




            <div class="flex">


                <div class="flex-1">

                    ${summary[1] || ""}

                </div>



                <div class="flex-1">

                    ${summary[2] || ""}

                </div>



                <div class="flex-1">

                    ${summary[5] || ""}

                </div>


            </div>





            <div class="flex items-center mt-1">


                <div class="flex-1">

                    ${summary[3] || ""}

                </div>



                <div class="flex-1">

                    ${summary[4] || ""}

                </div>



                <div class="flex-1 text-right">


                    <button

                        id="ai-detail-btn"

                        class="text-xs text-blue-600 font-semibold hover:underline"

                    >

                        📊 AI 상세분석 보기 >

                    </button>


                </div>


            </div>



        </div>


    `;



    /*
        최종 출력
    */


    target.innerHTML = `


        <div class="mb-2">


            <div class="text-xs font-bold text-gray-800 mb-1">

                💡 AI 의견

            </div>



            <div class="text-xs text-gray-700 leading-5">


                ${

                    aiOpinion

                    ||

                    "시장 금리 흐름을 분석 중입니다."

                }


            </div>


        </div>





        <div class="border-t pt-2">


            ${marketData}


        </div>



    `;



}



function renderKPI(data){

    dashboardKPIData = data;



    /* ======================================================
       KPI DOM
    ====================================================== */


    const highestGap =
        document.getElementById(
            "kpi-highest-gap"
        );


    const lowestGap =
        document.getElementById(
            "kpi-lowest-gap"
        );


    const averageRate =
        document.getElementById(
            "kpi-average-rate"
        );


    const averageGap =
        document.getElementById(
            "kpi-average-gap"
        );


    const productCount =
        document.getElementById(
            "kpi-product-count"
        );


    const changeCount =
        document.getElementById(
            "kpi-change-count"
        );





    /* ======================================================
       최고금리 比
    ====================================================== */


    if(highestGap){


        const value =
            Number(
                data.highest_gap || 0
            );


        highestGap.innerHTML =
            value < 0
            ?
            `
            <span class="text-red-600">
            ▲${Math.abs(value).toFixed(2)}%p
            </span>
            `
            :
            `
            <span class="text-blue-600">
            +${value.toFixed(2)}%p
            </span>
            `;


    }






    /* ======================================================
       최저금리 比
    ====================================================== */


    if(lowestGap){


        const value =
            Number(
                data.lowest_gap || 0
            );


        lowestGap.innerHTML =
            value < 0
            ?
            `
            <span class="text-red-600">
            ▲${Math.abs(value).toFixed(2)}%p
            </span>
            `
            :
            `
            <span class="text-blue-600">
            +${value.toFixed(2)}%p
            </span>
            `;


    }






    /* ======================================================
       평균금리
    ====================================================== */


    if(averageRate){


        averageRate.innerHTML =
            data.average_rate !== undefined
            ?
            `${Number(data.average_rate).toFixed(2)}%`
            :
            "-";


    }






    /* ======================================================
       평균금리 比
    ====================================================== */


    if(averageGap){


        const value =
            Number(
                data.average_gap || 0
            );


        averageGap.innerHTML =
            value < 0
            ?
            `
            <span class="text-red-600">
            ▲${Math.abs(value).toFixed(2)}%p
            </span>
            `
            :
            `
            <span class="text-blue-600">
            +${value.toFixed(2)}%p
            </span>
            `;


    }






    /* ======================================================
       상품수
    ====================================================== */


    if(productCount){


        productCount.innerHTML =
            data.product_count !== undefined
            ?
            `${Number(data.product_count).toLocaleString()}개`
            :
            "-";


    }






    /* ======================================================
       금리변동수
    ====================================================== */


    if(changeCount){


        changeCount.innerHTML =
            data.change_count !== undefined
            ?
            `${Number(data.change_count)}건`
            :
            "0건";


    }






    updateTime(
        data.last_updated
    );


}







/* ==========================================================
   LAST UPDATED
========================================================== */


function updateTime(time){


    const target =
        document.getElementById(
            "last-updated"
        );



    if(!target){

        return;

    }





    if(time){


        target.innerHTML =
        `
        <i class="fa-regular fa-clock"></i>
        기준일시 : ${time}
        `;


    }


    else{


        const now =
            new Date()
            .toLocaleString(
                "ko-KR"
            );


        target.innerHTML =
        `
        <i class="fa-regular fa-clock"></i>
        ${now}
        `;


    }


}



/* ==========================================================
   WOORI MARKET POSITION
   /api/woori
========================================================== */


let wooriPositionData = {};



async function fetchWooriData(){


    const data =
        await apiFetch(
            "/api/woori"
        );


    if(!data){

        console.log(
            "WOORI DATA EMPTY"
        );

        return;

    }



    console.log(
        "🔥 WOORI API",
        data
    );



    wooriPositionData = data;



    renderWooriPosition(
        data
    );


}





function renderWooriPosition(data){

    console.log(
        "🔥 RENDER WOORI",
        data
    );


    const rank =
        document.getElementById(
            "woori-rank"
        );


    const rate =
        document.getElementById(
            "woori-rate"
        );


    const avgGap =
        document.getElementById(
            "woori-gap-average"
        );



    /*
        시장순위
    */

    if(rank){

        rank.innerHTML =
            data.market_rank
            ?
            `${data.market_rank}위`
            :
            "-";

    }



    /*
        현재금리
    */

    if(rate){

        rate.innerHTML =
            data.rate !== undefined
            ?
            `${Number(data.rate).toFixed(2)}%`
            :
            "-";

    }



    /*
        시장평균 대비
    */

    if(avgGap){


        const value =
            Number(
                data.average_gap ?? 0
            );


        if(
            value > 0
        ){

            avgGap.innerHTML =
            `
            <span class="text-blue-600 font-bold">
            +${value.toFixed(2)}%p
            </span>
            `;


        }
        else if(
            value < 0
        ){

            avgGap.innerHTML =
            `
            <span class="text-red-600 font-bold">
            ▲${Math.abs(value).toFixed(2)}%p
            </span>
            `;


        }
        else{


            avgGap.innerHTML =
            `
            <span class="text-gray-500">
            -
            </span>
            `;


        }


    }



}

/* ==========================================================
   TOP 10 RATE RANKING
   /api/rates
========================================================== */

async function fetchRatesData() {

    const select =
        document.getElementById(
            "top10-category-select"
        );

    let category = "ALL";

    if (select) {

        category =
            select.value;

    }

    const data =
        await apiFetch(
            `/api/rates?category=${category}`
        );

    if (!data) {
        return;
    }

    renderTop10(
        data.top10 || data
    );

}

function renderTop10(items) {

    const top5Body =
        document.getElementById(
            "top5-table-body"
        );

    const top10Body =
        document.getElementById(
            "top10-table-body"
        );

    if (!top5Body || !top10Body) {
        return;
    }

    top5Body.innerHTML = "";
    top10Body.innerHTML = "";

    if (!items || items.length === 0) {

        top5Body.innerHTML =
        `
        <tr>
            <td colspan="4" class="text-center py-4 text-gray-400">
                데이터 없음
            </td>
        </tr>
        `;

        top10Body.innerHTML =
        `
        <tr>
            <td colspan="4" class="text-center py-4 text-gray-400">
                데이터 없음
            </td>
        </tr>
        `;

        return;

    }

    items
        .slice(0, 10)
        .forEach((item, index) => {

            const tr =
                document.createElement("tr");

            const bank =
                item.kor_co_nm ||
                item.bank_name ||
                "-";

            const rate =
                item.intr_rate2 ??
                item.max_rate ??
                item.intr_rate ??
                item.base_rate ??
                "-";

            const diff =
                item.diff ??
                item.change ??
                "-";

            tr.innerHTML =
            `
            <td class="py-2">

                ${index + 1}

            </td>

            <td class="py-2">

                ${bank}

            </td>

            <td class="py-2 text-right font-semibold text-blue-600">

                ${
                    rate !== "-"
                    ? Number(rate).toFixed(2) + "%"
                    : "-"
                }

            </td>

            <td class="py-2 text-right">

                ${diff}

            </td>
            `;

            if (index < 5) {

                top5Body.appendChild(
                    tr
                );

            } else {

                top10Body.appendChild(
                    tr
                );

            }

        });

}




/* ==========================================================
   상승 / 하락 TOP5
   /api/financial
========================================================== */


async function fetchFinancialData(){


    const data =
        await apiFetch(
            "/api/financial"
        );


    if(!data){
        return;
    }


    renderRateChanges(

        data.up_top5 || [],

        data.down_top5 || []

    );


}



function renderRateChanges(
    upList,
    downList
){


    const up =
        document.getElementById(
            "rates-up-list"
        );


    const down =
        document.getElementById(
            "rates-down-list"
        );



    if(up){

        up.innerHTML="";


        if(upList.length===0){

            up.innerHTML =
            `
            <li class="empty-msg">
            변동 없음
            </li>
            `;

        }


        upList
        .slice(0,5)
        .forEach(item=>{


            const li =
                document.createElement(
                    "li"
                );


            li.className =
                "change-item";


            li.innerHTML =
            `

            <span>

            ${
            item.kor_co_nm ||
            item.bank_name ||
            "-"
            }

            <br>

            <small>

            ${
            item.fin_prdt_nm ||
            item.product_name ||
            ""

            }

            </small>

            </span>


            <strong class="status-up">

            +

            ${
            item.change_value ||
            (
            item.new_rate-item.old_rate
            )
            .toFixed(2)
            }

            %p

            </strong>


            `;


            up.appendChild(li);


        });


    }




    if(down){


        down.innerHTML="";



        if(downList.length===0){


            down.innerHTML =
            `
            <li class="empty-msg">
            변동 없음
            </li>
            `;

        }



        downList
        .slice(0,5)
        .forEach(item=>{


            const li =
                document.createElement(
                    "li"
                );


            li.className =
                "change-item";



            li.innerHTML =
            `

            <span>

            ${
            item.kor_co_nm ||
            item.bank_name ||
            "-"
            }


            <br>

            <small>

            ${
            item.fin_prdt_nm ||
            item.product_name ||
            ""

            }

            </small>


            </span>



            <strong class="status-down">


            ${
            item.change_value ||
            (
            item.new_rate-item.old_rate
            )
            .toFixed(2)
            }

            %p


            </strong>


            `;


            down.appendChild(li);


        });



    }


}




/* ==========================================================
   전체 상품 조회
   /api/products
========================================================== */


async function fetchAllProducts(
    keyword=""
){


    let url =
        "/api/products";


    if(keyword){

        url +=
        "?q="+
        encodeURIComponent(keyword);

    }



    const data =
        await apiFetch(url);



    if(!data){
        return;
    }



    renderAllProductsTable(

        data.products ||
        data.all_products ||
        []

    );



}



function renderAllProductsTable(
    products
){


    const tbody =
        document.getElementById(
            "all-products-table-body"
        );


    if(!tbody){
        return;
    }



    tbody.innerHTML="";



    if(products.length===0){

        tbody.innerHTML =
        `
        <tr>
        <td colspan="6"
        class="empty-msg">
        조회 상품 없음
        </td>
        </tr>
        `;


        return;

    }



    products.forEach(item=>{


        const tr =
            document.createElement(
                "tr"
            );


        tr.innerHTML =
        `

        <td>

        ${
        item.category ||
        item.type ||
        "예금"
        }

        </td>



        <td>

        ${
        item.kor_co_nm ||
        item.bank_name ||
        "-"
        }

        </td>



        <td>

        ${
        item.fin_prdt_nm ||
        item.product_name ||
        "-"
        }

        </td>



        <td>

        ${
        item.intr_rate !== undefined
        ?
        Number(item.intr_rate).toFixed(2)+"%"
        :
        item.base_rate
        ?
        Number(item.base_rate).toFixed(2)+"%"
        :
        "-"
        }

        </td>



        <td>

        <strong>

        ${
        item.intr_rate2 !== undefined
        ?
        Number(item.intr_rate2).toFixed(2)+"%"
        :
        item.max_rate
        ?
        Number(item.max_rate).toFixed(2)+"%"
        :
        "-"
        }


        </strong>

        </td>



        <td>

        ${
        item.save_trm ||
        item.period_months ||
        "-"
        }

        개월


        </td>


        `;



        tbody.appendChild(tr);


    });


}

/* ==========================================================
   Gemini AI Assistant
   /api/ai/search
========================================================== */


async function handleAISearch(event){


    event.preventDefault();



    const input =
        document.getElementById(
            "ai-query-input"
        );



    if(!input){
        return;
    }



    const query =
        input.value.trim();



    if(!query){
        return;
    }



    appendChatMessage(
        query,
        "user-message"
    );



    input.value="";



    const loading =
        appendChatMessage(
            "Gemini AI가 분석 중입니다...",
            "ai-message"
        );



    try{


        const response =
            await fetch(
                "/api/ai/search",
                {

                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },


                body:
                JSON.stringify({
                    query:query
                })

                }
            );



        const data =
            await response.json();



        removeChatMessage(
            loading
        );



        appendChatMessage(

            data.answer ||
            data.result ||
            "분석 결과가 없습니다.",

            "ai-message"

        );



    }

    catch(error){


        console.error(
            "AI Error:",
            error
        );


        removeChatMessage(
            loading
        );


        appendChatMessage(

            "AI 분석 요청 중 오류가 발생했습니다.",

            "ai-message"

        );


    }



}




/* ==========================================================
   Chat UI Helper
========================================================== */


function appendChatMessage(
    message,
    className
){


    const container =
        document.getElementById(
            "ai-chat-messages"
        );


    if(!container){
        return null;
    }



    const id =
        "chat-" + Date.now();



    const div =
        document.createElement(
            "div"
        );


    div.id=id;


    div.className =
        `chat-bubble ${className}`;



    div.textContent =
        message;



    container.appendChild(
        div
    );



    container.scrollTop =
        container.scrollHeight;



    return id;


}



function removeChatMessage(id){


    const target =
        document.getElementById(
            id
        );


    if(target){

        target.remove();

    }

}



/* ==========================================================
   상품 검색
========================================================== */


function setupProductSearch(){


    const input =
        document.getElementById(
            "product-search-input"
        );



    if(!input){
        return;
    }



    input.addEventListener(
        "keypress",

        e=>{


            if(e.key==="Enter"){


                fetchAllProducts(
                    input.value.trim()
                );


            }


        }

    );


}




/* ==========================================================
   Event Listener
========================================================== */


function setupEventListeners(){



    // TOP10 변경

    const category =
        document.getElementById(
            "top10-category-select"
        );



    if(category){


        category.addEventListener(
            "change",
            fetchRatesData
        );


    }





    // AI Search


    const aiForm =
        document.getElementById(
            "ai-search-form"
        );



    if(aiForm){


        aiForm.addEventListener(
            "submit",
            handleAISearch
        );


    }




    // 상품 검색


    setupProductSearch();



}




/* ==========================================================
   Dashboard Final Initialize
========================================================== */


window.addEventListener(
    "load",

    ()=>{


        fetchFinancialData();


        fetchAllProducts();



    }

);

/* ======================================================
   HERO 시장경쟁력 데이터 로딩
====================================================== */

async function loadHero(){

    try {

        const res = await fetch("/api/woori");

        const data = await res.json();


        // 시장순위

        const rank =
            document.getElementById("kpi-rank");


        if(rank){

            rank.innerHTML =
                `${data.market_rank || "-"}`;

        }



        // 우리금융 금리

        const wooriRate =
            document.getElementById("kpi-woori-rate-mini");


        if(wooriRate){

            wooriRate.innerText =
                data.rate
                ? `${Number(data.rate).toFixed(2)}%`
                : "-";

        }



        // 업권 최고금리

        const bestRate =
            document.getElementById("kpi-best-rate-mini");


        if(bestRate){

            const gap =
                Number(data.highest_gap || 0);


            const best =
                Number(data.rate || 0) - gap;


            bestRate.innerText =
                best
                ? `${best.toFixed(2)}%`
                : "-";

        }



                // 업권 최저금리

        const heroLowest =
            document.getElementById(
                "kpi-lowest-rate-mini"
            );


        if(heroLowest){

            const lowestRate =
                Number(
                    data.lowest_rate || 0
                );


            if(lowestRate > 0){

                heroLowest.innerText =
                    `${lowestRate.toFixed(2)}%`;

                heroLowest.className =
                    "text-sm font-bold";

            }


            else{

                heroLowest.innerText =
                    "-";

            }

        }



    }
    catch(error){

        console.error(
            "Hero 데이터 로딩 오류:",
            error
        );

    }

}


/* ==========================================================
   AI DETAIL MODAL + HOVER PREVIEW
========================================================== */


document.addEventListener(
    "click",
    function(e){


       /*
    상세 분석 버튼 클릭
*/


const btn =
    e.target.closest(
        "#ai-detail-btn"
    );


if(btn){


    console.log(
        "AI DETAIL BUTTON CLICK"
    );



    /*
        클릭 순간 우리금융 데이터 재조회
    */


    fetch(
        "/api/woori"
    )


    .then(
        response =>
            response.json()
    )


    .then(
        data => {


            console.log(
                "DETAIL WOORI DATA",
                data
            );



            /*
                상세분석 전용 데이터 저장
            */


            wooriPositionData =
                data;



            /*
                상세내용 다시 생성
            */


            if(
                typeof renderAIDetailModal === "function"
            ){


                renderAIDetailModal();


            }





            /*
                모달 열기
            */


            const modal =
                document.getElementById(
                    "ai-detail-modal"
                );



            if(modal){


                modal.classList.remove(
                    "hidden"
                );


                modal.classList.add(
                    "flex"
                );


            }


        }

    )


    .catch(
        error => {


            console.error(
                "WOORI DETAIL ERROR",
                error
            );


        }
    );


}




        /*
            모달 닫기
        */


        const close =
            e.target.closest(
                "#ai-detail-close"
            );



        if(close){


            const modal =
                document.getElementById(
                    "ai-detail-modal"
                );



            if(modal){


                modal.classList.add(
                    "hidden"
                );


                modal.classList.remove(
                    "flex"
                );


                console.log(
                    "AI DETAIL MODAL CLOSE"
                );


            }


        }


    }
);








/* ==========================================================
   AI DETAIL HOVER PREVIEW
========================================================== */


document.addEventListener(
    "mouseover",
    function(e){


        const btn =
            e.target.closest(
                "#ai-detail-btn"
            );



        if(!btn){

            return;

        }





        let preview =
            document.getElementById(
                "ai-detail-preview"
            );



        if(!preview){


            preview =
                document.createElement(
                    "div"
                );



            preview.id =
                "ai-detail-preview";



            preview.className =
                `
                fixed
                z-[9999]
                w-80
                bg-white
                border
                border-blue-100
                rounded-xl
                shadow-xl
                p-4
                text-xs
                text-gray-700
                `;



            preview.innerHTML =
`

<div class="flex items-center justify-between mb-3">

    <div class="font-bold text-blue-700">

        📊 AI 상세 분석 미리보기

    </div>


    <span class="text-[10px] text-gray-400">

        AI Insight

    </span>

</div>



<div class="space-y-3 text-gray-700">



    <div>

        <div class="font-bold text-gray-800 mb-1">

            📈 시장 흐름

        </div>


        <div class="text-[11px] leading-5">

            저축은행 금리 경쟁이 지속되고 있으며

            평균금리 수준과 최고금리 변화를

            지속적으로 모니터링하고 있습니다.

        </div>


    </div>





    <div class="border-t pt-2">


        <div class="font-bold text-gray-800 mb-1">

            🏦 우리금융 경쟁력

        </div>


        <div class="text-[11px] leading-5">

            우리금융은 시장 평균 대비

            경쟁력을 유지하고 있으며

            주요 경쟁사 대비 금리 포지션을

            지속 관리할 필요가 있습니다.

        </div>


    </div>





    <div class="border-t pt-2">


        <div class="font-bold text-gray-800 mb-1">

            ⚠️ 주요 체크포인트

        </div>


        <div class="text-[11px] leading-5">

            • 최고금리 상품 변동 여부 확인

            <br>

            • 경쟁사 금리 상승 여부 모니터링

            <br>

            • 신규 상품 출시 영향 분석

        </div>


    </div>



</div>


<div
class="mt-3 pt-2 border-t text-[10px] text-blue-600 text-right"
>

상세 분석에서 전체 내용을 확인하세요 →

</div>


`;



            document.body.appendChild(
                preview
            );


        }





        /*
            AI 표시 내용 연결
        */


        const content =
            document.getElementById(
                "ai-preview-content"
            );



        if(content){



            const summary =
                document.querySelector(
                    "#executive-summary-mini"
                );



            const answer =
                document.querySelector(
                    "#ai-mini-answer"
                );



            let text =
                "";



            if(
                summary
                &&
                summary.innerText.trim()
            ){


                text =
                    summary.innerText;


            }
            else if(
                answer
                &&
                answer.innerText.trim()
            ){


                text =
                    answer.innerText;


            }
            else{


                text =
                    `
                    시장 데이터를 기반으로
                    AI 분석을 준비 중입니다.
                    `;


            }



            content.innerHTML =
                text.replace(
                    /\n/g,
                    "<br>"
                );


        }







        /*
            위치 계산
        */


        const rect =
            btn.getBoundingClientRect();



        preview.style.left =
            rect.left
            +
            "px";



        preview.style.top =
            (
                rect.bottom
                +
                8
            )
            +
            "px";



        preview.style.display =
            "block";



    }
);









/* ==========================================================
   AI DETAIL HOVER OUT
========================================================== */


document.addEventListener(
    "mouseout",
    function(e){


        const btn =
            e.target.closest(
                "#ai-detail-btn"
            );



        if(!btn){

            return;

        }



        const preview =
            document.getElementById(
                "ai-detail-preview"
            );



        if(preview){


            preview.style.display =
                "none";


        }


    }
);

/* ==========================================================
   AI DETAIL CLICK TEST
========================================================== */

document.addEventListener(
    "click",
    function(e){

        const btn =
            e.target.closest(
                "#ai-detail-btn"
            );


        if(btn){

            console.log(
                "🔥 AI DETAIL CLICK TEST OK"
            );

        }

    }
);