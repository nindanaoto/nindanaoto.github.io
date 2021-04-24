---
marp: true
---
<!-- 
theme: default
size: 16:9
paginate: true
footer : ![](image/ccbysa.png) [licence](https://creativecommons.org/licenses/by-sa/4.0/)
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

# 完全準同型暗号入門

佐藤研究室 松岡　航太郎
matusoka.kotaro@gmail.com

---

## 準同型暗号とは？

- 「暗号文のママ計算できる」暗号
- 平文に対する演算と準同型な演算を暗号上で定義できる
- 概念が提案されたのは1978年(RSAと同年)

---

## 準同型暗号の例: RSA暗号

- $p,q∈ℙ,n=pq,e≤ϕ(n)=(p-1)(q-1),d=e⁻¹ \bmod n$とする
- $c,m$を暗号文と平文を示すものとする
- 暗号化: $c ≡ mᵉ \bmod n$, 復号 $mᵈ \bmod n$'
- 実はこれが乗算について準同型暗号になっていることを見よう
- すなわち、２つの暗号文を掛け算して復号すると平文の掛け算が得られる
- $(c_1 ⋅ c_2)^d = (m_1^e ⋅ m_2^e)^d = (m_1⋅m_2)^{ed} ≡ m_1⋅m_2 \bmod n$

---

## 準同型暗号の種類

今日では以下の4つに分けられる   
基本的に上に行くほど制限が強く、下に行くほど計算が重い

- 部分(Partially)準同型暗号 (PHE): 加算か乗算だけをサポートするもの
    - ex. RSA暗号、ElGamal暗号、Paillier暗号など
- Somewhat HE: 両方できるが演算回数に暗号形式に依存した制限が在るもの
    - 格子ベースでないものは知る限りではここが限界
- Leveled HE: 演算回数の制限がパラメータで変更できるもの
    - 暗号上で評価する関数の空間を暗号化時に制限する必要が在る
- 完全(Fully)準同型暗号: 任意の関数が評価できる
    - 知られているものは格子ベース
    - 今日の本題なので詳しくは後述

---

## Learning With Error (LWE)

- 最もよく知られている格子暗号でNP困難なShort Vector Problemに依拠する(提案はRegevさんの2005年)
- これの拡張が耐量子暗号の候補として[NIST Round3](https://csrc.nist.gov/projects/post-quantum-cryptography/round-3-submissions)まで生き残っている
- ここでは全係数が剰余環上にとられるInteger LWEを紹介する
- $n,q∈ℤ$を公開パラメータ、$\mathbf{s},\mathbf{a}∈ℤ_q^n$は各係数が一様分布、$e∈ℤ_q$は正規分布に従って取られるものとする
- $\mathbf{s}$は秘密鍵で、$e$はエラー(またはノイズ)
- $ℤ_q∋b=\mathbf{a}⋅\mathbf{s}+m+e$として、$(\mathbf{a},b)$の組が暗号文
- 復号は$b-\mathbf{a}⋅\mathbf{s}=m+e$から一番近いあり得る平文に丸める

---

## LWEの加法準同型性

- 実はLWEはそのままでも加法が定義できることを確認する
- $(\mathbf{a}_1,b_1)+(\mathbf{a}_2,b_2)=(\mathbf{a}_1+\mathbf{a}_2,b_1+b_2)$とする
$$\begin{aligned}(b_1+b_2)-(\mathbf{a}_1+\mathbf{a}_2)⋅\mathbf{s}&=(b_1-\mathbf{a}_1⋅\mathbf{s})+(b_2-\mathbf{a}_2⋅\mathbf{s})\\&=m_1+m_2+e_1+e_2\end{aligned}$$
- ここで重要なのは加法によってエラー$e$も増えること
- 復号では丸めを行うのでエラーが増えすぎると誤ったメッセージに丸める可能性が在る
- ∴任意の関数を評価するにはエラーを除去する必要が在る

---

## Bootstrapping

- 準同型暗号上で復号関数を評価することでエラーを除去する操作のこと
- Gentryさんはこれを最初に提案し、構成を与えた
- 現状の完全準同型暗号は全てこれによって構成されている
- あとでTFHEにおけるBootstrappingのアイデアを見る

---

## 完全準同型暗号

以下の4つの世代に分けられる
- 第１世代: SHEを使ってBootstrappingを構成したもの
  - 効率の問題などで現実に用いられることはほぼない
- 第２世代:  剰余環上の乗算と加算をサポートするもの
  - 第２世代を構成する過程でLHEが作られ、以降はそれをベースとしている
  - ex. BGV(Brakerski-Gentry-Vaikuntanathan),BFV(Brakerski/Fan-Vercauteren)
- 第３世代: バイナリ演算をサポートするもの
  - Bootstrappingが他の世代に比して高速(1000倍のオーダ)
  - ex. GSW(Gentry-Sahai-Waters),TFHE(Torus FHE)
- 第４世代: 有限精度複素数演算をサポートするもの
  - 実数が扱えるので深層学習用途に人気
  - ex. CKKS(Cheon-Kim-Kim-Song)

---

## TFHE

- 知られている中で最も高速なBootstrapping(10msオーダ)
- バイナリ演算以外の非線形演算の評価にも適している(ReLUなど)
- 