from random import choice
from shorturl import API_URL
from requests import get, post

SLUG_CHARACTERS = [chr(x) for x in range(ord('a'), ord('z') + 1)] + [chr(x) for x in range(ord('A'), ord('Z') + 1)] + [chr(x) for x in range(ord('0'), ord('9') + 1)] + ['-', '_']

def gen_slug():
    """ 
    Generates a random SLUG from the SLUG_CHARACTERS list.
    Checks whether the slug already in the database or not, if so generates a new one until a new is found.
    Every SLUG is 8 characters long.
    """

    while True:
        slug = "".join(choice(SLUG_CHARACTERS) for i in range(8))
        
        check_uniqueness = get(API_URL + 'storage?where={"slug":"' + slug + '"}')

        if not check_uniqueness.json()['_items']:
            return slug
    