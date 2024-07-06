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

# LT about PQC

京都大学大学院情報学研究科情報学専攻通信情報システムコース 
佐藤 高史研究室 博士課程2年
2019年度未踏 OB

松岡　航太郎

---

## PQCとは?

- Post Quantum Cryptography の略
    - 耐量子計算機暗号
- 量子コンピュータは既存の暗号を高速に解ける可能性がある
    - 基本的にはShorのアルゴリズムに基づいた攻撃
    - RSA暗号や楕円曲線暗号などが解ける
- ※ AESの安全性はそれほど劣化しない
    - AESはブロック暗号の一種であり, 数学的な問題に基づいていない
    - Groverのアルゴリズムに基づいた全探索の高速化程度
        - bit数を倍にすればまぁ十分
-　共通鍵暗号でよいケースは大体AESが使われるので, 公開鍵暗号が必要なアプリケーションが危険
    - 鍵交換と

---

## NIST PQC Selected Algorithm 2022

- 去年の8月に3つのアルゴリズムが選定された