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

# Garbled Circuit

松岡　航太郎

---

## Garbled Circuitとは

- GCと略されることが多いがGarbage Collectionではない
- 主にはAESなどの普通の暗号を使って秘密計算をやる仕組み
- 準同型暗号と並べて扱われることも多い
- 名前の通り論理演算を行う

---

## Garbled Circuitの基本的発想

- AESなどでは暗号文と鍵とがほぼ同じ形式になっている
- AESだとブロック長が128bitで鍵が256bitなので２ブロックと対応
- ということは暗号文を秘密鍵として解釈し直すことができる
- 出力を入力の暗号文を鍵として暗号化してやれば正しい組のときだけ復号できる

---

## Garbled Table

- 前のスライドのアイデアをNANDを例として具体的に書くと下の図のようになる
- 実際はこの表(Garbled Table)はどういう論理ゲートかを隠すためにランダムに並び替える
- $\rm{Enc}(p,sk,r)$は$p$が平文、$sk$が秘密鍵、$r$がある乱数の暗号文
- $A_1:=\rm{Enc}(1,sk,a_1)$のように定義する

||$A_1$|$A_0$|
|---|---|---|
|$B_1$|$\rm{Enc}(\rm{Enc}(C_1,B_1,b_{11}),A_1,a_{11})$|$\rm{Enc}(\rm{Enc}(C_0,B_1,b_{10}),A_0,a_{10})$|
|$B_0$|$\rm{Enc}(\rm{Enc}(C_0,B_0,b_{01}),A_1,a_{01})$|$\rm{Enc}(\rm{Enc}(C_0,B_0,b_{00}),A_0,a_{00})$|

---

## Garbled Circuit の高速化

- よく使われるのはFreeXORとHalfAND
- FreeXORはその名の通り暗号文同士をXORするだけでXORゲートの処理をできるようにする
- HalfANDは暗号文の表を2項目だけに減らす
- これらは関数を隠さない場合に適用できる
- 復号が成功したか失敗したかを判定するのは難しいので暗号文の1bitをランダムなフラグにしてどの暗号文なら成功するかを埋め込むこともできる

---

## Garbled Circuitの問題点

- もしあり得る入力すべてにアクセスできると関数と平分がバレる
- それを避けるのに紛失通信が使われる
- 複数回評価することができない