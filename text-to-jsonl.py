#!/usr/bin/env python3

import jsonlines
import sys


from lib.Config import config_from_tag
from lib.Parse import files_in_corpus, tokenized_sentences_from_file


config = config_from_tag( sys.argv[ 1 ] )

sent_count = 0
word_count = 0
file_count = 0

with jsonlines.open( config[ 'body_json' ], 'w' ) as wri:
    for filename in files_in_corpus( config[ 'corpus' ] ):
        file_count += 1
        doc = []
        for sent in tokenized_sentences_from_file( filename ):
            doc.append( sent )
            sent_count += 1
            word_count += len( sent )
        wri.write( doc )

print( f"Collected {file_count} files, {sent_count} sentences, and {word_count} words." )


