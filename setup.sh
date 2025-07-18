# #!/bin/bash
# # setup.sh: 慶應かるた会Webアプリ用のディレクトリ構成を作成するスクリプト（親ディレクトリ: KarutaWeb）

# # プロジェクトのベースディレクトリを作成
# mkdir -p KarutaWeb/templates

# # プロジェクトディレクトリに移動
# cd KarutaWeb || { echo "ディレクトリ KarutaWeb に移動できませんでした"; exit 1; }

# # アプリケーション本体ファイルとDBファイルを作成（空ファイル）
# touch app.py SQLtest.db

# # テンプレートファイルを作成（空ファイル）
# touch templates/index.html templates/login.html templates/register.html templates/dashboard.html

# echo "プロジェクトのディレクトリ構成が作成されました！"

#!/bin/bash
# staticディレクトリの作成

mkdir -p KarutaWeb/static/css
mkdir -p KarutaWeb/static/js
mkdir -p KarutaWeb/static/images

# 空のCSSファイルを作成
touch KarutaWeb/static/css/style.css

echo "Static directories created under KarutaWeb/static/"
