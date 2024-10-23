import os
from keggmapwizard.kegg_pathway_map import download_kegg_resources


def cli():
    import fire

    # keggmapwizard --map_ids "['00400', '00380']" --orgs "['gma', 'mus']"
    fire.Fire(download_kegg_resources)


if __name__ == '__main__':
    cli()
