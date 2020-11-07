---
marp: true
---
<!-- 
theme: default
size: 16:9
paginate: true
footer : ![](../image/ccbysa.png) [licence](https://creativecommons.org/licenses/by-sa/4.0/)
style: |
  h1, h2, h3, h4, h5, header, footer {
        color: white;
    }
  section {
    background-color: #505050;
    color:white
  }
  table{
      color:black
  }
  code{
    color:black
  }
-->

<!-- page_number: true -->

# Canonical Embedding

松岡　航太郎

---

## Canonical Embeddingとは

- Embeddingは日本語で言えば埋め込みで[wiki](https://ja.wikipedia.org/wiki/%E5%9F%8B%E3%82%81%E8%BE%BC%E3%81%BF_(%E6%95%B0%E5%AD%A6))によると数学的構造間の構造を保つような単射のことらしい
- ここで扱うのはBGVやCKKSで出てくる$X^N+1$の零点に値を埋め込むこと
- TRLWEでは係数に値を入れていたので違う
- どうやって埋め込むかを考えてそれからその特性を見る

---

## 多項式の補間

- まず$N$個の点$\{(x_0,y_0),(x_1,y_1),...,(x_{N-1},y_{N-1})\}$を$N-1$次の多項式で補間することを考えよう
- つまりある多項式$p$があって、$∀i∈[0,N),p(x_i)=y_i$となる$p$をつくる
- そのためには以下の性質を満たす$N$個の多項式$g_i$を構成すれば良い
$$g_i(x_j)=\begin{cases}1\qquad if\quad i==j\\ 0\qquad otherwise\end{cases}$$
- これがあれば明らかに$p=∑_{i=0}^{N-1}y_ig_i$でよい

---

## $g_i$の構成

- $h(x)=∏_{i=0}^{N-1}(x-x_i)$

---

## 参考文献

- [The Chinese Remainder Theorem](https://math.berkeley.edu/~kmill/math55sp17/crt.pdf)