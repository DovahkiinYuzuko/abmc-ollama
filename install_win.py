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
    # プロジェクトのルートディレクトリを取得
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    print("--- abmc-ollama Installer for Windows ---")

    # 1. 過去のビルド産物を完全に削除
    # ルートに移動させた古いexeも削除対象に入れるよ
    old_exe = os.path.join(base_dir, 'abmc-ollama.exe')
    if os.path.exists(old_exe):
        os.remove(old_exe)

    for target in ["build", "dist"]:
        if os.path.exists(target):
            shutil.rmtree(target, ignore_errors=True)
    
    for spec in os.listdir("."):
        if spec.endswith(".spec"):
            os.remove(spec)

    # 2. 依存ライブラリのインストール
    run_command("pip install -r requirements.txt", "依存ライブラリをインストール中", "Installing dependencies")

    # 3. ビルド実行
    build_cmd = (
        f'pyinstaller --onefile --name abmc-ollama '
        f'--icon="assets/icon.ico" '
        f'--add-data "src/logoAA.txt;." '
        f'src/main.py'
    )
    run_command(build_cmd, "ビルド中 (クリーンビルド実行)", "Building executable (Clean Build)")

    # 4. 実行ファイルをルートへ移動
    dist_exe = os.path.join(base_dir, 'dist', 'abmc-ollama.exe')
    if os.path.exists(dist_exe):
        print(f"[Move] Moving executable to project root...")
        shutil.move(dist_exe, old_exe)

    # 5. PATH 登録 (プロジェクトルートを登録するよ)
    # パス区切り文字の問題が出ないように配列判定ロジックを採用
   # 5. PATH 登録 (プロジェクトルートを登録し、即時反映の通知を送る) [cite: 14]
    ps_command = (
        f"$target = '{base_dir}'; "
        f"$oldPath = [System.Environment]::GetEnvironmentVariable('Path', 'User'); "
        f"if ($oldPath.Split(';') -notcontains $target) {{ "
        f"  [System.Environment]::SetEnvironmentVariable('Path', \"$oldPath;$target\", 'User'); "
        f"  $sig = '[DllImport(\"user32.dll\", SetLastError = true, CharSet = CharSet.Auto)] public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, string lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);'; "
        f"  $type = Add-Type -MemberDefinition $sig -Name 'Win32' -Namespace 'Utils' -PassThru; "
        f"  $res = [UIntPtr]::Zero; "
        f"  $type::SendMessageTimeout([IntPtr]0xffff, 0x001A, [UIntPtr]::Zero, 'Environment', 0x0002, 5000, [out]$res) | Out-Null; "
        f"}}"
    )

    # 6. 後片付け (distとbuildを消してスッキリさせる)
    shutil.rmtree(os.path.join(base_dir, 'build'), ignore_errors=True)
    shutil.rmtree(os.path.join(base_dir, 'dist'), ignore_errors=True)

    print("\n" + "="*60)
    print("インストール完了 / Installation complete")
    print("新しい PowerShell またはコマンドプロンプトを開いて、 / Open a new PowerShell or Command Prompt,")
    print("「abmc-ollama」と打ち込んでみてください。 / and try typing 'abmc-ollama'.")
    print("="*60)

if __name__ == "__main__":
    install()