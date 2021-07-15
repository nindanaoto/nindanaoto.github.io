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

# Secure Function Evaluation

松岡　航太郎

---

## このスライドで話すこと

- 暗号化したまま計算ができるような仕組み(秘密計算)は複数ある
- 準同型暗号、Garbled Circuit,　秘密分散あたりがよくある
- 厳密には復号しているがIntel SGXなどのTrusted Execution Environment(TEE)が産業用途では使われる
- ここではそれらをまとめて取り扱う理論的な枠組みについて簡単に話す

---

## Secure Function Evaluationとは

- よくSFEと略される、最もゆるい枠組み
- 評価したい関数と出力はパブリックで入力がプライベート
- 有名なのは[ミリオネア問題](https://en.wikipedia.org/wiki/Socialist_millionaire_problem)
- お互いの所持金を相手に教えずに誰が一番金持ちかを判定する
- 要は暗号化したまま数字を比較する

---

## Secure Computation Offloading

- 講師の論文で名前をつけたもの
- 関数も出力も入力もプライベートで、関数と入力は同じパーティが提供する
- クラウドコンピューティングのような計算処理をオフロードする状況を指す

---

## Private Function Evaluation

- PFEと略される
- 評価したい関数も入力もプライベートだが異なるパーティが提供する。出力は場合による
- サーバーで画像認識サービスを提供しているような状況がわかりやすいか
- 出力を関数提供者以外が知ると関数の情報が一部漏れるし逆も起きる

---

## 何が問題になるか

- そもそも暗号文のママ計算できる仕組みが必要
- 2-partyなら比較的簡単だが3-party以上の状況だと理論的にも難しい
- 準同型暗号の場合はMulti-Keyか秘密鍵を分散することで対応する
- 攻撃者のモデルの問題もある

---

## Honest-But-Curious

- HBCと略されることも
- プロトコルにはちゃんと従うがその過程で得た情報を使った攻撃はしてくる
- 現状の秘密計算はこの仮定を置くことが多い
- 現実の攻撃者はMalicious modelと言われる
- Maliciousでは不正な応答を行う場合がある
- 計算をオフロードしてるのにランダムな結果が返ってくるとか

---

## Verifiable Computation

- 直訳すれば検証可能計算？VCと略される
- 計算をオフロードしたときに頼んだ通りの計算をしたことを自分で関数を評価するよりも少ない計算量で検証できるような仕組み

---

## Federated Learning

- 秘密計算のキラーアプリと目されている
- データを隠したまま機械学習をする
- 医療データなど中央集権的に扱うことのできない学習データを扱う
- 2-partyではあまり意味がない
- 学習結果や残差に情報が残っていることなども問題

---

## 参考文献

- [TFHEのミリオネア問題チュートリアル](https://tfhe.github.io/tfhe/coding.html)
- [Modelling and Automatically Analysing PrivacyProperties for Honest-but-Curious Adversaries](https://www.cs.ox.ac.uk/people/andrew.paverd/casper/casper-privacy-report.pdf)
- [Pepper Project (Verifiable Computation)](https://www.pepper-project.org/)
- [Federated Learningの解説](https://blog.openmined.org/what-is-federated-learning/)/
