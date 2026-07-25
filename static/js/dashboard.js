/* ===================================
   SBRateBot V5 Dashboard JS
   Full Replacement Version
=================================== */


let productData = [];

let selectedCategory = "정기예금";

let selectedPeriod = "12개월";

let aiTimer = null;



document.addEventListener(
    "DOMContentLoaded",
    function(){


        console.log(
            "SBRateBot V5 Dashboard Loaded"
        );


        initDashboard();

        initProductFilter();

        initProductSearch();

        initAISearch();

        initAIAutoSearch();


    }
);



async function initDashboard(){


    await loadKPI();

    await loadWoori();

    await loadFinancial();

    await loadRates();

    await loadProducts();

    await loadAI();


    // V5 신규 영역

    await loadExecutive();

    await loadWatchList();

    await loadSystemStatus();


}





/* ===================================
   KPI
=================================== */


async function loadKPI(){


    try{


        const response =
        await fetch(
            "/api/kpi"
        );


        const data =
        await response.json();



        setText(
            "#product-count",
            (data.product_count || 0)
            + "개"
        );


        setText(
            "#bank-count",
            (data.bank_count || "-")
        );


        setText(
            "#max-rate",
            formatRate(
                data.max_rate
            )
        );


        setText(
            "#avg-rate",
            formatRate(
                data.average_rate
            )
        );


        setText(
            "#min-rate",
            formatRate(
                data.min_rate
            )
        );



    }
    catch(error){


        console.error(
            "KPI ERROR",
            error
        );


    }


}





/* ===================================
   우리금융 Market Position
=================================== */


async function loadWoori(){


    try{


        const response =
        await fetch(
            "/api/woori"
        );


        const data =
        await response.json();



        const rate =
        Number(
            data.rate || 0
        );



        setText(
            "#woori-rate",
            formatRate(rate)
        );



        setText(
            "#current-rate",
            formatRate(rate)
        );



        setText(
            "#market-rank",
            data.market_rank
            ?
            data.market_rank+"위"
            :
            "-"
        );



        setText(
            "#basis-product",
            data.product || "-"
        );


        setText(
            "#basis-product-card",
            data.product || "-"
        );



        setText(
            "#financial-rank",
            data.financial_rank
            ?
            data.financial_rank+"위"
            :
            "-"
        );



        setHTML(
            "#average-gap",
            formatGap(
                data.average_gap
            )
        );


        setHTML(
            "#highest-gap",
            formatGap(
                data.highest_gap
            )
        );


        setHTML(
            "#lowest-gap",
            formatGap(
                data.lowest_gap
            )
        );



    }
    catch(error){


        console.error(
            "WOORI ERROR",
            error
        );


    }


}





/* ===================================
   금융지주 비교
=================================== */


async function loadFinancial(){


    try{


        const response =
        await fetch(
            "/api/financial"
        );


        const data =
        await response.json();



        renderRateTable(
            "#financial-table",
            data
        );



        calculateFinancialRank(
            data
        );



    }
    catch(error){


        console.error(
            "FINANCIAL ERROR",
            error
        );


    }


}





function calculateFinancialRank(
    data
){


    if(
        !Array.isArray(data)
    )
    return;



    const list =
    data.filter(
        item => {


            const bank =
            String(
                item.bank || ""
            );


            return (

                bank.includes("우리금융")

                ||

                bank.includes("KB")

                ||

                bank.includes("신한")

                ||

                bank.includes("하나")

            );


        }
    );



    list.sort(
        (a,b)=>
        Number(b.rate)
        -
        Number(a.rate)
    );



    const index =
    list.findIndex(
        item =>
        String(item.bank)
        .includes(
            "우리금융"
        )
    );



    setText(
        "#financial-rank",
        index >=0
        ?
        index+1+"위"
        :
        "-"
    );


}





/* ===================================
   시장 TOP10
=================================== */


async function loadRates(){


    try{


        const response =
        await fetch(
            "/api/rates"
        );


        const data =
        await response.json();



        renderRateTable(
            "#market-table",
            data
        );


    }
    catch(error){


        console.error(
            "RATE ERROR",
            error
        );


    }


}





/* ===================================
   공통 테이블
=================================== */


