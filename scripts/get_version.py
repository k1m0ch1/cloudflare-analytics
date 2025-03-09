import subprocess

def get_version():
    try:
        version = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).decode().strip()
    except subprocess.CalledProcessError:
        version = "0.1.0"
    return version

if __name__ == "__main__":
    print(get_version())

