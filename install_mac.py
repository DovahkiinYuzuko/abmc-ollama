import os
import sys
import subprocess
import shutil

def run_command(command, description_jp, description_en):
    print(f"[Run] {description_jp} / {description_en}...")
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

def install():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    print("--- abmc-ollama Installer for macOS ---")

    # 1. 過去のビルド産物を完全に削除
    root_bin = os.path.join(base_dir, 'abmc-ollama')
    if os.path.exists(root_bin):
        os.remove(root_bin)

    for target in ["build", "dist"]:
        if os.path.exists(target):
            shutil.rmtree(target, ignore_errors=True)
    
    for spec in os.listdir("."):
        if spec.endswith(".spec"):
            os.remove(spec)

    # 2. 依存ライブラリ
    run_command("pip3 install -r requirements.txt", "依存ライブラリをインストール中", "Installing dependencies")

    # 3. ビルド
    build_cmd = (
        f'pyinstaller --onefile --name abmc-ollama '
        f'--icon="assets/icon.ico" '
        f'--add-data "src/logoAA.txt:." '
        f'src/main.py'
    )
    run_command(build_cmd, "ビルド中", "Building executable")

    # 4. 実行ファイルをルートへ移動
    dist_bin = os.path.join(base_dir, "dist", "abmc-ollama")
    if os.path.exists(dist_bin):
        print(f"[Move] Moving binary to project root...")
        shutil.move(dist_bin, root_bin)
        # 実行権限を付与
        os.chmod(root_bin, 0o755)

    # 5. エイリアス登録 (Macの標準シェルはzshなので.zshrcを優先)
    alias_line = f'\nalias abmc-ollama="{root_bin}"\n'
    zshrc = os.path.expanduser("~/.zshrc")
    
    if os.path.exists(zshrc):
        with open(zshrc, "r") as f:
            content = f.read()
        if 'alias abmc-ollama=' not in content:
            with open(zshrc, "a") as f:
                f.write(alias_line)
            print("[Info] Alias registered to .zshrc")

    # 6. 後片付け
    shutil.rmtree(os.path.join(base_dir, 'build'), ignore_errors=True)
    shutil.rmtree(os.path.join(base_dir, 'dist'), ignore_errors=True)

    print("\n" + "="*60)
    print("インストール完了 / Installation complete")
    print("新しい ターミナル を開いて、 / Open a new Terminal,")
    print("「abmc-ollama」と打ち込んでみてください。 / and try typing 'abmc-ollama'.")
    print("="*60)

if __name__ == "__main__":
    install()