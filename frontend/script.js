// Form validation
(function () {
    'use strict'
    var forms = document.querySelectorAll('.needs-validation')
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
          form.classList.add('was-validated')
        }, false)
      })
})()

// Helper functions
function getCentsValue(id) {
    const element = document.getElementById(id);
    if (!element) {
        console.error(`Element with ID '${id}' not found.`);
        return 0;
    }
    const value = parseFloat(element.value);
    return isNaN(value) ? 0 : Math.round(value * 100);
}

function formatCurrency(cents) {
    return (cents / 100).toFixed(2) + ' €';
}

function formatPercentage(value) {
    return value.toFixed(1) + '%';
}

// Global variables
let currentInputData = null;
let currentResult = null;

// Collect form data
function collectFormData() {
    return {
        RE4: getCentsValue('RE4'),
        STKL: parseInt(document.getElementById('STKL').value),
        LZZ: parseInt(document.getElementById('LZZ').value),
        ZKF: parseFloat(document.getElementById('ZKF').value),
        R: parseInt(document.getElementById('R').value),
        KVZ: parseFloat(document.getElementById('KVZ').value),
        PVS: document.getElementById('PVS').checked ? 1 : 0,
        PVZ: document.getElementById('PVZ').checked ? 1 : 0,
        PKV: parseInt(document.getElementById('PKV').value),
        af: parseInt(document.getElementById('af').value),
        f: parseFloat(document.getElementById('f').value),
        AJAHR: parseInt(document.getElementById('AJAHR').value),
        ALTER1: document.getElementById('ALTER1').checked ? 1 : 0,
        JFREIB: getCentsValue('JFREIB'),
        JHINZU: getCentsValue('JHINZU'),
        JRE4: getCentsValue('JRE4'),
        JRE4ENT: getCentsValue('JRE4ENT'),
        JVBEZ: getCentsValue('JVBEZ'),
        KRV: parseInt(document.getElementById('KRV').value),
        LZZFREIB: getCentsValue('LZZFREIB'),
        LZZHINZU: getCentsValue('LZZHINZU'),
        MBV: getCentsValue('MBV'),
        PKPV: getCentsValue('PKPV'),
        PVA: parseFloat(document.getElementById('PVA').value),
        SONSTB: getCentsValue('SONSTB'),
        SONSTENT: getCentsValue('SONSTENT'),
        STERBE: getCentsValue('STERBE'),
        VBEZ: getCentsValue('VBEZ'),
        VBEZM: getCentsValue('VBEZM'),
        VBEZS: getCentsValue('VBEZS'),
        VBS: getCentsValue('VBS'),
        VJAHR: parseInt(document.getElementById('VJAHR').value),
        ZMVB: parseInt(document.getElementById('ZMVB').value)
    };
}

// Helper functions for text conversion
function getSteuerklasseText(stkl) {
    const classes = {
        1: 'I (ledig)', 2: 'II (alleinerziehend)', 3: 'III (verheiratet, höheres Einkommen)',
        4: 'IV (verheiratet, ähnliches Einkommen)', 5: 'V (verheiratet, geringeres Einkommen)', 6: 'VI (Nebenjob)'
    };
    return classes[stkl] || stkl;
}

function getLzzText(lzz) {
    const periods = {1: 'Jahr', 2: 'Monat', 3: 'Woche', 4: 'Tag'};
    return periods[lzz] || lzz;
}

function getKirchensteuerText(r) {
    const religions = {0: 'Keine', 1: 'Evangelisch/Katholisch (9%)', 2: 'Andere (8%)'};
    return religions[r] || r;
}

// Calculate social insurance estimates
function calculateSocialInsurance(brutto, lzz) {
    const monthlyBrutto = lzz === 2 ? brutto : brutto / 12;
    const kvRate = 0.146, pvRate = 0.036, rvRate = 0.186, avRate = 0.024;
    const bbgKvPv = 66150 / 12, bbgRv = 96600 / 12;
    const basisKvPv = Math.min(monthlyBrutto, bbgKvPv);
    const basisRv = Math.min(monthlyBrutto, bbgRv);
    
    return {
        kv: basisKvPv * kvRate / 2, pv: basisKvPv * pvRate / 2,
        rv: basisRv * rvRate / 2, av: basisRv * avRate / 2
    };
}

