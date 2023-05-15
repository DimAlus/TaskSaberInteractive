import toml, os

settings = {}
settings_file = ""
__dn = os.path.dirname(__file__).replace("\\", "/")

__setting_files = [__dn + "/settings.overload.toml", __dn + "/settings.toml"]
for fname in __setting_files:
    if os.path.exists(fname):
        try:
            with open(fname, "r") as f:
                settings = toml.load(f)
            settings_file = fname
            break
        except Exception as e:
            pass
