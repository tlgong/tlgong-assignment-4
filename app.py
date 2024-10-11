# app.py

from flask import Flask, render_template, request, jsonify
from main import NewsLSA

app = Flask(__name__)

# 初始化 NewsGroupsSimilarity 类
similarity_model = NewsLSA()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    input_text = data.get('input_text', '')
    top_n = data.get('top_n', 5)

    if not input_text:
        return jsonify({'error': '输入文本为空。'}), 400

    try:
        # 计算相似度
        top_similar = similarity_model.compute_cosine_similarity(input_text, top_n=top_n)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # 准备返回的数据
    results = []
    for idx, sim in top_similar:
        category = similarity_model.get_document_category(idx)
        preview = similarity_model.get_document_preview(idx)
        results.append({
            'index': int(idx),  # 转换为标准的 int
            'similarity': round(float(sim), 4),
            'category': category,
            'preview': preview
        })

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