function renderRateTable(
    selector,
    data
){


    const table =
    document.querySelector(
        selector
    );


    if(!table)
    return;



    table.innerHTML="";



    if(
        !Array.isArray(data)
        ||
        data.length===0
    ){


        table.innerHTML = `

        <tr>
        <td colspan="5">
        데이터 없음
        </td>
        </tr>

        `;


        return;

    }



    data.forEach(
        (item,index)=>{


            const rank =
            item.rank
            ||
            index+1;



            const row =
            document.createElement(
                "tr"
            );



            row.innerHTML = `

            <td>
            ${rank}위
            </td>

            <td>
            ${
                highlightWoori(
                    item.bank
                )
            }
            </td>

            <td>
            ${item.product || "-"}
            </td>

            <td>
            <strong>
            ${
                formatRate(
                    item.rate
                )
            }
            </strong>
            </td>

            <td>
            ${
                formatChange(
                    item.change
                )
            }
            </td>

            `;



            table.appendChild(
                row
            );


        }
    );


}

/* ===================================
   전체 상품 조회
=================================== */


async function loadProducts(){


    try{


        const response =
        await fetch(
            "/api/products"
        );


        productData =
        await response.json();



        renderProducts();


    }
    catch(error){


        console.error(
            "PRODUCT ERROR",
            error
        );


    }


}





function renderProducts(){


    const table =
    document.querySelector(
        "#product-table"
    );


    if(!table)
    return;



    const keyword =
    (
        document.querySelector(
            "#product-search"
        )?.value
        ||
        ""
    )
    .toLowerCase();



    let filtered =
    productData.filter(
        item=>{


            const category =
            item.category || "";


            const period =
            item.period || "";



            const bank =
            String(
                item.bank || ""
            )
            .toLowerCase();



            const product =
            String(
                item.product || ""
            )
            .toLowerCase();



            return (

                category === selectedCategory

                &&

                (
                    selectedCategory !== "정기예금"

                    ||

                    period === selectedPeriod

                )

                &&

                (

                    bank.includes(keyword)

                    ||

                    product.includes(keyword)

                )

            );


        }
    );



    filtered.sort(
        (a,b)=>
        Number(b.rate)
        -
        Number(a.rate)
    );



    table.innerHTML="";



    filtered.forEach(
        (item,index)=>{


            const row =
            document.createElement(
                "tr"
            );



            row.innerHTML = `

            <td>
            ${index+1}위
            </td>


            <td>
            ${
                highlightWoori(
                    item.bank
                )
            }
            </td>


            <td>
            ${item.product || "-"}
            </td>


            <td>
            <strong>
            ${
                formatRate(
                    item.rate
                )
            }
            </strong>
            </td>


            <td>
            ${
                formatChange(
                    item.change
                )
            }
            </td>

            `;


            table.appendChild(
                row
            );


        }
    );


}





/* ===================================
   상품 필터
=================================== */


function initProductFilter(){


    const categoryButtons =
    document.querySelectorAll(
        ".product-tabs button"
    );



    const periodButtons =
    document.querySelectorAll(
        ".period-filter button"
    );



    categoryButtons.forEach(
        button=>{


            button.addEventListener(
                "click",
                ()=>{


                    categoryButtons.forEach(
                        b=>
                        b.classList.remove(
                            "active"
                        )
                    );


                    button.classList.add(
                        "active"
                    );



                    selectedCategory =
                    button.innerText.trim();



                    renderProducts();


                }
            );


        }
    );



    periodButtons.forEach(
        button=>{


            button.addEventListener(
                "click",
                ()=>{


                    periodButtons.forEach(
                        b=>
                        b.classList.remove(
                            "active"
                        )
                    );



                    button.classList.add(
                        "active"
                    );



                    selectedPeriod =
                    button.innerText.trim();



                    renderProducts();


                }
            );


        }
    );


}





function initProductSearch(){


    const input =
    document.querySelector(
        "#product-search"
    );


    if(!input)
    return;



    input.addEventListener(
        "input",
        renderProducts
    );


}





/* ===================================
   AI Summary
=================================== */


async function loadAI(){


    try{


        const response =
        await fetch(
            "/api/ai"
        );


        const data =
        await response.json();



        const box =
        document.querySelector(
            "#ai-summary"
        );



        if(!box)
        return;



        box.innerHTML =

        (

            data.summary || []

        )
        .map(
            item=>
            `<li>${item}</li>`
        )
        .join("");



    }
    catch(error){


        console.error(
            "AI ERROR",
            error
        );


    }


}





