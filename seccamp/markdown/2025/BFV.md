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

- ここではナイーブな実装を扱う(課題1の想定回答の疑似コード)
- ２つの元を掛け算, その剰余を取り, 係数の小数部を抜き出せば良い
  - 係数の型を適切にとればオーバフローにより係数の剰余は自動的にとれる
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

## TRLWEの具体的構成(平文が$(\mathbb{Z}_t)_N[X]$の場合, BFVの暗号文)

- $m[X] \in (\mathbb{Z}_t)[X], Δ=\frac{1}{t}\in\mathbb{T}$とする
- TRLWEの暗号文は$b[X]=\mathbf{a}[X]⋅ \mathbf{s}[X]+Δ⋅ m[X]+e[X]$
- 復号は$\lceil (b[X]-\mathbf{a}[X]⋅ \mathbf{s}[X])/Δ\rfloor$

---

## 演習タイム(課題3)

- ここまで説明したTRLWEを実装しよう
- $q=2^{64}, N=2^{11}, α=2^{-51}$

---

## BFVの加算

- TRLWEは加法準同型性が成り立つ
- ２つの暗号文$(\mathbf{a}[X]_1,b[X]_1),(\mathbf{a}[X]_2,b[X]_2)$を考える
- その和を$(\mathbf{a}[X]_1+\mathbf{a}[X]_2,b[X]_1+b[X]_2)$とする
- $b_1[X]+b_2[X]-(a_1[X]+a_2[X])⋅s[X]=Δ \cdot (m_1[X]+m_2[X])+e_1[X]+e_2[X]$になり、$m_1[X]+m_2[X]$が出てくるので加法準同型になっている
- TLWEよりサイズが小さいのでより高速に加算ができることになる
  - 係数ごとに独立した加算なのでSIMDライク
- ノイズも加算されているので回数には限界がある

---

## BFVの乗算(naive)

- TRLWEは乗算に近いものも定義できる
$$
\begin{aligned}
(b_0[X] -  a_0[X] \cdot S[X]) \cdot (b_1[X] - a_1[X]\cdot S[X]) &= (\lceil m_0[X] \cdot \Delta \rfloor + e[X]) \cdot (\lceil m_1[X] \cdot \Delta \rfloor + e_1[X])\\
b_0[X] \cdot b_1[X] - (a_0[X] \cdot b_1[X] + a_1[X] \cdot b_0[X]) \cdot S[X] + a_0[X] \cdot a_1[X] \cdot S[X]^2 & \approx  \lceil m_0[X] \cdot m_1[X] \cdot \Delta^2 \rfloor + e_2[X]\\
\lceil \frac{b_0[X] \cdot b_1[X] - (a_0[X] \cdot b_1[X] + a_1[X] \cdot b_0[X]) \cdot S[X] + a_0[X] \cdot a_1[X] \cdot S[X]^2}{\Delta} \rfloor& \approx  \lceil m_0[X] \cdot m_1[X] \cdot \Delta \rfloor e_2[X]
\end{aligned}
$$

- ということは乗算結果の新しい暗号文として$\lceil\frac{(a_0[X] \cdot b_1[X] + a_1[X] \cdot b_0[X], b_0[X] \cdot b_1[X],  a_0[X] \cdot a_1[X] )}{\Delta}\rfloor = (a_2[X], b_2[X], c_2[X])$ を与えれば乗算になる
  - $\Delta$で割るので乗算は剰余を取らずに実数として考えて実行する

---

## 実装的な実数での乗算の扱い

- 除算して乗算の上側をとることになるので一時的に64bitより大きい計算が必要
  - long double(x86のWindows以外の環境なら80bit)で計算するのが一番楽?
    - numpyで実装できる
    - ちょっと誤差が出るが, 暗号のエラーと区別できないのであまり問題ではない
  - 精度を維持したいならPythonの組み込み整数型は精度に上限がないのでそれも簡単
- 除算した後は64bitに丸めなおす
  - ちょっとノイズが増えるが, そうしないと小数部分がどんどん伸びてってしまう
  - 実装上遅いし扱いが面倒なだけでダメなわけではない