// Create pie chart
function createTaxChart(lstlzz, solzlzz, bk, netto) {
    const canvas = document.getElementById('taxChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const total = lstlzz + solzlzz + bk + netto;
    const data = [
        { label: 'Lohnsteuer', value: lstlzz, color: '#dc3545' },
        { label: 'Solidaritätszuschlag', value: solzlzz, color: '#fd7e14' },
        { label: 'Kirchensteuer', value: bk, color: '#6f42c1' },
        { label: 'Nettolohn', value: netto, color: '#198754' }
    ];
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    let currentAngle = -Math.PI / 2;
    const centerX = canvas.width / 2, centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 10;
    
    data.forEach(item => {
        if (item.value > 0) {
            const sliceAngle = (item.value / total) * 2 * Math.PI;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
            ctx.closePath();
            ctx.fillStyle = item.color;
            ctx.fill();
            currentAngle += sliceAngle;
        }
    });
}

// Display results
function displayResults(result, inputData) {
    console.log('Displaying results:', result, inputData);
    
    const lstlzz = parseFloat(result.LSTLZZ) || 0;
    const solzlzz = parseFloat(result.SOLZLZZ) || 0;
    const bk = parseFloat(result.BK) || 0;
    const brutto = inputData.RE4;
    const totalTax = lstlzz + solzlzz + bk;
    const netto = brutto - totalTax;
    
    // Update main results
    document.getElementById('LSTLZZ').textContent = formatCurrency(lstlzz);
    document.getElementById('SOLZLZZ').textContent = formatCurrency(solzlzz);
    document.getElementById('BK').textContent = formatCurrency(bk);
    document.getElementById('TOTAL').textContent = formatCurrency(totalTax);
    document.getElementById('NETTO').textContent = formatCurrency(netto);
    
    // Update percentages
    document.getElementById('LSTLZZ-percent').textContent = formatPercentage((lstlzz / brutto) * 100);
    document.getElementById('SOLZLZZ-percent').textContent = formatPercentage((solzlzz / brutto) * 100);
    document.getElementById('BK-percent').textContent = formatPercentage((bk / brutto) * 100);
    document.getElementById('TOTAL-percent').textContent = formatPercentage((totalTax / brutto) * 100);
    document.getElementById('NETTO-percent').textContent = formatPercentage((netto / brutto) * 100);
    
    // Update summary
    document.getElementById('summary-brutto').textContent = formatCurrency(brutto);
    document.getElementById('summary-stkl').textContent = getSteuerklasseText(inputData.STKL);
    document.getElementById('summary-lzz').textContent = getLzzText(inputData.LZZ);
    document.getElementById('summary-zkf').textContent = inputData.ZKF;
    document.getElementById('summary-kirche').textContent = getKirchensteuerText(inputData.R);
    document.getElementById('summary-kvz').textContent = inputData.KVZ + '%';
    
    // Social insurance estimates
    const socialInsurance = calculateSocialInsurance(brutto / 100, inputData.LZZ);
    document.getElementById('KV-estimate').textContent = formatCurrency(socialInsurance.kv * 100);
    document.getElementById('PV-estimate').textContent = formatCurrency(socialInsurance.pv * 100);
    document.getElementById('RV-estimate').textContent = formatCurrency(socialInsurance.rv * 100);
    document.getElementById('AV-estimate').textContent = formatCurrency(socialInsurance.av * 100);
    
    // Yearly projections
    const yearlyMultiplier = {1: 1, 2: 12, 3: 52, 4: 365}[inputData.LZZ] || 12;
    const yearlyTax = totalTax * yearlyMultiplier;
    const yearlyNetto = netto * yearlyMultiplier;
    const yearlyBrutto = brutto * yearlyMultiplier;
    const effectiveRate = (yearlyTax / yearlyBrutto) * 100;
    
    document.getElementById('YEAR-tax').textContent = formatCurrency(yearlyTax);
    document.getElementById('YEAR-netto').textContent = formatCurrency(yearlyNetto);
    document.getElementById('EFFECTIVE-rate').textContent = formatPercentage(effectiveRate);
    
    createTaxChart(lstlzz, solzlzz, bk, netto);
}

// Update display and store data
function updateDisplayResults(result, inputData) {
    currentInputData = inputData;
    currentResult = result;
    
    // Enable export buttons
    const exportBtn = document.getElementById('exportDropdown');
    const compareBtn = document.getElementById('compareBtn');
    if (exportBtn) exportBtn.disabled = false;
    if (compareBtn) compareBtn.disabled = false;
    
    displayResults(result, inputData);
}

// Quick scenario loading
function loadQuickScenario(scenario) {
    document.getElementById('tax-form').reset();
    
    // Set defaults
    document.getElementById('LZZ').value = '2';
    document.getElementById('KVZ').value = '1.7';
    document.getElementById('AJAHR').value = '2025';
    document.getElementById('VJAHR').value = '2025';
    document.getElementById('f').value = '1.0';
    document.getElementById('af').value = '1';
    
    const scenarios = {
        'single': {STKL: '1', ZKF: '0', R: '0', RE4: '3500.00', JRE4: '42000.00'},
        'married': {STKL: '3', ZKF: '0', R: '1', RE4: '4500.00', JRE4: '54000.00'},
        'parent': {STKL: '2', ZKF: '1', R: '1', RE4: '3200.00', JRE4: '38400.00'},
        'family': {STKL: '3', ZKF: '2', R: '1', RE4: '4200.00', JRE4: '50400.00'}
    };
    
    const data = scenarios[scenario];
    if (data) {
        Object.keys(data).forEach(key => {
            const element = document.getElementById(key);
            if (element) element.value = data[key];
        });
        
        const names = {
            'single': 'Alleinstehend, keine Kinder',
            'married': 'Verheiratet, Steuerklasse III',
            'parent': 'Alleinerziehend, 1 Kind',
            'family': 'Verheiratet, 2 Kinder'
        };
        alert('Szenario "' + names[scenario] + '" geladen!');
    }
}

// Save/Load functions
function saveCalculation() {
    const name = prompt('Name für diese Berechnung:', 'Berechnung ' + new Date().toLocaleDateString());
    if (!name) return;
    
    const data = collectFormData();
    const savedCalculations = JSON.parse(localStorage.getItem('savedCalculations') || '[]');
    savedCalculations.push({name: name, date: new Date().toISOString(), data: data});
    localStorage.setItem('savedCalculations', JSON.stringify(savedCalculations));
    alert('Berechnung gespeichert!');
}

function resetForm() {
    if (confirm('Alle Eingaben zurücksetzen?')) {
        document.getElementById('tax-form').reset();
        document.getElementById('result').style.display = 'none';
        document.getElementById('error').style.display = 'none';
        
        // Reset defaults
        document.getElementById('LZZ').value = '2';
        document.getElementById('KVZ').value = '1.7';
        document.getElementById('STKL').value = '1';
        document.getElementById('AJAHR').value = '2025';
        document.getElementById('VJAHR').value = '2025';
        document.getElementById('f').value = '1.0';
        document.getElementById('af').value = '1';
    }
}

function printResult() {
    window.print();
}

// --- Calculation History --- //

const MAX_HISTORY_ITEMS = 10;

function getHistory() {
    return JSON.parse(localStorage.getItem('calculationHistory') || '[]');
}

function saveToHistory(inputData, result) {
    let history = getHistory();
    const timestamp = new Date();
    const name = `Berechnung vom ${timestamp.toLocaleDateString()} um ${timestamp.toLocaleTimeString()}`;

    const historyItem = {
        name: name,
        timestamp: timestamp.toISOString(),
        inputData: inputData,
        result: result
    };

    history.unshift(historyItem); // Add to the beginning

    if (history.length > MAX_HISTORY_ITEMS) {
        history = history.slice(0, MAX_HISTORY_ITEMS);
    }

    localStorage.setItem('calculationHistory', JSON.stringify(history));
    renderHistory();
}

function loadFromHistory(timestamp) {
    const history = getHistory();
    const item = history.find(h => h.timestamp === timestamp);

    if (item) {
        // Populate form with saved data
        Object.keys(item.inputData).forEach(key => {
            const element = document.getElementById(key);
            if (element) {
                if (element.type === 'checkbox') {
                    element.checked = item.inputData[key] === 1;
                } else {
                    element.value = item.inputData[key];
                }
            }
        });

        // Display the results of the loaded calculation
        updateDisplayResults(item.result, item.inputData);
        alert(`Berechnung \'${item.name}\' geladen.`);
    } else {
        alert('Fehler: Berechnung nicht in der Historie gefunden.');
    }
}

function deleteFromHistory(timestamp) {
    if (confirm('Möchten Sie diesen Eintrag wirklich löschen?')) {
        let history = getHistory();
        history = history.filter(h => h.timestamp !== timestamp);
        localStorage.setItem('calculationHistory', JSON.stringify(history));
        renderHistory();
    }
}

function renderHistory() {
    const historyList = document.getElementById('history-list');
    const historyCard = document.getElementById('history-card');
    const history = getHistory();

    historyList.innerHTML = ''; // Clear current list

    if (history.length === 0) {
        historyCard.style.display = 'none';
        return;
    }

    historyCard.style.display = 'block';

    history.forEach(item => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';

        const textSpan = document.createElement('span');
        textSpan.textContent = item.name;
        textSpan.style.cursor = 'pointer';
        textSpan.onclick = () => loadFromHistory(item.timestamp);

        const deleteButton = document.createElement('button');
        deleteButton.className = 'btn btn-sm btn-outline-danger';
        deleteButton.innerHTML = '<i class="bi bi-trash"></i>';
        deleteButton.onclick = () => deleteFromHistory(item.timestamp);

        li.appendChild(textSpan);
        li.appendChild(deleteButton);
        historyList.appendChild(li);
    });
}



