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
- PHE(Partial): 加算だけもしくは乗算だけできるHE (RSAとか)
- SHE(Somewhat): 両方できるが乗算の回数に暗号方式に依存した回数制限がある
- LHE(Leveled): 両方できるがパラメータ依存で乗算の回数制限があるもの

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

- Torus Ring Learning With Errorsの略
  - LWEの多項式環版のトーラス係数版
- 多項式を暗号化する暗号化方式
- Ringは多項式『環』の上で定義することから来ている
  - 課題でやってもらった多項式の剰余演算が出てくる
  - 厳密にはTorus係数多項式だと環じゃない気がする
    - 後に見るようにTorusには乗算が定義できない

---

## Torusの直感的定義

- 日本語で言うと円周群のこと。$\mathbb{T}$とかく。
- 時計の針の角度をイメージすると良い
- 具体的な数字としては針の角度を2πで割ったもの

---

## Torusとは

- ここでは、$\mathbb{R} \bmod 1$を定義とする。つまり、実数の小数部分で、$[0,1)$または$[-0.5,0.5)$に値をとる
  - 理論を理解する上では$[-0.5,0.5)$だけでもよい
  - $[0,1)$は実装上効率が良い場合が在る
- Torus同士の乗算は定義されないが、加算は定義できる
- 加算の例: $0.8+0.6=1.4≡0.4 \bmod 1,0.3-0.9=-0.6 ≡ 0.4 \bmod 1$
- 乗算が定義できない。例: $1.2≡0.2 \bmod 1,2.4≡0.4 \bmod 1$なので、乗算が定義できるなら$1.2⋅ 2.4=2.88≡0.2⋅0.4=0.08\bmod 1$だが成立しない。
- 整数($\mathbb{Z}$)との乗算は定義できる。例:$3⋅ 0.4≡ 0.2 \bmod 1$

---

## モジュラー正規分布

- Modular Gaussian Distribution。
- 通常の正規分布のサンプルは実数($\mathbb{R}$)に値をとるが、これはTorusに値をとる
  - 離散ガウス分布は整数に丸めるがこれはTorus
  - 実際の実装は整数に近似するので離散正規分布を使うべき説はある
- 正規分布のサンプルを$\bmod 1$したものがモジュラー正規分布
  - これをエラーに使うのがTFHEでは最も標準的なのでまずはこれから


---

## TRLWEの具体的構成(平文が$\mathbb{T}_N[X]$の場合)

- 暗号の安全性を決めるパラメータは2つで$N∈\mathbb{Z}^+,α_{bk} \in \mathbb{R}^+$
- $\mathbf{a}[X] ∈ \mathbb{T}_N[X],b[X],m[X],e[X] \in \mathbb{T}_N[X], S[X] \in \mathbb{B}^\pm_N[X]$とする
  - $\mathbb{B}^\pm = {-1,0,1}$は一般にTernaryと呼ぶ(表記は一般的ではない)
- $m[X]$が平文、$\mathbf{a}[X]←U_{\mathbb{T}_N[X]}$,$e[X]←\mathcal{D}_{\mathbb{T}_N[X],α_{bk}}$,$S[X]←U_{(\mathbb{B}^\pm_N[X])^k}$とする
- TRLWEの暗号文は$b[X]=a[X]⋅ S[X]+ m[X] +e[X]$として、$(a[X],b[X])$という$N-1$次の多項式$2$要素のベクトルである
- $b[X]-a[X]⋅S[X]=m[X]+e[X]$になるので、この$e[X]$をどうにかして削除する方法を加えると$m[X]$がとれて復号できる
- $N,k,α_{bk}$を大きくすればするほど安全($α_{bk}$は大きくしすぎると暗号文が壊れる)
- 同じ安全性・データならTLWEよりTRLWEはサイズが小さい(と信じられている)

---

## TRLWEの具体的構成(平文が$(\mathbb{Z}_t)_N[X]$の場合, BFVの暗号文)

- $m[X] \in (\mathbb{Z}_t)[X], Δ=\frac{1}{t}\in\mathbb{T}$とする
- TRLWEの暗号文は$b[X]=a[X]\cdot S[X]+Δ⋅ m[X]+e[X]$
- 復号は$\lceil (b[X]-a[X]\cdot S[X])/Δ\rfloor$
  - ここの丸めはuintでやった方が考えやすいかも?

