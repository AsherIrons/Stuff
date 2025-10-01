import subprocess

def getUsers():
    cmd = ["net", "users", "/domain"]
    output = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    users = []
    capture = False
    for line in output.splitlines():
        if "----" in line:
            capture = not capture
            continue
        if capture:
            users.extend(line.split())
    return users


def userEnabled(username):
    cmd = ["net", "user", username, "/domain"]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
        for line in out.splitlines():
            if "Account active" in line:
                return "Yes" in line
    except subprocess.CalledProcessError:
        return False
    return False


if __name__ == "__main__":
    print("=== Domain User Status ===")
    for user in getUsers():
        status = "ENABLED" if userEnabled(user) else "DISABLED"
        print(f"{user:<20} {status}")
