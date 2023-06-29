def validateArtistName(artist_name):
    if not artist_name:
        raise ValueError("Artist name cannot be an empty string")

    if '\0' in artist_name:
        raise ValueError("Artist name cannot contain null characters")

    if artist_name.startswith('system.'):
        raise ValueError("Artist name cannot start with 'system.' prefix")

    if not artist_name[0].isalpha() and not artist_name[0] == '_':
        raise ValueError("Artist name should start with an underscore or a letter character")

    # replacing $ with dollarSign
    artist_name = artist_name.replace('$', 'dollarSign')

    #Removes leading or trailing "." s  
    artist_name = artist_name.strip('.')


    return artist_name

#Checks if the artist is one that we 
#returns bool 
def isRapArtist(artist_name,spotify):
    # Search for the artist
    result = spotify.search(q='artist:' + artist_name, type='artist')

    try:
        # Get the first artist matching the search
        artist = result['artists']['items'][0]
        
        # Check if "hip hop" or "rap" is in the artist's genres
        return any(genre in artist['genres'] for genre in ['hip hop', 'rap'])

    except IndexError:
        print(f"No artist named {artist_name} found.")
        return None

# testing the function with a valid artist name
print(validateArtistName("T.I."))

