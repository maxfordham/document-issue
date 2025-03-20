from mfdb import get_project_roles

if __name__ == "__main__":
    import pathlib
    project_roles = [list(x.model_dump().values()) for x in get_project_roles().root]
    fpth = pathlib.Path(__file__).parent.parent / "src" / "bep" / "data" / "project_roles.csv"

    with open(fpth, "w") as f:
        f.write("role_name,role_title,role_category\n")
        for role in project_roles:
            f.write(f"{role[0]},{role[1]},{role[2]}\n")
    print("done")