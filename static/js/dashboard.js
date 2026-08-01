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

window.sbLastAIQuestion = window.sbLastAIQuestion || "";
window.sbLastAIAnswer = window.sbLastAIAnswer || "";



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


    /*
        WIBEE AI BRIEFING
    */

    fetchWibeeBriefing();


    /*
        MARKET TOP10
    */

    fetchRatesData();


    /*
        RATE CHANGE TOP5
    */

    fetchFinancialData();


    /*
        UI EVENT BINDING
    */

    setupEventListeners();


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


    const [data, kpiData, freshWooriData] = await Promise.all([
        apiFetch("/api/ai"),
        apiFetch("/api/kpi"),
        apiFetch("/api/woori")
    ]);

    if(!data){
        return;
    }

    const marketKpi = kpiData || {};
    const marketWoori = freshWooriData || wooriPositionData || {};



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
                        ${Number(marketKpi.product_count || 0).toLocaleString()}개
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
                        ${Number(marketKpi.average_rate || 0).toFixed(2)}%
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
                        ${Number(marketKpi.max_rate || 0).toFixed(2)}%
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
                        ${Number(marketKpi.min_rate || 0).toFixed(2)}%
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
                        ${(Number(marketKpi.max_rate || 0) - Number(marketKpi.min_rate || 0)).toFixed(2)}%p
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
marketWoori.market_rank
?
marketWoori.market_rank + "위"
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
marketWoori.rate
?
Number(
    marketWoori.rate
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
    marketWoori.average_gap || 0
)
>= 0

?

`
<span class="text-blue-600">
+${Number(
    marketWoori.average_gap
)
.toFixed(2)}%p
</span>
`

:

