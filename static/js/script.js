// static/js/script.js

document.getElementById('searchButton').addEventListener('click', function() {
    const inputText = document.getElementById('inputText').value.trim();
    if (!inputText) {
        alert('Please insert words');
        return;
    }

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input_text: inputText, top_n: 5 })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        const resultsList = document.getElementById('resultsList');
        resultsList.innerHTML = '';

        const similarities = [];

        data.results.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `
                <strong>Ineex：</strong>${item.index}<br>
                <strong>Similarity：</strong>${item.similarity}<br>
                <strong>Category：</strong>${item.category}<br>
                <strong>Preview：</strong>${item.preview}
            `;
            resultsList.appendChild(li);
            similarities.push(item.similarity);
        });

        // 绘制柱状图
        drawChart(similarities, data.results.map(item => `Index ${item.index}`));
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Erroe occurs, try again');
    });
});

function drawChart(similarities, labels) {
    const ctx = document.getElementById('similarityChart').getContext('2d');

    if (window.similarityBarChart) {
        window.similarityBarChart.destroy();
    }

    window.similarityBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Similarity',
                data: similarities,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                }
            }
        }
    });
}
