

import jsonlines


class Index:

    def __init__( self, path = None ):
        if path is None:
            self.key_to_word = [ "__NO_WORD__" ]
            self.word_to_key = { "__NO_WORD__": 0 }
            self.next_key = 1
        else:
            self.load( path )

    def __len__( self ):
        return self.next_key

    def add( self, word ):
        self.word_to_key[ word ] = self.next_key
        self.key_to_word.append( word )
        self.next_key += 1

    def add_once( self, word ):
        if not self.has_word( word ):
            self.add( word )

    def has_key( self, key ):
        return key < self.next_key

    def has_word( self, word ):
        return word in self.word_to_key

    def keys_to_words( self, keys ):
        if isinstance( keys, int ):
            return self.key_to_word[ keys ]
        words = []
        for key in keys:
            words.append( self.keys_to_words( key ) )
        return words

    def load( self, path ):
        with jsonlines.open( path ) as rdr:
            self.next_key = rdr.read()
            self.word_to_key = rdr.read()
            self.key_to_word = rdr.read()

    def save( self, path ):
        with jsonlines.open( path, 'w' ) as wri:
            wri.write( self.next_key )
            wri.write( self.word_to_key )
            wri.write( self.key_to_word )

    def words_to_keys( self, words ):
        if isinstance( words, str ):
            return self.word_to_key[ words ]
        keys = []
        for word in words:
            keys.append( self.words_to_keys( word ) )
        return keys