---

## 演習タイム(課題4,5)

- 課題4の暗号文の加算は自明なのでテストを走らせるだけ
  - 暗号化・復号実装がちゃんとしていればきっと動くはず
- 課題5の乗算は実のところ多項式の乗算を適切に扱うのが一番面倒かも
  - 必要であれば自分でもう一つテストを書くと良いかもしれない
  - 提供している高速多項式実装の場合, 最後にintでcastする前に割れば良い
  - 
---

## Relinearlization(アイデア)

- 乗算をすると出力の暗号文は次元が$3$になってしまう
  - 乗算をこのまま続けていくとどんどん次元が増えてしまう
  - 絶対にだめなわけではないが計算効率が急速に下がる
- 乗算で増えてしまった次元を減らすのがRelinearlization
- $(a_2[X],b_2[X]) - (0,c[X] \cdot S[X]^2)$ が計算できれば次数が元に戻る
  - $c[X] \cdot S[X]^2$を計算するには$S[X]^2$を$S[X]$で暗号化して送ってやればいい
  - 

---

## 整数多項式対角行列とTRLWEの積

- いきなりTRGSWの具体的構成をみてもモチベーションがわからない
- TRGSWを使ってやりたい演算を構成していくことでTRGSWを導出する
- 以下のような演算を復号せずにやりたい(準同型暗号上の多項式乗算)
  - 加法ができることは既に見ている
  - 簡単のためここでは$k=2$を仮定する
- この行列の部分をどうにかして暗号文にしたのがTRGSW

$\begin{aligned}
μ[X]&∈\mathbb{Z}_N[X]\\
μ[X]⋅(a_0[X],a_1[X],b[X])&=(a_0[X],a_1[X],b[X])⋅
\left(
    \begin{array}{ccc}
      μ[X] & 0 & 0\\
      0 & μ[X] & 0\\
      0 & 0 & μ[X]\\
    \end{array}
  \right)
\end{aligned}$

---

## スケーリング

- TRGSWの構成には３つ重要なアイデアがあり、１つがスケーリング
- TFHEで考える暗号文は整数係数多項式をそのまま平文にすることはできない
- 行列の方をTorus係数にしてその分をTRLWEに押し付けて整数係数に丸める
  - 丸めの分だけノイズが増えることに注意
- $Bg\in\mathbb{Z},Bg>μ[X],e_r[X]∈\mathbb{T}_N[X]$
- $e_r[X]$は丸めによるノイズ
- ノイズが$μ[X]$倍されることに留意
$\begin{aligned}
⌈Bg⋅(a_0[X],a_1[X],b[X])⌋⋅&
\left(
    \begin{array}{ccc}
      \frac{μ[X]}{Bg} & 0 & 0\\
      0 &  \frac{μ[X]}{Bg}  & 0\\
      0 & 0 & \frac{μ[X]}{Bg}
    \end{array}
  \right)=(a_0^r[X],a_1^r,b^r[X])\\
  &≈μ[X]⋅(a_0[X],a_1[X],b[X])\\
  b^r[X]-\mathbf{a}^r[X]⋅\mathbf{s}[X] &= μ[X](b[X] - \mathbf{a}[X]⋅\mathbf{s}[X]+e_r[X])
\end{aligned}$

---

## 零行列加算

- 行列に0を暗号化したTRLWEを加算することで行列を隠す(暗号文でマスクする)
  - 足した後の行列はTRLWEのベクトルとして解釈できる
- $(\mathbf{a}_i[X],b_i[X])$は0を暗号化したTRLWE
- つまり、$b_i[X]-\mathbf{a}_i[X]⋅s[X]=0+e_i[X]$
  - 0の暗号文を定数倍し足しても0の暗号でノイズが増えるだけ

