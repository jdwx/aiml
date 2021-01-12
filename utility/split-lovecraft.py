#!/usr/bin/env python3

import pdfplumber
import re
import unicodedata


def get_works( toc ):
    lines = toc.splitlines()
    for line in lines:
        line = line.strip()
        line = re.sub( r"\.\.+", " ", line )
        line = re.sub( r"\s+", " ", line )
        if "" == line:
            continue
        if "Table of Contents" == line:
            continue
        if re.match( r'^\.+$', line ):
            continue
        x = line.split()
        title = ' '.join( x[ 0 : -1 ] )
        if "Preface" == title:
            continue
        page_num = int( x[ -1 ] )
        works.append( ( title, page_num ) )


works = []

with pdfplumber.open( '../ext/The Complete Works of H.P. Lovecraft.pdf' ) as pdf:
    page = pdf.pages[ 2 ]
    text = page.extract_text()
    get_works( text )
    page = pdf.pages[ 3 ]
    text = page.extract_text()
    get_works( text )

    for i in range( len( works ) ):
        if i + 1 < len( works ):
            last = works[ i + 1 ][ 1 ] - 1
        else:
            last = len( pdf.pages )
        title = works[ i ][ 0 ]
        path = title.replace( ' ', '_' ) + '.txt'
        print( f"{title} (pages {works[i][1]} to {last}): {path}" )

        work = ""
        for j in range( works[ i ][ 1 ] - 1, last ):
            text = pdf.pages[ j ].extract_text()
            work += text + "\n"

        # Remove the title from the text of the story.
        if work[ 0 : len( title ) ] == title:
            work = work[ len( title ) : ].strip()

        # Remove the publication year from the text of the story.
        if re.match( r"^\(19[0-9][0-9]\)", work ):
            work = work[ 6 : ].strip()
        else:
            print( work[ 0 : 40 ] )

        # This PDF uses some very strange characters as quotes and apostrophes.
        work = work.replace( '’', "'" )
        work = work.replace( "‗", "'" )
        work = work.replace( "‘", "'" )
        work = work.replace( '―', '"' )
        work = work.replace( '‖', '"' )
        work = work.replace( '”', '"' )

        # Other general UTF-8 cleanup.
        work = work.replace( "—", "--" )
        work = work.replace( "–", "-" )
        work = work.replace( "•", " " )
        work = work.replace( "·", " ")

        """
        # Lovecraft's use of apostrophes for dialect is painful for the parser.  (Also racist AF.)
        work = work.replace( "in' ", "in_ " )
        work = work.replace( "in'.", "in_." )
        work = work.replace( "in',", "in_," )
        work = work.replace( "'em's ", "_em's " )
        work = work.replace( " 'phone", " phone" )
        dialect = [
            "cap'n", "'tis", "an'", "wa'n't", "o'", "excep'", "s'pose", "'em", "calc'late", "husban'", "her'n",
            "reg'lar", "'ud", "n'gai", "n'gha'ghaa", "y'hah", "mis'", "cha'ncey", "ol'", "wider'n", "graoun'",
            "col'", "nobody'd", "allow'd", "cou'd", "n'gah", "deny'd", "Hallowe'en", "o'clock", "p'inted",
            "bar'ls", "kep'", "t'other", "bigger'n", "sep'rit", "thflthkh'ngha", "y'bthnk", "h'ehye",
            "n'grkdl'lh", "e'yayayayaaaa", "ngh'aaaaa", "ngh'aaaa", "h'yuh", "year'"
        ]
        for d in dialect:
            du = d[ 0 ].upper() + d[ 1 : ] if d[ 0 ] != "'" else "'" + d[ 1 ].upper() + d[ 2 : ]
            for e in [ d, du ]:
                for pre in [ " ", "\"", "\n", "--" ]:
                    for post in [ " ", "\"", ".", ",", ";", "\n", "--", "!", "?" ]:
                        efrom = pre + e + post
                        eto = efrom.replace( "'", "_" )
                        work = work.replace( efrom, eto )
        """

        punct = "'\",.;?!-/():&*[]#_¡¿"
        for x in work:
            if unicodedata.category( x )[ 0 ] == 'P':
                if x not in punct:
                    print( x )

        # Remove the "Table of Contents" link from the end of the text.
        work = work.replace( "Return to Table of Contents", "" )

        # Clean up any remaining leading/trailing whitespace.
        work = work.strip()

        with open( "../corpus/lovecraft/input/" + path, 'w' ) as f:
            f.write( work )