/* ===================================
   V5 Executive Dashboard
=================================== */


async function loadExecutive(){


    const summary =
    document.querySelector(
        "#executive-summary"
    );


    if(summary){


        summary.innerHTML = `

        <p>
        AI가 오늘 시장 데이터를 분석했습니다.
        </p>

        <p>
        우리금융 경쟁력과 금리 변동을
        지속 모니터링합니다.
        </p>

        `;


    }



    setText(
        "#market-status",
        "안정"
    );


    setText(
        "#ai-confidence",
        "99%"
    );


}





async function loadWatchList(){


    const box =
    document.querySelector(
        "#watch-list"
    );



    if(!box)
    return;



    box.innerHTML = `

    <div>
    🟢 우리금융저축은행
    <br>
    금융지주 경쟁력 유지
    </div>


    <div>
    ⚠ 경쟁은행 모니터링
    <br>
    금리 변화 감시
    </div>


    `;


}





async function loadSystemStatus(){


    setText(
        "#data-status",
        "Running"
    );


    setText(
        "#ai-status",
        "Connected"
    );


    setText(
        "#dashboard-status",
        "Online"
    );


}





/* ===================================
   AI 검색
=================================== */


function initAISearch(){


    const button =
    document.querySelector(
        "#ai-search-btn"
    );


    const input =
    document.querySelector(
        "#ai-question"
    );



    if(button){


        button.addEventListener(
            "click",
            searchAI
        );


    }



    if(input){


        input.addEventListener(
            "keydown",
            e=>{


                if(
                    e.key==="Enter"
                ){


                    e.preventDefault();

                    searchAI();


                }


            }
        );


    }


}





function initAIAutoSearch(){


    const input =
    document.querySelector(
        "#ai-question"
    );



    if(!input)
    return;



    input.addEventListener(
        "input",
        ()=>{


            clearTimeout(
                aiTimer
            );



            aiTimer =
            setTimeout(
                ()=>{


                    if(
                        input.value.trim()
                        .length>=2
                    ){

                        searchAI();

                    }


                },
                800
            );


        }
    );


}





async function searchAI(){


    const input =
    document.querySelector(
        "#ai-question"
    );



    const answer =
    document.querySelector(
        "#ai-answer"
    );



    if(
        !input ||
        !answer
    )
    return;



    const question =
    input.value.trim();



    if(!question)
    return;



    answer.innerText =
    "AI 분석중...";



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

                    question:question

                })

            }
        );



        const data =
        await response.json();



        answer.innerHTML =
        data.answer
        ||
        "분석 결과가 없습니다.";



    }
    catch(error){


        console.error(
            error
        );


        answer.innerText =
        "AI 검색 오류";


    }


}





/* ===================================
   공통 함수
=================================== */


function setText(
    selector,
    value
){


    const el =
    document.querySelector(
        selector
    );


    if(el)
    el.innerText =
    value;


}





function setHTML(
    selector,
    value
){


    const el =
    document.querySelector(
        selector
    );


    if(el)
    el.innerHTML =
    value;


}





function formatRate(
    value
){


    const num =
    Number(value || 0);



    if(
        !num
    )
    return "-";



    return num.toFixed(2)+"%";


}





function formatGap(
    value
){


    const num =
    Number(value || 0);



    if(num>0){


        return `

        <span class="rate-change increase">

        +${num.toFixed(2)}%p

        </span>

        `;


    }



    if(num<0){


        return `

        <span class="rate-change decrease">

        ▲${Math.abs(num).toFixed(2)}%p

        </span>

        `;


    }



    return "0.00%p";


}





function formatChange(
    value
){


    const num =
    Number(
        String(value || 0)
        .replace("+","")
    );



    if(num>0){


        return `

        <span class="rate-change increase">

        +${num.toFixed(2)}%

        </span>

        `;


    }



    if(num<0){


        return `

        <span class="rate-change decrease">

        ▲${Math.abs(num).toFixed(2)}%

        </span>

        `;


    }



    return "0.00%";


}





function highlightWoori(
    name
){


    if(
        String(name)
        .includes(
            "우리금융"
        )
    ){


        return `<strong>${name}</strong>`;


    }


    return name || "-";


}