// Export functions

function exportToPDF() {
    if (!currentInputData || !currentResult) {
        alert('Bitte führen Sie zuerst eine Berechnung durch.');
        return;
    }
    
    const name = prompt('Name für den Export (optional):', '');
    const exportData = {input_data: currentInputData, result: currentResult, name: name || null};
    
    fetch('http://127.0.0.1:8000/api/v1/export/pdf', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(exportData),
    })
    .then(response => response.ok ? response.blob() : Promise.reject('Export fehlgeschlagen'))
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `lohnsteuer_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    })
    .catch(error => alert('Fehler beim PDF-Export: ' + error));
}

function exportToExcel() {
    if (!currentInputData || !currentResult) {
        alert('Bitte führen Sie zuerst eine Berechnung durch.');
        return;
    }
    
    const name = prompt('Name für den Export (optional):', '');
    const exportData = {input_data: currentInputData, result: currentResult, name: name || null};
    
    fetch('http://127.0.0.1:8000/api/v1/export/excel', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(exportData),
    })
    .then(response => response.ok ? response.blob() : Promise.reject('Export fehlgeschlagen'))
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `lohnsteuer_${new Date().toISOString().split('T')[0]}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    })
    .catch(error => alert('Fehler beim Excel-Export: ' + error));
}

// Main form submission
document.getElementById('tax-form').addEventListener('submit', function (e) {
    e.preventDefault();
    console.log('Form submitted');

    const form = e.target;
    if (!form.checkValidity()) {
        console.log('Form validation failed');
        return;
    }

    const data = collectFormData();
    console.log('Sending data:', data);

    fetch('http://127.0.0.1:8000/api/v1/calculate_payroll_tax', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
    })
    .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(result => {
        console.log('Received result:', result);
        updateDisplayResults(result, data);
        saveToHistory(data, result); // Save to history
        document.getElementById('result').style.display = 'block';
        document.getElementById('error').style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
        const errorDiv = document.getElementById('error');
        errorDiv.textContent = 'Fehler bei der Berechnung: ' + (error.detail || error.message || JSON.stringify(error));
        errorDiv.style.display = 'block';
        document.getElementById('result').style.display = 'none';
    });
});

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    renderHistory(); // Render history on page load
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    console.log('Page loaded, tooltips initialized');
    
    // Add API test button
    const testButton = document.createElement('button');
    testButton.textContent = 'API Test';
    testButton.className = 'btn btn-info btn-sm';
    testButton.style.position = 'fixed';
    testButton.style.top = '10px';
    testButton.style.right = '10px';
    testButton.style.zIndex = '9999';
    testButton.onclick = function() {
        fetch('http://127.0.0.1:8000/')
            .then(response => response.json())
            .then(data => {
                console.log('API Test successful:', data);
                alert('API ist erreichbar: ' + data.message);
            })
            .catch(error => {
                console.error('API Test failed:', error);
                alert('API nicht erreichbar. Fehler: ' + error.message);
            });
    };
    document.body.appendChild(testButton);
});