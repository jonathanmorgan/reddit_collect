import re

# regular expression to match 4-byte unicode characters.
re_test = re.compile( u'[\U00010000-\U0010ffff]' )

# create test string
test_string = u'Some example text with a sleepy face: \U0001f62a with two copies of the character \U0001f62a and stuff ( ' + unichr(1972) + u' and ' + unichr(40960) + u' ) at the end.'

# get iterator of all matches.
re_match_list = re_test.finditer( test_string )

# loop over and output information
match_count = 0
replace_string = test_string
for re_match in re_match_list:

    # output the match and the span.
    match_count += 1
    character_entity = re_match.group( 0 ).encode( 'ascii', 'xmlcharrefreplace' )
    span = re_match.span()
    start = span[ 0 ]
    end = span[ 1 ]
    print( str( match_count ) + " - " + character_entity + " - span: ( " + str( start ) + ", " + str( end ) + " )" )

    replace_string = replace_string[:start] + character_entity + replace_string[end:]
    
print( "replaced?: " + replace_string )

match_count = 0
replace_string = test_string
re_match = re_test.search( replace_string )
while ( ( re_match ) and ( re_match != None ) ):

    # output the match and the span.
    match_count += 1
    character_entity = re_match.group( 0 ).encode( 'ascii', 'xmlcharrefreplace' )
    span = re_match.span()
    start = span[ 0 ]
    end = span[ 1 ]
    print( str( match_count ) + " - " + character_entity + " - span: ( " + str( start ) + ", " + str( end ) + " )" )

    replace_string = replace_string[:start] + character_entity + replace_string[end:]

    re_match = re_test.search( replace_string )

print( "replaced?: " + replace_string )

from python_utilities.strings.string_helper import StringHelper

helper_replaced = StringHelper.entitize_4_byte_unicode( test_string )

print( "helper replaced?: " + helper_replaced )