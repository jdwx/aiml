

import glob
import re


from .Flatten import completely_flatten


from nltk.tokenize import sent_tokenize


def files_in_corpus( corpus ):
    for pattern in corpus:
        for path in glob.glob( pattern ):
            yield path


def format_for_fasttext( text ):
    out = ""
    for word in split_for_fasttext( text ):
        space = out != ""
        if space:
            out += " "
        out += word
    return out


def sentences_from_corpus( corpus ):
    for path in files_in_corpus( corpus ):
        # print( "Parsing", path )
        for sent in sentences_from_file( path ):
            yield sent


def sentences_from_file( path ):
    with open( path, 'r' ) as f:
        text = f.read()

    for sent in sent_tokenize( text ):
        sent.replace( "\n", "" )
        yield sent


def split_for_fasttext( text ):
    text = text.lower()
    trailers = ".\""
    if len( text ) > 1 and text[ -1 ] in trailers:
        out = split_for_fasttext( text[ 0 : -1 ] )
        out.append( text[ -1 ] )
        return out

    return _split_for_fasttext( text )


def _split_for_fasttext( text ):

    # print( "split =", text )

    as_is = [ "a.m.", "p.m.", "e.g.", "i.e.", "mr.", "mrs." ]
    if text in as_is:
        return [ text ]

    ignore = [ "", " ", "\n" ]
    if text in ignore:
        return []

    ws_split = [ " ", "\n", "\t" ]
    for sep in ws_split:
        subs = text.split( sep )
        out = []
        if 1 == len( subs ):
            continue
        for sub in subs:
            out.extend( _split_for_fasttext( sub ) )
        return out

    punc_split = [ "!", ",", ";", "\"", "--", "?", "(", ")", "-" ]
    for sep in punc_split:
        subs = text.split( sep )
        if 1 == len( subs ):
            continue
        out = []
        first = True
        for sub in subs:
            if first:
                first = False
            else:
                out.append( sep )
            out.extend( _split_for_fasttext( sub ) )

        return out

    if text[ -1 ] == ":":
        out = _split_for_fasttext( text[ 0 : -1 ] )
        out.append( text[ -1 ] )
        return out

    trailers = [ "'s", "'m", "'d", "'t" ]
    if len( text ) > 2 and text[ -2 : ] in trailers:
        out = _split_for_fasttext( text[ 0 : -2 ] )
        out.append( text[ -2 : ] )
        return out

    return [ text ]


def split_word_for_fasttext( word ):

    if 1 == len( word ):
        return [ word ]

    splits( )

    punc = ".,!?;"
    if word[ -1 ] in punc:
        out = split_word_for_fasttext( word[ 0 : -1 ] )
        out.append( word[ -1 ] )
        return out

    return [ word ]


def tokenized_sentences_from_file( file ):
    for sent in sentences_from_file( file ):
        yield split_for_fasttext( sent )


def tokens_from_file( file ):
    for sent in sentences_from_file( file ):
        yield from split_for_fasttext( sent )