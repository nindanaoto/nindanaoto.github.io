---
marp: true
---
<!--
theme: default
size: 16:9
paginate: true
footer : ![](../../seccamp/image/ccbysa.png) [licence](https://creativecommons.org/licenses/by-sa/4.0/)
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

# Turorial for B/FV

松岡　航太郎

---

## 自己紹介

- 京都大学大学院情報学研究科 佐藤高史 研究室 博士課程
- 京都大学工学部電気電子工学科卒　特色入試
- 東京都立戸山高等学校卒
- 2019年度未踏スーパークリエータ
- 京都大学機械研究会(2019年度NHK学生ロボコン優勝)
- 趣味は読書
- 卒業研究は超伝導体と磁性体を含む動電磁界シミュレーション
- 修士論文はTFHEのFPGA実装, 最近ASICも作った

---

## 目標

- B/FVの乗算を実装し、背景となる理論を説明できるようになること
- 目に見える目標は乗算のテストが動くPython実装の製作

---

## 準同型暗号とは？

- Homomorphic Encryption
- 「暗号文のママ計算できる」暗号
- 平文に対する演算と準同型な演算を暗号上で定義できる
- 概念が提案されたのは1978年(RSAと同年)
- DARPA、Intel、IBM、Microsftなどが鎬を削っている
- 流行りの応用は医療データなどの機密性の高いデータを扱うPrivate AI
- [標準化](https://homomorphicencryption.org/standard/)の動きも在る
  - [ISO/IEC 18033-6:2019(en) IT Security techniques — Encryption algorithms — Part 6: Homomorphic encryption](https://www.iso.org/obp/ui/#iso:std:iso-iec:18033:-6:ed-1:v1:en)

---

## Fully Homomorphic Encryptionとは？

- FHEとよく略す。日本語で言えば完全準同型暗号。
- 暗号文を入力として、暗号文のママ『任意』の関数を適用できるような暗号
  - 整数の暗号文であれば任意の回数加算と乗算ができることが十分条件
  - bitの暗号文であれば任意の回数NANDができることが十分条件
- TFHEは後者で論理回路として表現できる関数なら評価可能

---

## FullyじゃないHomomorphic Encryption

- 多くのHEは剰余環上の整数に対する演算をサポートしている
- PHE(Partial): 加算だけもしくは乗算だけできるHE
- SHE(Somewhat): 両方できるが、乗算の回数に暗号方式に依存した回数制限がある
- LHE(Leveled): 両方できるが、パラメータ依存で乗算の回数制限があるもの

---

## FHEの世代

- [wikipedia](https://en.wikipedia.org/wiki/Homomorphic_encryption)が詳しい
- 第1世代FHE: Gentryさんの博士論文(2009)など
- 第2世代FHE: Brakerski-Gentry-Vaikuntanathan (BGV, 2011)など
- 第3世代FHE: Craig Gentry, Amit Sahai, and Brent Waters (GSW,2013)やTFHE(2016)など
- 第4世代FHE:  Cheon Jung Hee, Kim Andrey, Kim Miran, Song Yongsoo(CKKS, 2017)

---

# B/FV

- Brakerski-Fan-Vercauteren の略
- 有限体上の計算を行う
  - 各係数が剰余環の値であるような多項式の剰余が成す体
    - 剰余環は整数を割った余りの成す環
    - 有限体は有限な元が成す体なので法が素数なら剰余環も有限体になる
    
- BFVとよく似た方式にBGVが存在する
  - MSB側に平文を乗っけるかLSB側に平文を乗っけるかの違いしかない
    - 相互にノイズの増大があるだけで変換できることが知られている
  - 歴史的にはBGVが先
    - 両方とも第２世代に分類される

---

## 講義の流れ

- 以下のような章構成として, 各章の後に実装時間を設けます
  - 最後の章は昼食後にアドバンスドな話とかするだけなので最悪省略
  - 実装は既定の時間が終了しかつ半数以上の人が達成したら終了の予定
- Relinearlizationは時間内に実装できるか怪しい
  - 時間内にできなくても落ち込まないで

1. 導入とTRLWEの暗号化と復号(今)
2. TRLWEの加法性と乗法性
3. Relinearlization
4. RNSととBootstrapping
---

## TRLWEとは

- Torus Ring-LWEの略
- TLWEは平文がスカラーだったが、TRLWEでは多項式になる
- Ringは多項式『環』の上で定義することから来ている
  - 課題でやってもらった多項式の剰余演算が出てくる
  - 厳密にはTorus係数多項式だと環じゃない気もしないでもない

---

## 多項式環上の乗算

- この処理がTFHEで一番重い処理なので高速化したいならここを高速化すべき
  - FFT(高速フーリエ変換)かNTT(数論変換)を使って実装するのが知る限り最速
- ここではナイーブな実装を扱う(知る限り最適な実装は7章で扱う)
  - 課題2.1で扱ったもの
- ２つの元を掛け算、剰余を取り、係数の小数部に相当する部分を抜き出せば良い
- 入力を$a[X]∈\mathbb{T}_N[X],b[X]∈\mathbb{Z}_N[X]$とする
- $a[X]=\sum_{i=0}^{N-1}a_iX^i,a_i∈\mathbb{T}$である

```
for i from 0 to N-1
  cᵢ = 0
for i from 0 to N-1
  for j from 0 to N-1
    if i+j<N
      cᵢ₊ⱼ += aᵢ⋅bⱼ
    else
      cᵢ₊ⱼ₋ₙ -= aᵢ⋅bⱼ (Nの下付きが打てないのでₙになっている)
```

---

## TRLWEの具体的構成(平文が$\mathbb{T}_N[X]$の場合)

- 暗号の安全性を決めるパラメータは3つで$N,k∈\mathbb{Z}^+,α_{bk} \in \mathbb{R}^+$
  - 厳密には$k=1$の場合のみがTRLWEで$k>1$の場合はTMLWEと呼ぶべきか
    - 本講義ではTRLWEと一緒くたに呼ぶ
- $\mathbf{a}[X] ∈ (\mathbb{T}_N[X])^k,b[X],m[X],e[X] \in \mathbb{T}_N[X], \mathbf{s}[X] \in (\mathbb{B}^\pm_N[X])^k$とする
  - $\mathbb{B}^\pm = {-1,0,1}$は一般にTernaryと呼ぶ(表記は一般的ではない)
  - binaryだと安全性が足らなくなるので増やす
- $m[X]$が平文、$\mathbf{a}[X]←U_{(\mathbb{T}_N[X])^k}$,$e[X]←\mathcal{D}_{\mathbb{T}_N[X],α_{bk}}$,$\mathbf{s}[X]←U_{(\mathbb{B}_N[X])^k}$とする
- TRLWEの暗号文は$b[X]=\mathbf{a}[X]⋅ \mathbf{s}[X]+ m[X] +e[X]$として、$(\mathbf{a}[X],b[X])$という$N-1$次の多項式$k+1$要素のベクトルである
- $b[X]-\mathbf{a}[X]⋅\mathbf{s}[X]=m[X]+e[X]$になるので、この$e[X]$をどうにかして削除する方法を加えると$m[X]$がとれて復号できる
- $N,k,α_{bk}$を大きくすればするほど安全($α_{bk}$は大きくしすぎると暗号文が壊れる)
- 同じ安全性・データならTLWEよりTRLWEはサイズが小さい(と信じられている)

---

## TRLWEの加法準同型性

- TLWEとTRLWEはよく似ているので加法準同型性も同じように成り立つ
- ２つの暗号文$(\mathbf{a}[X]_1,b[X]_1),(\mathbf{a}[X]_2,b[X]_2)$を考える
- その和を$(\mathbf{a}[X]_1+\mathbf{a}[X]_2,b[X]_1+b[X]_2)$とする
- $b_1[X]+b_2[X]-(a_1[X]+a_2[X])⋅s[X]=m_1[X]+m_2[X]+e_1[X]+e_2[X]$になり、$m_1[X]+m_2[X]$が出てくるので加法準同型になっている
- TLWEよりサイズが小さいのでより高速に加算ができることになる
  - 係数ごとに独立した加算なのでSIMDライク

---

## TRLWEの具体的構成(平文が$\mathbb{B}_N[X]$の場合)

- これもTLWEと似た形
- $m[X] \in \mathbb{B}[X],μ=1/8 \in\mathbb{T}$とする
- $(μ(2⋅ m[X]-1[X])∈\mathbb{T}_N[X])$である
- TRLWEの暗号文は$b[X]=\mathbf{a}[X]⋅ \mathbf{s}[X]+μ(2⋅ m[X]-1[X])+e[X]$
- 復号は$(1+\mathit{sgn}(b[X]-\mathbf{a}[X]⋅ \mathbf{s}[X]))/2$($\mathit{sgn}$は符号関数で各係数に作用)

---

## 演習タイム

- ここまで説明したTRLWEを実装しよう

---

## BFVの乗算

- 加算はTFHEと同じなので割愛
$$
\begin{aligned}
(b_0[X] -  a_0[X] \cdot S[X]) \cdot (b_1[X] - a_1[X]\cdot S[X]) &= (\lceil m_0[X] \cdot \Delta \rfloor + e[X]) \cdot (\lceil m_1[X] \cdot \Delta \rfloor + e_1[X])\\
b_0[X] \cdot b_1[X] - (a_0[X] \cdot b_1[X] + a_1[X] \cdot b_0[X]) \cdot S[X] + a_0[X] \cdot a_1[X] \cdot S[X]^2 & \approx  \lceil m_0[X] \cdot m_1[X] \cdot \Delta^2 \rfloor + e_2[X]\\
\lceil \frac{b_0[X] \cdot b_1[X] - (a_0[X] \cdot b_1[X] + a_1[X] \cdot b_0[X]) \cdot S[X] + a_0[X] \cdot a_1[X] \cdot S[X]^2}{\Delta} \rfloor& \approx  \lceil m_0[X] \cdot m_1[X] \cdot \Delta \rfloor e_2[X]
\end{aligned}
$$

- ということは新しい暗号文として$\lceil\frac{(a_0[X] \cdot b_1[X] + a_1[X] \cdot b_0[X], b_0[X] \cdot b_1[X],  a_0[X] \cdot a_1[X] )}{\Delta}\rfloor = (a_2[X], b_2[X], c_2[X]$ を与えれば乗算になる
  - $\Delta$で割るので乗算は剰余を取らずに実数として考えて実行する

---

## Relinearlization

- 見ての通り出力の暗号文は次元が$3$になってしまう
  - 乗算をこのまま続けていくとどんどん次元が増えてしまう
- 乗算で増えてしまった次数を減らすのがRelinearlization
  - 実体としてはKeySwitchingと同じ
- $(a_2[X],b_2[X]) - (0,c[X] \cdot S[X]^2)$ が計算できれば次数が元に戻る
  - $c[X] \cdot S[X]^2$を計算するには$S[X]^2$を$S[X]$で暗号化して送ってやればいい
    - 乗算によるノイズ増加のトレードオフはTRGSWのExternalProductと一緒
      - S[X]を平文とするTRGSWの下半分($a[X]$の部分が$0$なので)だけ用意すればいい

---