`

<span class="text-red-600">
▲${Math.abs(
Number(
    marketWoori.average_gap
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
            "market-detail-content"
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

                        id="market-detail-btn"

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
   WIBEE AI BRIEFING
   /api/kpi + /api/woori
========================================================== */

async function fetchWibeeBriefing(){

    const [kpi, woori, changes] = await Promise.all([
        apiFetch("/api/kpi"),
        apiFetch("/api/woori"),
        apiFetch("/api/rate-changes")
    ]);

    if(!kpi || !woori){
        return;
    }

    renderWibeeBriefing(kpi, woori, changes || {});
}


function renderWibeeBriefing(kpi, woori, changes = {}){

    const status = document.getElementById("wibee-market-status");
    const judgementEl = document.getElementById("wibee-judgement");
    const riseEl = document.getElementById("wibee-rise-count");
    const fallEl = document.getElementById("wibee-fall-count");
    const changeEl = document.getElementById("wibee-change-count");
    const wooriRateEl = document.getElementById("wibee-woori-rate");
    const rankEl = document.getElementById("wibee-rank");
    const bestRateEl = document.getElementById("wibee-best-rate");
    const averageRateEl = document.getElementById("wibee-average-rate");

    const gap = Number(woori.average_gap ?? kpi.average_gap ?? 0);
    const changeCount = Number(
        changes.change_count ??
        changes.total_change_count ??
        kpi.change_count ??
        0
    );
    const riseCount = Number(
        changes.up_count ??
        changes.rise_count ??
        (Array.isArray(changes.up_all) ? changes.up_all.length : 0)
    );
    const fallCount = Number(
        changes.down_count ??
        changes.fall_count ??
        (Array.isArray(changes.down_all) ? changes.down_all.length : 0)
    );

    let marketStatus = "안정";
    let dotClass = "bg-emerald-500";
    let textClass = "text-emerald-600";

    if(changeCount >= 120){
        marketStatus = "변동 확대";
        dotClass = "bg-orange-500";
        textClass = "text-orange-600";
    }
    else if(changeCount >= 80){
        marketStatus = "변동 관찰";
        dotClass = "bg-amber-400";
        textClass = "text-amber-600";
    }

    if(status){
        status.className = `inline-flex items-center gap-1 ${textClass}`;
        status.innerHTML = `<span class="w-2 h-2 rounded-full ${dotClass}"></span>${marketStatus}`;
    }

    if(riseEl){ riseEl.textContent = Number.isFinite(riseCount) ? riseCount : 0; }
    if(fallEl){ fallEl.textContent = Number.isFinite(fallCount) ? fallCount : 0; }
    if(changeEl){ changeEl.textContent = Number.isFinite(changeCount) ? changeCount : 0; }

    const wooriRate = Number(woori.rate ?? woori.best_rate ?? 0);
    const bestRate = Number(kpi.max_rate ?? kpi.highest_rate ?? 0);
    const averageRate = Number(kpi.average_rate ?? kpi.avg_rate ?? 0);
    const rank = woori.market_rank ?? woori.rank ?? "-";
    const total = woori.market_total ?? woori.total ?? "-";

    if(wooriRateEl){
        wooriRateEl.textContent = Number.isFinite(wooriRate) && wooriRate > 0 ? `${wooriRate.toFixed(2)}%` : "-";
    }
    if(bestRateEl){
        bestRateEl.textContent = Number.isFinite(bestRate) && bestRate > 0 ? `${bestRate.toFixed(2)}%` : "-";
    }
    if(averageRateEl){
        averageRateEl.textContent = Number.isFinite(averageRate) && averageRate > 0 ? `${averageRate.toFixed(2)}%` : "-";
    }
    if(rankEl){
        rankEl.textContent = rank !== "-" ? `${rank}위 / ${total}` : "-";
    }

    if(judgementEl){
        let judgement = "시장 평균 수준의 금리 경쟁이 이어지고 있습니다.";
        if(gap < -0.20){
            judgement = "우리금융은 시장평균을 하회해 상위권과의 금리 격차 점검이 필요합니다.";
        }
        else if(gap < 0){
            judgement = "우리금융은 시장평균을 소폭 하회하며 최고금리 중심의 경쟁을 모니터링할 필요가 있습니다.";
        }
        else if(gap > 0.20){
            judgement = "우리금융은 시장평균을 뚜렷하게 상회하며 높은 금리 경쟁력을 유지하고 있습니다.";
        }
        else if(gap > 0){
            judgement = "우리금융은 시장평균을 소폭 상회하며 안정적인 금리 경쟁력을 유지하고 있습니다.";
        }
        judgementEl.textContent = judgement;
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

    if (!Array.isArray(items) || items.length === 0) {

        const emptyRow = `
        <tr>
            <td colspan="4" class="text-center py-4 text-gray-400">
                데이터 없음
            </td>
        </tr>
        `;

        top5Body.innerHTML = emptyRow;
        top10Body.innerHTML = emptyRow;
        return;
    }

    items
        .slice(0, 10)
        .forEach((item, index) => {

            const tr = document.createElement("tr");

            const bank =
                item.kor_co_nm ||
                item.bank_name ||
                item.bank ||
                "-";

            const rate =
                item.intr_rate2 ??
                item.max_rate ??
                item.intr_rate ??
                item.base_rate ??
                item.rate ??
                null;

            const rawDiff =
                item.diff ??
                item.change ??
                item.change_value ??
                0;

            const diffValue = Number(rawDiff);
            let diffHtml = '<span class="text-gray-400">-</span>';

            if(!Number.isNaN(diffValue) && diffValue > 0){
                diffHtml = `<span class="text-blue-600">+${diffValue.toFixed(2)}%p</span>`;
            }
            else if(!Number.isNaN(diffValue) && diffValue < 0){
                diffHtml = `<span class="text-red-500">▲${Math.abs(diffValue).toFixed(2)}%p</span>`;
            }
            else if(typeof rawDiff === "string" && rawDiff.trim() && rawDiff !== "-"){
                diffHtml = rawDiff;
            }

            const isWoori = String(bank).includes("우리금융");

            if(isWoori){
                tr.className = "bg-blue-50/80 font-bold text-blue-700 [box-shadow:inset_0_0_0_1px_#bfdbfe]";
            }

            const rankClass = index < 3
                ? "bg-orange-100 text-orange-600"
                : isWoori
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-600";

            tr.innerHTML = `
            <td class="py-2 text-center">
                <span class="${rankClass} w-4 h-4 rounded-full inline-flex items-center justify-center text-[10px] font-bold">
                    ${index + 1}
                </span>
            </td>
            <td class="py-2 text-center truncate px-1" title="${bank}">${bank}</td>
            <td class="py-2 text-center font-semibold ${isWoori ? "text-blue-700" : "text-blue-600"}">
                ${rate !== null && !Number.isNaN(Number(rate)) ? Number(rate).toFixed(2) + "%" : "-"}
            </td>
            <td class="py-2 text-center font-semibold whitespace-nowrap">
                ${diffHtml}
            </td>
            `;

            if (index < 5) {
                top5Body.appendChild(tr);
            }
            else {
                top10Body.appendChild(tr);
            }

        });
}



/* ==========================================================
   시장 전체 순위 MODAL
========================================================== */

async function openAllRatesModal(){

    const modal = document.getElementById("top10-all-modal");
    const tbody = document.getElementById("top10-all-table-body");

    if(!modal || !tbody){
        return;
    }

    modal.classList.remove("hidden");
    modal.classList.add("flex");

    tbody.innerHTML = `
        <tr>
            <td colspan="5" class="py-6 text-center text-gray-400">
                전체 순위를 불러오는 중입니다.
            </td>
        </tr>
    `;

    const data = await apiFetch("/api/rates?all=1");
    const items = Array.isArray(data) ? data : [];

    if(items.length === 0){
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="py-6 text-center text-gray-400">
                    순위 데이터가 없습니다.
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = "";

    items.forEach((item, index) => {

        const bank = item.bank || item.bank_name || item.kor_co_nm || "-";
        const product = item.product || item.product_name || item.fin_prdt_nm || "-";
        const rate = Number(item.rate ?? item.max_rate ?? item.intr_rate2);
        const change = Number(item.change ?? item.diff ?? 0);
        const isWoori = String(bank).includes("우리금융");

        let changeHtml = '<span class="text-gray-400">-</span>';
        if(Number.isFinite(change) && change > 0){
            changeHtml = `<span class="text-blue-600">+${change.toFixed(2)}%p</span>`;
        }
        else if(Number.isFinite(change) && change < 0){
            changeHtml = `<span class="text-red-500">▲${Math.abs(change).toFixed(2)}%p</span>`;
        }

        const tr = document.createElement("tr");
        if(isWoori){
            tr.className = "bg-blue-50/80 font-bold text-blue-700 [box-shadow:inset_0_0_0_1px_#bfdbfe]";
        }

        tr.innerHTML = `
            <td class="py-2 text-center">${item.rank ?? index + 1}</td>
            <td class="py-2 text-center ${isWoori ? "font-bold text-blue-700" : "text-gray-700"}">${bank}</td>
            <td class="py-2 text-center text-gray-500 truncate" title="${product}">${product}</td>
            <td class="py-2 text-right font-semibold ${isWoori ? "text-blue-700" : "text-gray-800"}">${Number.isFinite(rate) ? rate.toFixed(2) + "%" : "-"}</td>
            <td class="py-2 text-right whitespace-nowrap">${changeHtml}</td>
        `;

        tbody.appendChild(tr);
    });
}

function closeAllRatesModal(){
    const modal = document.getElementById("top10-all-modal");
    if(!modal){
        return;
    }
    modal.classList.add("hidden");
    modal.classList.remove("flex");
}

document.addEventListener("click", function(e){
    if(e.target.closest("#top10-all-btn")){
        openAllRatesModal();
        return;
    }

    if(e.target.closest("#top10-all-close")){
        closeAllRatesModal();
        return;
    }

    const modal = document.getElementById("top10-all-modal");
    if(modal && e.target === modal){
        closeAllRatesModal();
    }
});





/* ==========================================================
   상승 / 하락 TOP5
   /api/financial
========================================================== */


async function fetchFinancialData(){

    // V6: 백엔드 전용 변동 API를 우선 사용
    const data = await apiFetch(
        "/api/rate-changes"
    );

    if(data){

        const upList = Array.isArray(data.up_top5)
            ? data.up_top5
            : [];

        const downList = Array.isArray(data.down_top5)
            ? data.down_top5
            : [];

        console.log(
            "RATE CHANGE API",
            data
        );

        renderRateChanges(
            upList,
            downList
        );

        return;
    }

    // API 실패 시 기존 /api/rates 결과를 이용한 최소 fallback
    const rates = await apiFetch(
        "/api/rates?all=1"
    );

    const items = Array.isArray(rates)
        ? rates
        : [];

    const normalized = items
        .map(item => ({
            ...item,
            change_value: Number(item.change ?? 0)
        }))
        .filter(item => Number.isFinite(item.change_value));

    const upList = normalized
        .filter(item => item.change_value > 0)
        .sort((a,b) => b.change_value - a.change_value)
        .slice(0,5);

    const downList = normalized
        .filter(item => item.change_value < 0)
        .sort((a,b) => a.change_value - b.change_value)
        .slice(0,5);

    renderRateChanges(
        upList,
        downList
    );
}

function renderRateChanges(
    upList,
    downList
){

    const up = document.getElementById("rates-up-list");
    const down = document.getElementById("rates-down-list");

    const renderRows = (target, list, direction) => {

        if(!target){
            return;
        }

        target.innerHTML = "";

        if(!Array.isArray(list) || list.length === 0){
            target.innerHTML = `
            <tr>
                <td colspan="4" class="py-4 text-center text-gray-400 font-normal">
                    ${direction === "up" ? "금리 상승 없음" : "금리 하락 없음"}
                </td>
            </tr>
            `;
            return;
        }

        list.slice(0, 5).forEach((item, index) => {

            const bank =
                item.kor_co_nm ||
                item.bank_name ||
                item.bank ||
                "-";

            const currentRateRaw =
                item.rate ??
                item.current_rate ??
                item.new_rate ??
                item.intr_rate2 ??
                item.max_rate ??
                null;

            const currentRate = Number(currentRateRaw);

            let value = Number(
                item.change_value ??
                item.change ??
                ((Number(item.new_rate) || 0) - (Number(item.old_rate) || 0))
            );

            if(Number.isNaN(value)){
                value = 0;
            }

            const absValue = Math.abs(value).toFixed(2);
            const tr = document.createElement("tr");

            const isWoori = String(bank).includes("우리금융");
            if(isWoori){
                tr.className = "bg-blue-50/80 font-bold text-blue-700 [box-shadow:inset_0_0_0_1px_#bfdbfe]";
            }

            tr.innerHTML = `
                <td class="py-2 text-center ${isWoori ? "text-blue-700" : "text-gray-500"}">${index + 1}</td>
                <td class="py-2 text-center px-1 ${isWoori ? "text-blue-700 font-bold" : "text-gray-700"} truncate" title="${bank}">${bank}</td>
                <td class="py-2 text-center text-xs font-semibold whitespace-nowrap ${isWoori ? "text-blue-700" : "text-gray-700"}">
                    ${Number.isFinite(currentRate) ? currentRate.toFixed(2) + "%" : "-"}
                </td>
                <td class="py-2 text-center text-xs font-semibold whitespace-nowrap ${isWoori ? "text-blue-700 font-bold" : (direction === "up" ? "text-blue-600" : "text-red-500")}">
                    ${direction === "up" ? "+" : "▲"}${absValue}%p
                </td>
            `;

            target.appendChild(tr);
        });
    };

    renderRows(up, upList, "up");
    renderRows(down, downList, "down");
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


    if(event){

        event.preventDefault();

    }


    const input =
        document.getElementById(
            "ai-question"
        )
        ||
        document.getElementById(
            "ai-query-input"
        );


    const answerBox =
        document.getElementById(
            "ai-mini-answer"
        );


    if(!input){

        console.log(
            "AI 질문 입력창 없음"
        );

        return;

    }


    const query =
        input.value.trim();


    if(!query){

        return;

    }


    if(answerBox){

        answerBox.innerHTML =
            `
            <span class="text-gray-400">
            AI가 분석 중입니다...
            </span>
            `;

    }


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
                            question:query
                        })

                }
            );


        if(!response.ok){

            throw new Error(
                `AI API Error : ${response.status}`
            );

        }


        const data =
            await response.json();


        const answer =
            data.answer ||
            data.result ||
            data.message ||
            "분석 결과가 없습니다.";

        const normalizeAIAnswerHtml = (value) => {
            let text = String(value ?? "")
                .replace(/^\s*Gemini AI 답변\s*/i, "")
                .replace(/^\s*제미나이 AI 답변\s*/i, "");

            // API가 <span>, <br> 등을 엔티티로 반환한 경우 한 번 복원
            if(/&lt;\/?(?:span|br|strong|b|div|p)\b/i.test(text)){
                const textarea = document.createElement("textarea");
                textarea.innerHTML = text;
                text = textarea.value;
            }

            const template = document.createElement("template");
            text = text
                .replace(/\r\n/g, "\n")
                .replace(/\n[ \t]*\n[ \t]*\n+/g, "\n\n");

            template.innerHTML = text.replace(/\n/g, "<br>");
            template.content.querySelectorAll("script, iframe, object, embed, style").forEach(el => el.remove());
            template.content.querySelectorAll("*").forEach(el => {
                [...el.attributes].forEach(attr => {
                    if(/^on/i.test(attr.name)) el.removeAttribute(attr.name);
                    if((attr.name === "href" || attr.name === "src") && /^javascript:/i.test(attr.value)) el.removeAttribute(attr.name);
                });
            });
            return template.innerHTML;
        };

        const cleanAnswerHtml = normalizeAIAnswerHtml(answer);
        const plainHolder = document.createElement("div");
        plainHolder.innerHTML = cleanAnswerHtml;
        const cleanAnswerText = plainHolder.innerText.trim();

        window.sbLastAIQuestion = query;
        window.sbLastAIAnswerText = cleanAnswerText;

        const applyRateColors = (root) => {
            root.querySelectorAll(".rate-change.increase").forEach(el => {
                el.classList.add("text-blue-600", "font-semibold");
            });
            root.querySelectorAll(".rate-change.decrease").forEach(el => {
                el.classList.add("text-red-600", "font-semibold");
            });
            root.querySelectorAll(".rate-change:not(.increase):not(.decrease)").forEach(el => {
                el.classList.add("text-gray-500");
            });
        };

        const decoratePlainRateChanges = (root) => {
            const walker = document.createTreeWalker(
                root,
                NodeFilter.SHOW_TEXT
            );
            const nodes = [];
            while(walker.nextNode()){
                const node = walker.currentNode;
                if(node.parentElement?.closest(".rate-change")) continue;
                if(/[+▲]\s*\d+(?:\.\d+)?%p/.test(node.nodeValue || "")){
                    nodes.push(node);
                }
            }

            nodes.forEach(node => {
                const text = node.nodeValue || "";
                const frag = document.createDocumentFragment();
                let last = 0;
                const re = /([+▲])\s*(\d+(?:\.\d+)?)%p/g;
                let match;
                while((match = re.exec(text))){
                    if(match.index > last){
                        frag.appendChild(document.createTextNode(text.slice(last, match.index)));
                    }
                    const span = document.createElement("span");
                    span.className = match[1] === "+"
                        ? "rate-change increase text-blue-600 font-semibold"
                        : "rate-change decrease text-red-600 font-semibold";
                    span.textContent = `${match[1]}${match[2]}%p`;
                    frag.appendChild(span);
                    last = re.lastIndex;
                }
                if(last < text.length){
                    frag.appendChild(document.createTextNode(text.slice(last)));
                }
                node.replaceWith(frag);
            });
        };

        if(answerBox){
            // 원문의 줄바꿈은 살리되, 과도한 빈 줄만 한 칸으로 축소
            const miniTemplate = document.createElement("template");
            miniTemplate.innerHTML = cleanAnswerHtml;
            applyRateColors(miniTemplate.content);
            decoratePlainRateChanges(miniTemplate.content);

            const brs = [...miniTemplate.content.querySelectorAll("br")];
            brs.forEach((br, idx) => {
                const next = br.nextSibling;
                if(next && next.nodeName === "BR"){
                    const spacer = document.createElement("span");
                    spacer.className = "block h-1";
                    br.replaceWith(spacer);
                    next.remove();
                }
            });

            answerBox.innerHTML = miniTemplate.innerHTML;
        }

        // 상세보기에서도 증감 색상이 항상 유지되도록 저장본에도 클래스 보강
        const detailTemplate = document.createElement("template");
        detailTemplate.innerHTML = cleanAnswerHtml;
        applyRateColors(detailTemplate.content);
        decoratePlainRateChanges(detailTemplate.content);
        window.sbLastAIAnswer = detailTemplate.innerHTML;


        console.log(
            "AI SEARCH RESULT",
            data
        );


    }
    catch(error){


        console.error(
            "AI Error:",
            error
        );


        if(answerBox){

            answerBox.innerHTML =
                `
                <span class="text-red-500">
                AI 분석 요청 중 오류가 발생했습니다.
                </span>
                `;

        }


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


    /* ======================================================
       TOP10 카테고리 변경
    ====================================================== */

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



    /* ======================================================
       AI 질문
       현재 V5 index.html : #ai-question
    ====================================================== */

    const aiInput =
        document.getElementById(
            "ai-question"
        )
        ||
        document.getElementById(
            "ai-query-input"
        );


    if(aiInput){


        const inputRow =
            aiInput.parentElement;


        const searchButton =
            inputRow
            ?
            inputRow.querySelector(
                "button"
            )
            :
            null;


        if(searchButton){

            searchButton.addEventListener(
                "click",
                handleAISearch
            );

        }


        aiInput.addEventListener(
            "keydown",
            e => {

                if(e.key === "Enter"){

                    handleAISearch(e);

                }

            }
        );


        const questionPanel =
            aiInput.closest(
                ".bg-gray-50"
            );


        if(questionPanel){

            const quickButtons =
                questionPanel.querySelectorAll(
                    "button"
                );


            quickButtons.forEach(
                button => {

                    if(button === searchButton){

                        return;

                    }


                    button.addEventListener(
                        "click",
                        e => {

                            e.preventDefault();

                            const label =
                                button.textContent.trim();


                            const questionMap = {

                                "시장현황":
                                    "시장현황 알려줘",

                                "우리금융":
                                    "우리금융 경쟁력은",

                                "경쟁사":
                                    "경쟁사 현황 알려줘"

                            };


                            aiInput.value =
                                questionMap[label]
                                ||
                                label;


                            handleAISearch(e);

                        }
                    );

                }
            );

        }

    }



    /* ======================================================
       기존 FORM 방식도 호환
    ====================================================== */

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



    /* ======================================================
       상품 검색
    ====================================================== */

    setupProductSearch();


}




/* ==========================================================
   Dashboard Final Initialize
========================================================== */


window.addEventListener(
    "load",

    ()=>{


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
   AI DETAIL HOVER PREVIEW - 마지막 실제 질문/답변
========================================================== */

document.addEventListener(
    "mouseover",
    function(e){

        const btn = e.target.closest("#ai-detail-btn");
        if(!btn){
            return;
        }

        let preview = document.getElementById("ai-detail-preview");

        if(!preview){
            preview = document.createElement("div");
            preview.id = "ai-detail-preview";
            preview.className = `
                fixed z-[9999] w-96 bg-white border border-blue-100
                rounded-xl shadow-xl p-4 text-xs text-gray-700
            `;
            document.body.appendChild(preview);
        }

        const escapeHtml = value => String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

        const question = window.sbLastAIQuestion ||
            document.getElementById("ai-question")?.value?.trim() ||
            "AI 질문";

        const answerHtml = window.sbLastAIAnswer ||
            "먼저 AI 질문을 실행하면 실제 답변 미리보기가 표시됩니다.";

        preview.innerHTML = `
            <div class="mb-3">
                <div class="font-bold text-blue-700">📊 AI 답변 미리보기</div>
            </div>
            <div class="text-[10px] text-gray-400 mb-1">질문</div>
            <div class="font-bold text-gray-800 mb-2">${escapeHtml(question)}</div>
            <div class="text-[10px] text-gray-400 mb-1">답변</div>
            <div class="text-[11px] leading-5 max-h-56 overflow-y-auto pr-1">${answerHtml}</div>
            <div class="mt-3 pt-2 border-t text-[10px] text-blue-600 text-right">클릭하면 전체 답변을 확인합니다 →</div>
        `;

        const rect = btn.getBoundingClientRect();
        const maxLeft = window.innerWidth - 400;
        preview.style.left = Math.max(12, Math.min(rect.left, maxLeft)) + "px";
        preview.style.top = (rect.bottom + 8) + "px";
        preview.style.display = "block";
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

/* ==========================================================
   시장분석 상세보기 : AI 질문 상세보기와 완전 분리
========================================================== */
document.addEventListener("click", function(event){
    if(event.target.closest("#market-detail-btn")){
        event.preventDefault();
        const modal = document.getElementById("market-detail-modal");
        if(modal){
            modal.classList.remove("hidden");
            modal.classList.add("flex");
        }
        return;
    }

    if(event.target.closest("#market-detail-close")){
        const modal = document.getElementById("market-detail-modal");
        if(modal){
            modal.classList.add("hidden");
            modal.classList.remove("flex");
        }
        return;
    }

    const modal = document.getElementById("market-detail-modal");
    if(modal && event.target === modal){
        modal.classList.add("hidden");
        modal.classList.remove("flex");
    }
});
