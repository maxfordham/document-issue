import pathlib
import os
import sys
import json
import re
import yaml


def get_stem(path: pathlib.Path):
    return path.name.replace("".join(path.suffixes), "")


def get_ext(fpth):
    """get file extension including compound json files"""
    return "".join(pathlib.Path(fpth).suffixes)


def read_json(fpth, encoding="utf8"):
    """
    read info in a .json file
    """

    def read(fpth):
        with open(fpth, "r", encoding=encoding) as f:
            json_file = json.load(f)
        return json_file

    json_file = read(fpth)
    json_file = json.loads(json_file)
    return json_file


def fpth_chg_extension(fpth, new_ext="docx"):
    return os.path.splitext(fpth)[0] + "." + new_ext


def get_home():
    """generate the home dir.

    Returns:
        fdir [str]: if windows: os.environ['userprofile'], if linux: os.environ['home']
    """
    if sys.platform == "linux":
        return os.environ["HOME"]
    elif sys.platform == "windows":
        return os.environ["userprofile"]
    else:
        return None


# directories -------------------------------------------------
def flatten_list(list_of_lists: list) -> list:
    """Flatten a list of (lists of (lists of strings)) for any level
    of nesting

    Args:
        list_of_lists: with mix of lists and other
    Returns:
        rt: list with no nested lists

    """
    rt = []
    for i in list_of_lists:
        if isinstance(i, list):
            rt.extend(flatten_list(i))
        else:
            rt.append(i)
    return rt


def jobno_fromdir(fdir):
    """
    returns the job number from a given file directory

    Args:
        fdir (filepath): file-directory
    Returns:
        job associated to file-directory
    Code:
        re.findall("[J][0-9][0-9][0-9][0-9]", txt)
    """
    matches = re.findall("[J][0-9][0-9][0-9][0-9]", fdir)
    if len(matches) == 0:
        job_no = "J5001"
    else:
        job_no = matches[0]
    return job_no


def find_fdir_keys(di):
    """searches dict for key that contains string 'fdir'. ignores J:\\
    can handle lists for fdir* values"""
    li = list(di.keys())
    li = flatten_list([di[l] for l in li if l[0:4] == "fdir"])
    li = [l for l in li if l != "J:\\"]
    li = [l for l in li if l != "None"]
    return li


def make_disclaimer_spacer(fdir):
    try:
        from PIL import Image

        width = 130
        height = 5

        img = Image.new(mode="RGB", size=(width, height), color="white")
        path = fdir / "disclaimer_spacer.png"
        img.save(path)
        return path
    except:
        return None


# ------------------------------
def str_presenter(dumper, data):
    """configures yaml for dumping multiline strings
    Ref: https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data
    """
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)
# ------------------------------
# ^ to use with safe_dum
# ^ configures yaml for pretty dumping of multiline strings


def preview_dict_as_yaml(di: dict, **kwargs):
    from IPython.display import Markdown

    s = yaml.dump(di, indent=2, **kwargs)
    return Markdown("\n```yaml\n" + s + "\n```")
