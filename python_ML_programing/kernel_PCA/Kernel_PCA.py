from scipy.spatial.distance import pdist, squareform
from scipy import exp
from scipy.linalg import eigh
import numpy as np

def rbf_kernel_pca(X, gamma, n_components):

    """ RBF カーネル PCA

    パラメータ
    ------------------
    X: (Numpy ndarray), shape = [n_samples, n_features]

    gamma: float
        RBF カーネルのチューニングパラメーター

    n_components: int
        返される主成分の個数

    戻り値
    ------------------
    alphas: {Numpy ndarray}, shape = [n_samples, k_featrures]
        射影されたデータセット

    lambdas: list
        固有値

    """

    # MxN 次元のデータセットでペアごとのユークリッド距離の２乗を計算
    sq_dists = pdist(X, 'sqeuclidean')

    # ペアごとの距離を正方行列に変換
    mat_sq_dists = squareform(sq_dists)

    # 対象カーネル行列を計算
    K = exp(-gamma * mat_sq_dists)

    # カーネル行列を中心化
    N = K.shape[0]
    one_n = np.ones((N,N)) / N
    K = K - one_n.dot(K) - K.dot(one_n) + one_n.dot(K).dot(one_n)

    # 中心化されたカーネル行列から固有対を取得
    # scipy.linalg.eighはそれらを昇順で返す
    eigvals, eigvecs = eigh(K)
    eigvals, eigvecs = eigvals[::-1], eigvecs[:,::-1]

    # 上位k個の固有ベクトル（射影されたサンプル）を収集
    alphas = np.column_stack((eigvecs[:, i] for i in range(n_components)))

    #対応する固有値を収集
    lambdas = [eigvals[i] for i in range(n_components)]

    return alphas, lambdas
