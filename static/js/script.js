// static/js/script.js

document.getElementById('searchButton').addEventListener('click', function() {
    const inputText = document.getElementById('inputText').value.trim();
    if (!inputText) {
        alert('请输入文本后再进行查询。');
        return;
    }

    // 发送POST请求到后端
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

        // 清空之前的结果
        const resultsList = document.getElementById('resultsList');
        resultsList.innerHTML = '';

        const similarities = [];

        // 显示结果
        data.results.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `
                <strong>文档索引：</strong>${item.index}<br>
                <strong>相似度：</strong>${item.similarity}<br>
                <strong>文档类别：</strong>${item.category}<br>
                <strong>文档内容预览：</strong>${item.preview}
            `;
            resultsList.appendChild(li);
            similarities.push(item.similarity);
        });

        // 绘制柱状图
        drawChart(similarities, data.results.map(item => `索引 ${item.index}`));
    })
    .catch(error => {
        console.error('Error:', error);
        alert('发生错误，请稍后再试。');
    });
});

function drawChart(similarities, labels) {
    const ctx = document.getElementById('similarityChart').getContext('2d');

    // 如果之前有图表，先销毁
    if (window.similarityBarChart) {
        window.similarityBarChart.destroy();
    }

    window.similarityBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '余弦相似度',
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