---

## OffTopic: TRLWEの安全性の直感的理解

- $a[X]\cdot S[X]$は行列ベクトル積としてかける
  - $a[X]$の係数で作った巡回行列と$S[X]$の係数のベクトル
    - つまり$A\cdot \mathbf{S} = \mathbf{b} - \mathbf{e} + \mathbf{m}$みたいな形にできる
- $A$の逆行列が計算できるとすると, もしこれが実数の話なら最小二乗法的な話に落ちる
  - 実際はTorusで周期性があるのでもっと難しいが
  - 最小二乗法だと思うと, ノイズがないとすぐ解けそうということはわかるはず
- 一般の解法については「格子暗号解読のための数学的基礎」とかを読むと良い

---

## Torusの実装法

- 実数の小数部の集合なのでナイーブには倍精度浮動小数点数で実装したくなる
  - ただ、倍精度浮動小数点数で$\bmod 1$の計算をするのは重い
- そこで、小数点が最上位bitの前にあるような固定小数点数を用いることにする
- 例:8bit幅の場合、$0.5$は$0b1000000$、$0.375$は$0b01100000$になる
- この方法だと加算や乗算で出た整数部分はオーバーフローで捨てられ剰余が不要
- 例:8bit幅の場合、$0.5+0.625 \bmod 1=0b1000000+0b10100000=0b0010000=0.125 \bmod 1$
- 固定小数点数の幅は$e$が十分に表現できる程度の幅($q$)であれば良い
  - つまりモジュラー正規分布の標準偏差によって十分な幅が決まる
- 符号付きで考えたほうが一般性があるためそちらを想定するが符号なしでも構成できるはず
  - 符号付きが必要な時だけ切り替えればよい

---

## 実数とトーラスの変換の実装

- モジュラー正規分布の実装には実数とTorusの変換が必要
- 理想的には実数の小数部分を取り出す操作
- 実数の小数部分を取り出すだけなら、$d \mod{1}$でよい
- 実際には固定幅の固定小数点にしたいので、実数の上から$\mathrm{lb}\ q$の部分を整数として取り出す
- $\bmod 1$はPythonだと正の数になるのでuintにしてからintにする
  - Python組み込みのIntの場合, intへの変換は$q/2$を以上なら$q/2$を引く
  - NumpyならCと同じでuint64をint64にするとbit列として解釈され意図通り
- 実装したい操作を数式で書くと以下のようになる

$$
\mathrm{uint}(\mathrm{int}((d \mod{1})⋅q))
$$

---

## 多項式環上の乗算

- ここではナイーブな実装を扱う(課題1の想定回答の疑似コード)
- ２つの元を掛け算, その剰余を取り, 係数の小数部を抜き出せば良い
  - 係数の型を適切にとればオーバフローにより係数の剰余は自動的にとれる
- 入力を$a[X]∈\mathbb{T}_N[X],b[X]∈\mathbb{Z}_N[X]$とする
  - 実装上は両方整数なので気にすることはないが
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

## 演習タイム(課題3)

- ここまで説明したTRLWEの暗号化と復号を実装しよう
  - 課題3のテストが通ればとりあえずよし
  - 本当はちゃんとした乱数生成器を使う必要があるが, 今回はそこには目を瞑ることにする
    - 乱数の品質が低いと暗号が脆弱になる
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
  - 乗算するために片方を$q'$倍して整数に丸める
