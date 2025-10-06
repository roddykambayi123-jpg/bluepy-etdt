
# This demo intentionally does nothing harmful.
# It's just a placeholder to illustrate a parent -> child chain for screenshots.
import subprocess, sys, shutil

def main():
    # Try to spawn a harmless shell that simply echoes and exits.
    shell = "cmd.exe" if sys.platform.startswith("win") else (shutil.which("bash") or "sh")
    try:
        subprocess.run([shell, "/c" if shell.endswith("cmd.exe") else "-lc", "echo BluePy demo"], check=False)
        print("Spawned harmless shell for demo.")
    except Exception as e:
        print("Demo spawn failed:", e)

if __name__ == "__main__":
    main()