$
\begin{array}{cc}
&⌈Bg⋅(\mathbf{a}[X],b[X])⌋⋅[
\left(
    \begin{array}{ccc}
      \frac{μ[X]}{Bg} & 0 & 0\\
      0 & \frac{μ[X]}{Bg} & 0\\
      0 & 0 & \frac{μ[X]}{Bg}
    \end{array}
  \right)+
  \left(
    \begin{array}{cc}
      \mathbf{a}_0[X] & b_0[X] \\
      \mathbf{a}_1[X] & b_1[X] \\
      \mathbf{a}_2[X] & b_2[X]
    \end{array}
  \right)]\\
  ≈&μ[X]⋅(\mathbf{a}[X],b[X])+⌈Bg⋅a_0[X]⌋⋅(\mathbf{a}_0[X],b_0[X])\\
  &+⌈Bg⋅a_1[X]⌋⋅(\mathbf{a}_1[X],b_1[X])+⌈Bg⋅b[X]⌋⋅(\mathbf{a}_2[X],b_2[X])  
\end{array}
$

---

## 何をしているか

- スペースの都合でこれは$k=1$
![](../../image/zeromatrixadd.jpg)

---

## $Bg$に関するトレードオフ

- $⌈Bg⋅a[X]⌋,⌈Bg⋅b[X]⌋$の係数の最大値は$Bg$
- つまり$Bg$を大きくすると0の暗号文由来のノイズが大きく影響する
- しかし$Bg$を小さくすると丸めによるノイズが大きくなる
- このトレードオフから逃れるのがDecomposition

---

## Decomposition(一般的定義)

- TRLWEを丸めるときに$Bg$を基数とみなして$l$桁に分解する
  - $Bg$を大きくせずに丸めによるノイズを減らせる
- Decompositionは多項式$a[x]∈T_N[X]$を入力にとる
- 出力として多項式のベクトル$\mathbf{ā}[X]∈(\mathbb{Z}_N[X])^l$を返す
  - 要素となる多項式の係数は入力となる多項式の係数の一桁を抜き出したもの
  - Torusを$Bg$進表現したときの１番上の桁を集めたもの、次の桁という具合でベクトルの要素は並ぶ
- $ā_{ij}$は$\mathop{\rm arg~min}\limits_{ā_{ij}} ∑^{N-1}_{j=0}(a_j-∑_{i=1}^{l}\frac{ā_{ij}}{Bg^i})^2\ s.t.\ ā_{ij}∈[-\frac{Bg}{2},\frac{Bg}{2})$を満たすとする
  - $[0,Bg)$でなく$[-\frac{Bg}{2},\frac{Bg}{2})$にとるのはノイズを小さくしたいから
- $ā_i[X]$を$0≤j≤N-1$次の係数が$ā_{ij}$である多項式とする
- 多項式のベクトル$\mathbf{ā}[X]$の$1≤i≤l$番目の要素を$ā_i[X]$として返す
---

## Decompositionでつくるもの

- 逆操作を先に見ることでイメージを得よう
  - スペースの都合でk=1の場合にしている
- $⌈Bg⋅(a[X],b[X])⌋$は$l=1$の場合のDecompositionになっている

$
(a[X],b[X])≈ (ā_1[X],...,ā_l[X],b̄_1[X],...,b̄_l[X])
\left(
    \begin{array}{cc}
      \frac{1}{Bg} & 0 \\
      \frac{1}{Bg^2} & 0 \\
      ⋮ & ⋮\\
      \frac{1}{Bg^l} & 0 \\
      0 & \frac{1}{Bg}\\
      0 & \frac{1}{Bg^2}\\
      ⋮&⋮\\
      0 & \frac{1}{Bg^l}\\
    \end{array}
\right)
$

---

## Decomposition(具体的構成)

- $ā_i[X]$を具体的に与えるアルゴリズムを示していく
  - 簡単のため$Bg=2^{Bgbit}$と書ける場合に限定する
  - Torusはuint32_tで表現されているものとする
- $[-\frac{Bg}{2},\frac{Bg}{2})$だと係数が負になる場合を考える必要がある
- 各桁に$\frac{Bg}{2}$をたすことで$[0,Bg)$にずらす
- こうするとbitマスクで取り出すだけで良くなる
- 最後に各係数から$\frac{Bg}{2}$を引いて元に戻す

---

