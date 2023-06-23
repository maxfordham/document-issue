import pathlib
import tomllib

def flatten(l):
    return [item for sublist in l for item in sublist]

def getreqs(path):
    return tomllib.loads(path.read_text())['project']['dependencies']
    


fdir_packages = pathlib.Path("../packages")
li_packages = list(fdir_packages.glob("*"))
fpths_pyproject = [l / "pyproject.toml" for l in li_packages]
reqs = list(set(flatten([getreqs(p) for p in fpths_pyproject])))

p = pathlib.Path("requirements-dev.txt")
p.write_text("\n".join(reqs))

    