---
marp: true
---
<!-- 
theme: default
size: 16:9
paginate: true
footer : ![](../../image/ccbysa.png) [licence](https://creativecommons.org/licenses/by-sa/4.0/)
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
    a {
    font-weight:bold;
    color:#F00;
  } 
-->

<!-- page_number: true -->


# TFHE実装入門

## Appendix

松岡　航太郎

---

## Notation(General)

- 普通の文字はスカラー、$[X]$がついていたら多項式
- 太字はベクトル、太字の大文字は行列
- $\mathbb{B}$: Binary,{0,1}
- $\mathbb{Z}$: 整数の集合
- $\mathbb{Z}^+$: 正整数の集合
- $\mathbb{T}$: Torusの集合,$\mathbb{R} \bmod 1$
- $U_{\mathbb{T}^n}$: $\mathbb{T}$から$n$個の値を独立にとる一様分布。ベクトルを返す。
- $U_{\mathbb{B}^n}$: $\mathbb{B}$から$n$個の値を独立にとる一様分布。ベクトルを返す。
- $\mathcal{D}_{\mathbb{T},α}$: 平均$0$標準偏差$α$のモジュラー正規分布。
- $μ$: 定数、1/8
---

## Notation(General)

- $\leftarrow$: $x\leftarrow D$ は $x$ それ自身かその要素あるいはその係数が分布$D$からとられることを意味する。

---

## Notation(TLWE)

- $\mathbf{s}∈ \mathbb{B}^n$: TLWEの秘密鍵。$\mathbf{s}←U_{\mathbb{B}^n}$
- $\mathbf{a}∈ \mathbb{T}$: TLWEの一部。$\mathbf{a}←U_{\mathbb{T}^n}$
- $e∈ \mathbb{T}$: TLWEのノイズ。$e←\mathcal{D}_{\mathbb{T},α}$
- $m$: スカラーの平文
- $b∈ \mathbb{T}$: TLWEの一部。$m∈\mathbb{T}$の場合、$b=\mathbf{a}⋅ \mathbf{s}+ m +e$

---

## Notation(TRLWE)

- $m[X]∈\mathbb{T}[X]$: 平文のTorus係数多項式

---

## Notation(TRGSW)

- $μ[X]∈\mathbb{Z}[X]$: 平文の整数係数多項式
- $⌈⋅⌋$: 丸め関数

---

## 128 bit Security Parameter

- $n=635$
- $N=1024$