## Decomposition(基本的アイデア)

- 前提としてもし各桁を$[0,Bg)$の範囲で取るならmaskだけで良い
  - $[0,Bg)$にとる場合を$â$とする
  - つまり$â_{ij}=(((aᵢ+2^{32-Bgbit⋅l-1})>>(32-Bgbit⋅i))\&(Bg-1))$
  - $2^{32-Bgbit⋅l-1}$は四捨五入のための定数
  - これは$\mathop{\rm arg~min}\limits_{\hat{a}_{ij}} ∑^{N-1}_{j=0}(a_j-∑_{i=1}^{l}\frac{\hat{a}_{ij}}{Bg^i})^2\ s.t.\ \hat{a}_{ij}\in[0,Bg)$を満たす
- $a[X]から\mathbf{â}[X]$を経由した$\mathbf{ā}[X]$への変換を考える
  - 以下のような関係が成り立つように$ā_{ij}$を決めることができる(要は桁上がりをしている)
$$
â_{ij} = \begin{cases} Bg+ā_{ij}\qquad if\quad â_{ij}≥\frac{Bg}{2}\\ ā_{ij}\qquad otherwise\end{cases}
$$

---

## Decomposition(疑似コード)

- このアイデアをナイーブに実装した場合の疑似コードを示そう
  - やっていることはほぼ繰り上がり計算なので加算機にそれを任せる最適化が可能だが複雑になりすぎるのでここでは説明しない
  - Torusは32bit固定小数点表現されていることを仮定している
  - 式に合わせるために分けているがâを更新して返してもよい

```
Decomposition(a[X])
  roundoffset = 1 << (32 - l * Bgbit - 1)
  for i from 1 to l
    for j from 0 to N-1
      âᵢⱼ=(((aⱼ+roundoffset)>>(32-Bgbit*i))&(Bg-1))
  for i from l to 1
    for j from 0 to N-1
      if âᵢⱼ ≥ Bg/2
        āᵢⱼ = âᵢⱼ - Bg
        â₍ᵢ₋₁₎ⱼ += 1
      else
        āᵢⱼ = âᵢⱼ
  return 𝐚̄[X]
```
---

## TRGSWの具体的構成(平文が$\mathbb{Z}_N[X]$の場合)

- DecompostionをTRLWEに施して掛け算をすると考えると$k=1$の暗号文は以下
  - 実際は平文空間は$\mathbb{B}$だけでもHomNANDはつくれる
$
\left(
    \begin{array}{cc}
      \frac{μ[X]}{Bg} & 0 \\
      \frac{μ[X]}{Bg^2} & 0 \\
      ⋮ & ⋮\\
      \frac{μ[X]}{Bg^l} & 0 \\
      0 & \frac{μ[X]}{Bg}\\
      0 & \frac{μ[X]}{Bg^2}\\
      ⋮&⋮\\
      0 & \frac{μ[X]}{Bg^l}\\
    \end{array}
\right)+
\left(
    \begin{array}{cc}
      a_1[X] & b_1[X] \\
      a_2[X] & b_2[X] \\
      ⋮ & ⋮\\
      a_l[X] & b_l[X] \\
      a_{l+1}[X] & b_{l+1}[X]\\
      a_{l+2}[X] & b_{l+2}[X]\\
      ⋮&⋮\\
      a_{2l}[X] & b_{2l}[X]\\
    \end{array}
\right)
$

---

## $l$に関するトレードオフ

- $l$を増やせば丸めのノイズを減らすことができる
- $l$を増やすと0の暗号文由来のノイズが増える
- $l$は丸めには指数で効き0の暗号文由来には線形で効く
- $l$を増やすほどExternal Productの多項式乗算が増えて重くなる
- トレードオフの出方が$Bg$と違う

---

## 演習タイム(課題6)

- かなり計算が複雑になるので提供する高速多項式実装の利用を推奨
  - もちろん自前の実装が十分速いならそれでも問題ない
  - 模範解答として作った実装だと1回7sかかった
    - Ryzen 9800X3D上なので, ノートパソコンだと3倍くらいはかかるかも