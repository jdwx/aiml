

import json


def config_from_file( path ):
    with open( path ) as f:
        return json.load( f )


def config_from_tag( tag ):
    path = "config/" + tag + ".json"
    return config_from_file( path )
