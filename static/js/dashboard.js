document.addEventListener('DOMContentLoaded', function () {
    console.log("SBRateBot V5 Engine Initialized - Fetching Real Data...");

    // 1. KPI 실제 데이터 로드
    loadKPIData();

    // 2. 금리 데이터 로드 (TOP 1~5, TOP 6~10, 상승/하락 TOP5)
    loadRatesData();

    // 3. 은행 목록 Dropdown 데이터 로드
    loadBankOptions();

    // 4. AI 브리핑 & 시장상태 로드
    loadAISummary();

    // 5. 버튼 및 이벤트 핸들러 등록
    setupEventHandlers();
});

// 1. KPI 실제 데이터 로드
function loadKPIData() {
    fetch('/api/kpi')
        .then(res => res.json())
        .then(data => {
            if (data.woori_rank) document.getElementById('woori-rank').innerText = data.woori_rank + '위';
            if (data.max_rate) document.getElementById('max-rate-val').innerText = data.max_rate;
            if (data.avg_rate) document.getElementById('avg-rate-val').innerText = data.avg_rate;
            if (data.woori_max_rate) document.getElementById('woori-max-rate-val').innerText = data.woori_max_rate;
            if (data.total_products) document.getElementById('total-products-val').innerText = data.total_products;
            if (data.total_banks) document.getElementById('total-banks-val').innerText = data.total_banks;
            if (data.changes_count !== undefined) document.getElementById('changes-count-val').innerText = data.changes_count;
        })
        .catch(err => console.error("KPI Data Load Error:", err));
}

// 2. 금리 데이터 (TOP10 분할 및 상승/하락) 로드
function loadRatesData() {
    fetch('/api/rates')
        .then(res => res.json())
        .then(data => {
            let rates = Array.isArray(data) ? data : (data.rates || data.data || []);
            
            if (rates.length === 0) return;

            // 금리 높은 순 정렬
            rates.sort((a, b) => {
                let rA = parseFloat(a.rate || a.init_rate || 0);
                let rB = parseFloat(b.rate || b.init_rate || 0);
                return rB - rA;
            });

            // TOP 1~5 / TOP 6~10 분할 렌더링
            renderTop10Split(rates.slice(0, 10));

            // 상승 / 하락 TOP5 렌더링
            renderMovements(rates);
        })
        .catch(err => console.error("Rates Data Load Error:", err));
}

function renderTop10Split(top10List) {
    const top1_5Box = document.getElementById('top1-5-list');
    const top6_10Box = document.getElementById('top6-10-list');

    if (!top1_5Box || !top6_10Box) return;

    top1_5Box.innerHTML = '';
    top6_10Box.innerHTML = '';

    top10List.forEach((item, index) => {
        const rank = index + 1;
        const bankName = item.bank_name || item.bank || '저축은행';
        const rate = parseFloat(item.rate || item.init_rate || 0).toFixed(2);
        const isWoori = bankName.includes('우리');

        const itemHTML = `
            <div class="rank-list-item ${isWoori ? 'highlight' : ''}">
                <span><strong class="rank-num ${isWoori ? 'text-primary' : ''}">${rank}</strong>${bankName}</span>
                <span class="fw-bold ${isWoori ? 'text-primary' : ''}">${rate}%</span>
            </div>
        `;

        if (rank <= 5) {
            top1_5Box.innerHTML += itemHTML;
        } else {
            top6_10Box.innerHTML += itemHTML;
        }
    });
}

function renderMovements(rates) {
    const upBox = document.getElementById('rate-up-list');
    const downBox = document.getElementById('rate-down-list');

    // diff / change 항목이 있는 데이터 필터링
    let upRates = rates.filter(r => (r.change || r.diff || 0) > 0);
    let downRates = rates.filter(r => (r.change || r.diff || 0) < 0);

    if (upBox) {
        if (upRates.length > 0) {
            upBox.innerHTML = upRates.slice(0, 5).map(r => `
                <div class="d-flex justify-content-between py-1">
                    <span class="text-truncate">${r.bank_name || r.bank}</span>
                    <span class="rate-up">+${parseFloat(r.change || r.diff).toFixed(2)}%p</span>
                </div>
            `).join('');
        } else {
            upBox.innerHTML = '<div class="text-muted text-xs py-2">상승 항목 없음</div>';
        }
    }

    if (downBox) {
        if (downRates.length > 0) {
            downBox.innerHTML = downRates.slice(0, 5).map(r => `
                <div class="d-flex justify-content-between py-1">
                    <span class="text-truncate">${r.bank_name || r.bank}</span>
                    <span class="rate-down">${parseFloat(r.change || r.diff).toFixed(2)}%p</span>
                </div>
            `).join('');
        } else {
            downBox.innerHTML = '<div class="text-muted text-xs py-2">하락 항목 없음</div>';
        }
    }
}

// 3. 은행 검색 드롭다운 동적 구성
function loadBankOptions() {
    fetch('/api/banks')
        .then(res => res.json())
        .then(banks => {
            const selectEl = document.getElementById('filter-bank');
            if (!selectEl) return;
            selectEl.innerHTML = '<option value="">은행 선택 (전체)</option>';
            
            let bankList = Array.isArray(banks) ? banks : (banks.banks || []);
            bankList.forEach(bank => {
                const name = typeof bank === 'string' ? bank : (bank.name || bank.bank_name);
                selectEl.innerHTML += `<option value="${name}">${name}</option>`;
            });
        })
        .catch(err => console.error("Bank Options Load Error:", err));
}

// 4. AI 시장 브리핑
function loadAISummary() {
    fetch('/api/ai/summary')
        .then(res => res.json())
        .then(data => {
            if (data.summary) {
                document.getElementById('ai-summary-text').innerText = data.summary;
            }
            if (data.status) {
                document.getElementById('market-status-text').innerText = data.status;
            }
            if (data.description) {
                document.getElementById('ai-assistant-desc').innerHTML = data.description;
            }
        })
        .catch(err => console.log("AI Summary Default Active"));
}

// 5. Gemini AI 질의응답 처리
function setupEventHandlers() {
    const btnSearch = document.getElementById('btn-ai-search');
    const btnQuickAsk = document.getElementById('btn-ai-quick-ask');

    const handleAiAsk = (inputId) => {
        const inputEl = document.getElementById(inputId);
        const query = inputEl ? inputEl.value.trim() : '';
        if (!query) return alert('질문 내용을 입력해주세요.');

        // 로딩 표시
        const originalText = btnSearch ? btnSearch.innerHTML : '';
        if (btnSearch) btnSearch.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> 분석중...';

        fetch('/api/ai/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        })
        .then(res => res.json())
        .then(data => {
            alert(`🤖 Gemini AI 분석 답변:\n\n${data.answer || '응답을 완료했습니다.'}`);
        })
        .catch(err => {
            alert('AI 응답을 가져오는 중 오류가 발생했습니다.');
        })
        .finally(() => {
            if (btnSearch) btnSearch.innerHTML = originalText;
        });
    };

    if (btnSearch) btnSearch.addEventListener('click', () => handleAiAsk('ai-prompt-input'));
    if (btnQuickAsk) btnQuickAsk.addEventListener('click', () => handleAiAsk('ai-quick-input'));
}