$$
\begin{aligned}
\lceil q'\cdot(b_0[X] -  a_0[X] \cdot S[X]) \rfloor \cdot (b_1[X] - a_1[X]\cdot S[X]) &= \lceil q'\cdot (m_0[X] \cdot \Delta + e[X])\rfloor \cdot (m_1[X] \cdot \Delta + e_1[X])\\
\approx \lceil q' \cdot b_0[X] \rfloor \cdot b_1[X] - (\lceil q' \cdot a_0[X]\rfloor \cdot b_1[X] + a_1[X] \cdot \lceil q' \cdot b_0[X] \rfloor) \cdot S[X] + \lceil q'\cdot a_0[X]\rfloor \cdot a_1[X] \cdot S[X]^2 & \approx  \lceil q' \cdot m_0[X] \cdot m_1[X] \cdot \Delta^2 \rfloor + e_2[X]\\
(\frac{\lceil q' \cdot b_0[X] \rfloor \cdot b_1[X] - (\lceil q' \cdot a_0[X]\rfloor \cdot b_1[X] + a_1[X] \cdot \lceil q' \cdot b_0[X] \rfloor) \cdot S[X] + \lceil q'\cdot a_0[X]\rfloor \cdot a_1[X] \cdot S[X]^2}{q'\cdot\Delta}) \bmod 1& \approx  \lceil m_0[X] \cdot m_1[X] \cdot \Delta \rfloor e_2[X]
\end{aligned}
$$

- ということは乗算結果の新しい暗号文として$\lceil\frac{(\lceil q' \cdot a_0[X]\rfloor \cdot b_1[X] + a_1[X] \cdot \lceil q' \cdot b_0[X] \rfloor, \lceil q' \cdot b_0[X] \rfloor \cdot b_1[X],  \lceil q' \cdot a_0[X]\rfloor \cdot a_1[X] )}{q'\cdot\Delta}\rfloor = (a_2[X], b_2[X], c_2[X])$ を与えれば乗算になる
  - この形の暗号文の名前は把握していない
  - $q'\cdot\Delta$で割るので乗算は剰余を取らずに実数として考えて実行する
  - あるいは先にTorusを$q'\cdot\Delta$で割っていると考える
    - Torusはdivisible gorupでもあるので整数で割ることはvalidな演算(のはず)

---

## 実装における実際の挙動

- $q'$は本来$q$とは独立に選べる
  - しかし明らかに$q'< q$のとき丸め誤差が入る
  - $q'=q$に取ってしまえばここを考えなくていい
  - 見たことある実装は基本的にこのアプローチ
- つまり実装上は$q'$は出てこなくてすべての多項式を整数係数多項式だと思って$q\cdot \Delta$で割ればいい
  - 実装上は$\Delta$も$\mod q$上なので$\Delta$で割る形で書くことになる
    - 課題3での$\Delta$の定義を参照のこと
- つまりコード上はこんな見た目になる

$\lceil\frac{(a_0[X] \cdot b_1[X] + a_1[X] \cdot b_0[X], b_0[X] \cdot b_1[X],  a_0[X] \cdot a_1[X] )}{\Delta}\rfloor = (a_2[X], b_2[X], c_2[X])$

---

## 実装的な実数での乗算の扱い

- 除算して乗算の上側をとることになるので一時的に64bitより大きい計算が必要
  - long double(x86のWindows以外の環境なら80bit)で計算するのが一番楽?
    - numpyで実装できる
    - 誤差が出るが, 暗号のエラーと区別できないのであまり問題でない
    - 提供する高速版はこのアプローチが自然にとれるようにしてある
  - 精度を維持したいならPythonの整数型は精度に上限がないのでそれも簡単
    - おそらく見れる速度にはならないのでやめた方がいい
- 除算した後は64bitに丸めなおす
  - ちょっとノイズが増えるが, そうしないと小数部分がどんどん伸びてしまう
  - 実装上遅いし扱いが面倒なだけでダメなわけではない

---

## 演習タイム(課題4,5,6)

- 課題4の暗号文の加算は自明なのでテストを走らせるだけ
  - 暗号化・復号実装がちゃんとしていればきっと動くはず
- 課題5はテストしやすいように分離しているだけ
  - ExtendedEncryptは実際は全く使わないので, ExtendedDecryptの実装だけ書いて終わりでも良い
  - 課題6でMulとどっちが悪いのかわからなくなると困りそうなので一応分けた
- 課題6の乗算は実のところ多項式の乗算を適切に扱うのが一番面倒かも
  - Extendedpolymul
  - 必要であれば自分でもう一つテストを書くと良いかもしれない
    - テスト提供するとほぼ答えなので分けていない
  - 提供している高速多項式実装の場合, 最後にuintでcastする前に割れば良い
- ExtendedDecryptionは$(a_2[X], b_2[X], c_2[X])$
  - $S[X]^2$が必要な項があることに注意

---

## Relinearlization(アイデア)

- 乗算をすると出力の暗号文は次元が$3$になってしまう
  - 乗算をこのまま続けていくとどんどん次元が増えてしまう
  - 絶対にだめなわけではないが計算効率が急速に下がる
- 乗算で増えてしまった次元を減らすのがRelinearlization
- $(a_2[X],b_2[X]) - (0,c[X] \cdot S[X]^2)$ が計算できれば次数が元に戻る
  - $c[X] \cdot S[X]^2$を計算するには$S[X]^2$を$S[X]$で暗号化して送ってやればいい
  - このために使われるのがGLevと呼ばれる暗号形式

---

## 整数多項式とTorus多項式の積

- いきなりGLevの具体的構成をみてもモチベーションがわからない
- やりたい演算を順次構成していくことでGLevを導出する
- 以下のような演算を復号せずにやりたい(準同型暗号上の多項式乗算)
- 乗算の結果の3要素の暗号文の$S[X]^2$と掛ける項を$c[X]$とする
- 計算したいのは$S[X]^2\cdot c[X]$
  - 整数係数多項式とTorus多項式の積
---

## スケーリング

- Glevの構成には2つ重要なアイデアがあり、１つがスケーリング
- TRLWEは整数係数多項式をそのまま平文にすることはできない
- $S^2[X]$をTorus係数にしてその分を$c[X]$に押し付けて整数係数に丸める
  - 丸めの分だけノイズが増えることに注意
- $Bg\in\mathbb{Z},Bg>|S[X]^2|_\infty$
- ノイズ($e[X]$)が$\lceil Bg\cdot c[X]\rfloor$倍されることに留意
$\begin{aligned}
\lceil Bg\cdot c[X]\rfloor \cdot (a[X], a[X]\cdot S[X] + \frac{S[X]^2}{Bg} + e[X])
\end{aligned}$

---

## $Bg$に関するトレードオフ

- $\lceil Bg⋅c[X]\rfloor$の係数の最大値は$Bg$
- つまり$Bg$を大きくすると$e[X]$が増幅される
- しかし$Bg$を小さくすると丸めによる誤差が大きくなる
  - $Bg=q$に取ればなくなるがそんな値は取れない
- このトレードオフから逃れるのがDecomposition

---

## Decomposition(一般的定義)

- 丸めるときに$Bg$を基数とみなして$l$桁に分解する
  - $Bg$を大きくせずに丸めによるノイズを減らせる
- Decompositionは多項式$c[x]∈T_N[X]$を入力にとる
- 出力として多項式のベクトル$\mathbf{\bar c}[X]∈(\mathbb{Z}_N[X])^l$を返す
  - 要素となる多項式の係数は入力となる多項式の係数の一桁を抜き出したもの
  - Torusを$Bg$進表現したときの１番上の桁を集めたもの、次の桁という具合でベクトルの要素は並ぶ
- $\bar c_{ij}$は$\mathop{\rm arg~min}\limits_{\bar c_{ij}} ∑^{N-1}_{j=0}(a_j-∑_{i=1}^{l}\frac{\bar c_{ij}}{Bg^i})^2\ s.t.\ \bar c_{ij}∈[-\frac{Bg}{2},\frac{Bg}{2})$を満たす
  - $[0,Bg)$でなく$[-\frac{Bg}{2},\frac{Bg}{2})$にとるのはノイズを小さくしたいから
- $\bar c_i[X]$を$0≤j≤N-1$次の係数が$\bar c_{ij}$である多項式とする
- 多項式のベクトル$\mathbf{\bar c}[X]$の$1≤i≤l$番目の要素を$\bar c_i[X]$として返す
---

## Decompositionでつくるもの

- 逆操作を先に見ることでイメージを得よう
- $⌈Bg⋅c[X]⌋$は$l=1$の場合のDecompositionになっている

$
c[X]≈ (\bar c_1[X],\cdots,\bar c_l[X]) \cdot (\frac{1}{Bg}, \frac{1}{Bg^2}, \cdots, \frac{1}{Bg^l})^T
$

---

## Decomposition(具体的構成)

- $\bar c_i[X]$を具体的に与えるアルゴリズムを示していく
  - 簡単のため$Bg=2^{Bgbit}$と書ける場合に限定する
  - Torusはuint64_tで表現されているものとする
    - 符号付きで考えると面倒になってしまうので一時的にcast
- $[-\frac{Bg}{2},\frac{Bg}{2})$だと係数が負になる場合を考える必要がある
- 各桁に$\frac{Bg}{2}$をたすことで$[0,Bg)$にずらす
- こうするとbitマスクで取り出すだけで良くなる
  - このあたりが面倒になる
- 最後に各係数から$\frac{Bg}{2}$を引いて元に戻す
  - 戻したら符号付きに戻る

---

## Decomposition(基本的アイデア)

- 前提としてもし各桁を$[0,Bg)$の範囲で取るならmaskだけで良い
  - $[0,Bg)$にとる場合を$\hat c$とする
  - つまり$\hat c_{ij}=(((c_i+2^{64-Bgbit⋅l-1})>>(64-Bgbit⋅i))\&(Bg-1))$
  - $2^{64-Bgbit⋅l-1}$は四捨五入のための定数
  - これは$\mathop{\rm arg~min}\limits_{\hat{c}_{ij}} ∑^{N-1}_{j=0}(c_j-∑_{i=1}^{l}\frac{\hat{c}_{ij}}{Bg^i})^2\ s.t.\ \hat{c}_{ij}\in[0,Bg)$を満たす
- $c[X]から\mathbf{\hat c}[X]$を経由した$\mathbf{\bar c}[X]$への変換を考える
  - 以下のような関係が成り立つように$\bar c_{ij}$を決めることができる(要は桁上がりをしている)
$$
\hat c_{ij} = \begin{cases} Bg+\bar c_{ij}\qquad if\quad \hat c_{ij}≥\frac{Bg}{2}\\ \bar c_{ij}\qquad otherwise\end{cases}
$$

---

## Decomposition(疑似コード)

- このアイデアをナイーブに実装した場合の疑似コードを示そう
  - ほぼ繰り上がり計算なので加算機でやる最適化が可能だが複雑になりすぎる
  - Torusは64bit固定小数点表現されていることを仮定している

```
Decomposition(c[X])
  roundoffset = 1 << (32 - l * Bgbit - 1)
  for i from 1 to l
    for j from 0 to N-1
      ̂cᵢⱼ=(((aⱼ+roundoffset)>>(64-Bgbit*i))&(Bg-1))
  for i from l to 1
    for j from 0 to N-1
      if ̂c ᵢⱼ ≥ Bg/2
        c̄ᵢⱼ = ĉᵢⱼ - Bg
        ĉ₍ᵢ₋₁₎ⱼ += 1
      else
        c̄ᵢⱼ = ĉᵢⱼ
  return c̄[X]
```
---

## Glevの具体的構成

- Decompostionを$c[X]$に施して掛け算をすると考えるとGLevの暗号文は以下
  - 今回は平文が$S[X]^2$だけなのでそう書いているが一般には他のものでも良い
- 要はTRLWEのベクトル
  - 各行の$a[X],e[X]$は独立に選ぶ
$
\left(
    \begin{array}{cc}
      a_0[X] & a_0[X]\cdot S[X] + \frac{S[X]^2}{Bg} + e_0[X]\\
      a_1[X] & a_1[X]\cdot S[X] + \frac{S[X]^2}{Bg^2} + e_1[X]\\
      \vdots&\vdots\\
      a_{l-1}[X] & a_{l-1}[X]\cdot S[X] + \frac{S[X]^2}{Bg^l} + e_{l-1}[X]\\
    \end{array}
\right)
$

---

## $l$に関するトレードオフ

- $l$を増やせば丸めのノイズを減らすことができる
- $l$を増やすとGLev暗号文由来のノイズが増える
  - たくさん足し合わせることになるので
- $l$は丸めには指数で効き0の暗号文由来には線形で効く
  - トレードオフの出方が$Bg$と違う
  - ノイズを最小化する$l,Bg$の組が存在する
- $l$を増やすほどExternal Productの多項式乗算が増えて重くなる
  - ノイズが許容される範囲で$l$を小さくとりがち

---

## 演習タイム(課題7)
- RelinearlizationKeyGenが$S[X]^2$を平文とするGLevの暗号化関数
  - 復号は(一般の場合でも知る限り)使わないので必要ない
- かなり計算が複雑になるので提供する高速多項式実装の利用を推奨
  - もちろん自前の実装が十分速いならそれでも問題ない
  - 模範解答として作った実装だと1回7sかかった
    - Ryzen 9800X3D上なので, ノートパソコンだと3倍くらいはかかるかも
  - 時間が余ったら高速化を試みると良い
    - Numpyの使い方の工夫だけでも早くなったりするかも
    - PyPy, Codon, Numba, Cythonあたりも試す?

---

## 参考文献

- [B/FV原論文(Brakerski)](https://eprint.iacr.org/2012/078)
- [B/FV原論文(Fan-Vercauteren)](https://eprint.iacr.org/2012/144)
- [The Chinese Remainder Theorem](https://math.berkeley.edu/~kmill/math55sp17/crt.pdf) 
- [Introduction to BFV](https://inferati.com/blog/fhe-schemes-bfv)
- [Bootstrapping for HElib](https://eprint.iacr.org/2014/873)
- [BFVのGPU実装](https://github.com/lightbulb128/troy-nova.git)


---

## Advanced Topics

- 時間が余ったら喋ろうと思っている話題のリスト
  - バッファとして消費する可能性もあるので喋らないかも
  - その時の様子で内容は決める

1. RNS&Double Decomposition
2. Fast Polynomial Multiplication
3. Bootstrapping (Lifting)
4. Packing
5. CLPX

---

## Packing

- Canonical Embeddingと呼ばれることもある
  - Embeddingは日本語で言えば埋め込みで[wiki](https://ja.wikipedia.org/wiki/%E5%9F%8B%E3%82%81%E8%BE%BC%E3%81%BF_(%E6%95%B0%E5%AD%A6))によると数学的構造間の構造を保つような単射のことらしい
- BFVの特徴としてよく言われるもの
  - (CKKSもだが)一般にはこちらの方式がよく使われる
- Packingは平文のエンコーディング方法の一つ
  - 暗号文の演算としては変わらない
- RLWEに見られる性質として, 加算に関しては係数ごとに並列な演算ができる
  - 乗算に関しても独立な計算ができたら便利そう
    - $t$を法とするNTTをかけてやればこれが達成できる 
      - $t=2^{16}+1$とかがよくつかわれる
    - CKKSだとFFT
    - 厳密には$N$次全てを使うのでなければNTTとして完全に分解できる必要はないので$t$を$2$とかにとってもよい
      - $t$の下で$X^N+1$が分解できる式の数が並列で扱えるスカラーの数
$b[X] = a[X] \cdot S[X] + \lceil NTT_t(m[X]) \cdot \Delta \rfloor + e[X]$

---

## Slot2Coeff/Coeff2Slot

- Packingで値を詰めた場合の各値のことをSlotと呼ぶ
  - たぶんSIMDレジスタ的な気持ち
- しかしBootstrappingなどをするときには多項式の係数に対して考えたほうが楽な場合が多い
  - 平文がNTTがかかってる状態のやつを暗号上でINTTをかけて係数に平文が来るようにしたい
- Nai\"eveな実装はとても簡単
  - NTTやINTTは行列(Vandermonde matrix)とベクトルの積として書ける
    - これをKeySwitchingとしてやればよい

---

## Lifting

- Bootstrappingをするにはノイズを消去する必要がある
  - SampleExtractIndexしてTFHEでBootsrapingする方法も知られてはいる
- BFV固有のBootstrappingのアイデアとしてLiftingがある
  - 平文を基数$p$で分解できる($t=p^e$)ものとして最下位を得る演算
    - 最下位を得られればそれを引けば最下位が消去できる
- 最も単純なものは$p=2,3$の場合
  - $p$乗して引くことを繰り返すだけ

---

## Liftingの疑似コード

- [Bootstrapping for HElib](https://eprint.iacr.org/2014/873)のFigure 1より
  - jのLoopのところがLifting
  - これで最上位桁を取り出せる

```
Digit Extraction(z,e)
w₀,₀ ← z
For k ← 0 to e-1
  y ← z
  For j ← 0 to k
    wⱼ,ₖ₊₁ ← (wⱼ,ₖ)ᵖ
    y ← (y - wⱼ,ₖ₊₁)/p
  wₖ₊₁,ₖ₊₁
return wₑ,ₑ
```

---