Swiss System Match Generator
====
## Description
スイスドロー用の対戦組み合わせ作成ツールです．雑に作ったので汚いし無駄が多いです．  
pushすると、https://[user_name].github.io/Swiss-Match-Generator/index.html に現在のcsvの情報がアップされます．

## Demo
https://k-seta.github.io/Swiss-Match-Generator/index.html
## Requirement
- Python 2.7.12
- Virtualenv 15.1.0

## Usage
`$ python swiss-system.py [対戦組み合わせ用のcsvファイル]`  
初期状態では，csvファイルは，
```
Name
p1
p2
p3
...
```
という形で作っておく．

## Install
1. `$ git clone https://github.com/k-seta/Swiss-Match-Generator.git`でcloneしてくる
2. `$ virtualenv venv`でVirtualenvの仮想環境作成する．
3. `$ source venv/bin/activate`でVirtualenvの仮想環境に入る．
4. `$ pip install -r requirements.txt`で仮想環境に必要なPythonモジュールをインストールする．