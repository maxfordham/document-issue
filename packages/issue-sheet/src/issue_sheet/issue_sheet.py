from d_i_functions import load_datapackage


def main():
    (
        df_document,
        df_issue,
        df_document_issue,
        df_distribution,
        lookup,
        config,
        projectinfo,
    ) = load_datapackage()
