

import collections


def completely_flatten( in_list ):

    if isinstance( in_list, ( str, bytes ) ) or not isinstance( in_list, collections.Sequence ):
        return in_list

    out_list = []
    for item in in_list:
        if isinstance( item, ( str, bytes ) ) or not isinstance( item, collections.Sequence ):
            out_list.append( item )
        else:
            out_list.extend( completely_flatten( item ) )
    return out_list


def flatten_list( what, max_depth ):

    if isinstance( what, ( str, bytes ) ) or not isinstance( what, collections.Sequence ):
        return what

    if 0 == max_depth:
        return completely_flatten( what )

    if 1 == max_depth:
        return [ completely_flatten( item ) for item in what ]

    max_depth -= 1
    return [ flatten_list( item, max_depth ) for item in what ]
