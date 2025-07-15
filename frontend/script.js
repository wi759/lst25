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

// Helper function to get number value from input and convert to cents
function getCentsValue(id) {
    const element = document.getElementById(id);
    if (!element) {
        console.error(`Element with ID '${id}' not found.`);
        return 0; // Return 0 or handle as appropriate
    }
    const value = parseFloat(element.value);
    if (isNaN(value)) {
        return 0;
    }
    return Math.round(value * 100);
}

document.getElementById('tax-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const form = e.target;
    if (!form.checkValidity()) {
        return;
    }

    const data = {
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

    fetch('http://127.0.0.1:8000/api/v1/calculate_payroll_tax', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(result => {
            document.getElementById('LSTLZZ').textContent = (result.LSTLZZ / 100).toFixed(2) + ' €';
            document.getElementById('SOLZLZZ').textContent = (result.SOLZLZZ / 100).toFixed(2) + ' €';
            document.getElementById('BK').textContent = (result.BK / 100).toFixed(2) + ' €';

            // Convert Decimal strings to numbers for calculation
            const lstlzz = parseFloat(result.LSTLZZ) || 0;
            const solzlzz = parseFloat(result.SOLZLZZ) || 0;
            const bk = parseFloat(result.BK) || 0;

            const total = (lstlzz + solzlzz + bk) / 100;
            document.getElementById('TOTAL').textContent = total.toFixed(2) + ' €';

            document.getElementById('result').style.display = 'block';
            document.getElementById('error').style.display = 'none';
        })
        .catch(error => {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = 'Fehler bei der Berechnung: ' + (error.detail || JSON.stringify(error));
            errorDiv.style.display = 'block';
            document.getElementById('result').style.display = 'none';
        });
});
