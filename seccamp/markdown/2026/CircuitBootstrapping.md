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

# Circuit Bootstrapping

松岡 航太郎

---

## Circuit Bootstrappingとは

- TLWE(lvl0)からTRGSWへ変換する操作
- BlindRotateとTRLWEからTRLWEへのSwitchingで作られる
    - 構成としては詳細を見ると4パターンある
        - BlindRotateにmanyLUTを使うか否か
        - Public/PrivateKeySwitchingを使うかAutomorphismを使うか
- 一般にGateBootstrappingより重いがCMUXが高速なので使いみちがある
    - もちろん小さい関数だとGateBootstrappingのほうが早い
    - 多入力多出力とみなせる場合が一番わかり易い

---

## BlindRotateによる処理

- BlindRotateでは雑に言うと定数除算を計算する
    - TRGSWでは平文は$Bg$の冪で割る必要がある
- 平文がバイナリならTestVectorはすべて1を$Bg$の冪と$2$で割ったもの
    - 0の時$-\frac{1}{2Bg^i}$みたいなのが出る
    - 1の時$\frac{1}{2Bg^i}$
    - $-\frac{1}{2Bg^i}$を足せば所望の値になる
- もちろん平文がバイナリ以外でも同様の操作は構成可能
- これで作れるのはTLWEなのでこれだけではだめ

---

## PublicKeySwitching

- IKSの時はTLWEからTLWEの写像としてKeySwitchingを書いた
  - 実際にはT(R)LWEからT(R)LWEへの写像としてかける
- Identity以外の場合にはT(R)LWEの各要素に所望の関数を適用する
  - Publicな要素にPublicな関数を適用する
  - 適用してからSwitching

---

## PrivateKeySwitching 

- 関数がPrivateな場合

---

## ManyLUTによる高速化

- 行ごとにやらずにまとめてやる

---

## Automorphism

---

## Annihilation

---

## ExternalProductによる秘密鍵との乗算

---