import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

class NewsLSA:
    """
    一个用于加载20newsgroups数据集、创建词项-文档矩阵、应用SVD降维
    以及计算文档相似度的类。
    """

    def __init__(self, subset='all', n_components=100, stop_words='english', max_df=0.5, random_state=42):
        self.subset = subset
        self.n_components = n_components
        self.stop_words = stop_words
        self.max_df = max_df
        self.random_state = random_state

        # 加载数据集
        self.newsgroups = fetch_20newsgroups(subset=self.subset)
        print("number of data", len(self.newsgroups.data))

        # 创建词项-文档矩阵
        self.vectorizer = TfidfVectorizer(stop_words=self.stop_words, max_df=self.max_df)
        self.X = self.vectorizer.fit_transform(self.newsgroups.data)
        print("shape:", self.X.shape)

        # 应用奇异值分解（SVD）进行降维
        self.svd = TruncatedSVD(n_components=self.n_components, random_state=self.random_state)
        self.X_reduced = self.svd.fit_transform(self.X)
        print(f"re_shape: {self.X_reduced.shape}")

    def cosine_similarity_manual(self, vec1, vec2):
        """
        手动计算两个向量之间的余弦相似度。

        参数：
        - vec1 (numpy.ndarray): 第一个向量。
        - vec2 (numpy.ndarray): 第二个向量。

        返回：
        - float: 余弦相似度值。
        """
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
        return dot_product / (norm_vec1 * norm_vec2)

    def compute_cosine_similarity(self, input_text, top_n=5):
        """
        计算输入文档与所有降维后文档的余弦相似度，并返回最相似的前N个文档。

        参数：
        - input_text (str): 输入文档文本。
        - top_n (int): 返回最相似的前N个文档，默认5。

        返回：
        - List[Tuple[int, float]]: 每个元组包含 (文档索引, 余弦相似度)。
        """
        # 将输入文档转换为 TF-IDF 向量
        input_tfidf = self.vectorizer.transform([input_text])

        # 使用 SVD 将 TF-IDF 向量降维
        input_reduced = self.svd.transform(input_tfidf)[0]  # 获取一维数组

        # 计算输入向量与所有文档的余弦相似度（向量化方法）
        dot_products = np.dot(self.X_reduced, input_reduced)
        norms_X = np.linalg.norm(self.X_reduced, axis=1)
        norm_input = np.linalg.norm(input_reduced)
        similarities = dot_products / (norms_X * norm_input + 1e-10)  # 加小常数避免除零

        # 获取前N个相似度最高的索引
        top_indices = np.argsort(similarities)[-top_n:][::-1]
        top_similar = [(idx, similarities[idx]) for idx in top_indices]

        return top_similar

    def get_document_preview(self, idx, length=200):
        """
        获取指定文档的内容预览。

        参数：
        - idx (int): 文档索引。
        - length (int): 预览的字符长度，默认200。

        返回：
        - str: 文档内容预览。
        """
        if idx < 0 or idx >= len(self.newsgroups.data):
            return "无效的文档索引。"
        return self.newsgroups.data[idx][:length].replace('\n', ' ') + "..."

    def get_document_category(self, idx):
        """
        获取指定文档的类别名称。

        参数：
        - idx (int): 文档索引。

        返回：
        - str: 文档类别名称。
        """
        if idx < 0 or idx >= len(self.newsgroups.target):
            return "无效的文档索引。"
        return self.newsgroups.target_names[self.newsgroups.target[idx]]
