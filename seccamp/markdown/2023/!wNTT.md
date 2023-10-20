---
marp: true
---
<!-- 
theme: default
size: 16:9
paginate: true
footer : https://nindanaoto.github.io ![](../../image/ccbysa.png) [licence](https://creativecommons.org/licenses/by-sa/4.0/)
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

# 数論変換における最新の研究動向

京都大学 佐藤研究室 D1 松岡　航太郎

---

## 普段の研究

- 準同型暗号が専門
    - 暗号のまま計算ができる暗号
    - 今日の話も準同型暗号と密接に関わりのある話
- 研究室は集積回路
    - 今準同型暗号を高速化できるハードウェアを作ったりしてる
- 京都大学工学部電気電子工学科卒　特色入試
- 東京都立戸山高等学校卒
- 2019年度未踏スーパークリエータ
- 京都大学機械研究会(2019年度NHK学生ロボコン優勝)

---

## 多項式乗算はおそすぎる!

- 多項式乗算はnaïveにやるとO(N²)のオーダ
    - 準同型暗号では多項式の演算はたくさん出てくる
        - これを速くすると全体が早くなる
    - 今日の話は多項式乗算を高速化した人々の成果の話

---

## オーダの限界はどこ?

- David Harvey(あとでもっかい出てくる)らが2019年に証明
    - (Integer multiplication in time O(n log n))[https://hal.science/hal-02070778/document]
    - ※多項式に基数を代入したら整数になるので多項式乗算と整数乗算はほぼ同じもの
- 現実的にはもうちょっと大きいオーダのものを使う
    - 