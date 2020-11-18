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
  a {
    font-weight:bold;
    color:#F00;
  } 
-->

<!-- page_number: true -->

# TEE

松岡　航太郎

---

## TEEとは

- Truset Execution Environmetnの略
- ハードウェアの機能によって耐タンパ性を保証する仕組み
- 通常のプログラムからハードウェア的に隔離された実行環境を提供する
- ハードウェアに脆弱性が見つかることがたまによくある
- サイドチャネル攻撃に弱い
- 実行速度が通常とほぼ変わらないのが一番のメリット
- ここでは4種類紹介する
- 同じTEEと言っても想定する状況がそれぞれ違う

---

## IntelSGX

- Intelが提供するTEE
- 主に想定されている用途はDRM
- Remote Attestationと呼ばれる遠隔のマシン同士の認証システムがある
- 研究者の人々によって無理やり秘密計算に使われている
- DRM用なのでそこらへんのノーパソとかでも積んでいたりする
- 基本的なアイデアはチップ内でだけ復号するというもの
- メモリの上でも暗号化されている
- メモリは最大256MBブロックでユーザーが管理する必要がある
- OSを信用していないのとEnclave内のメモリが少ないため
- 特殊な命令を特殊なライブラリで呼び出すので直接書くのは非人道的
- この制限を回避するための研究レベルのフレームワークがいくつかある

---

## [GraphenSGX](https://github.com/oscarlab/graphene)

- その道では有名らしいフレームワーク
- シングルアプリ用の小さなOSをEnclaveの中で動かす
- これによってメモリアクセスやライブラリの不便をwrapする

---

## [BI-SGX](https://bi-sgx.net/)

- 講師の未踏同期が作っていたフレームワーク
- SGX単体ではEプログラムが情報を流出させないとは保証されない
- データが流出しない統計処理だけを許すようにインタプリタを挟む
- インタプリタがメモリ周りの面倒を見る

---

## AMD SEV

- 同じx86だが全く違うTEE
- こちらはKVMを使ってVMを動かすことを想定している
- 普通のOSつきのVMをまるごと保護する
- メモリは暗号化されるがマネジメントは勝手にしてくれる
- Remote Attestationもある
- 実は[GCPですでに使える](https://cloud.google.com/blog/products/identity-security/introducing-google-cloud-confidential-computing-with-confidential-vms)
- 想定用途から[サーバ用であるEPYCにしか載ってない](https://github.com/AMDESE/AMDSEV/issues/1)らしい

---

## ARM Trust Zone

- 組み込み向けを想定している
- メモリの暗号化はオプション
- 特定のハードウェアは通常のアプリからアクセスできないようにしたりできる
- 信頼できないアプリケーションから守るという感じ
- ファームウェアのダンプをさせないようにしたりもできる
- この上で動かす専用のOSがいくつかある

---

## [RISC-V KeyStone](https://keystone-enclave.org/)

- オープンソースのTEE
- 他のTEEはクローズドであることに安全性の根幹がある
- どちらかいというと組み込み向け
- メモリ暗号化はオプション
- TrustZoneが隔離実行環境を一つしか持たないのに対し複数持つことができる

---

## 何を信用するか

- TEEでは原則チップメーカーを信用することになる
- アメリカ企業ならNSAにバレてもおかしくない
- ファウンドリが台湾なら台湾にバレるかもしれない
- DRM用途なら国レベルの組織が欲しがるものではない
- 原発の制御用途や政府の基幹サーバだと......?
- Keystoneなら理論上はすべて自前で作れば信用できるか？
- 実用的秘密計算としては情報の提供者さえ納得させられれば十分ではある
- 準同型暗号とは攻撃モデルが異なる

---

## 参考資料

- [TEEの解説論文](https://www.jstage.jst.go.jp/article/essfr/14/2/14_107/_pdf/-char/ja)
- [某氏のQiita](https://qiita.com/Cliffford/items/2f155f40a1c3eec288cf)
- [Intel SGXの解説論文](https://eprint.iacr.org/2016/086.pdf)
- [SGXのawesome list](https://github.com/Liaojinghui/awesome-sgx)
- [SGX,TrustZone,Keystoneの比較ポスター](https://www.slideshare.net/suzaki/3teeintel-sgx-arm-trustzone-riscv-keystone)