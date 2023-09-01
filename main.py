import asyncio
import sqlite3
import aiohttp
import requests

from aiohttp import ContentTypeError


async def fetch_any(session, url, field=None):
    async with session.get(url) as response:
        try:
            res = await response.json()
            return res if field is None else res[field]
        except ContentTypeError:
            return None

async def load_character_data(session, conn, character_id):
    character_data = await fetch_any(session, f'https://swapi.dev/api/people/{character_id}/')

    if character_data is not None:
        if character_data.get('url'):
            films = [await fetch_any(session, el, 'title') for el in character_data['films']]
            species = [await fetch_any(session, el, 'name') for el in character_data['species']]
            starships = [await fetch_any(session, el, 'name') for el in character_data['starships']]
            vehicles = [await fetch_any(session, el, 'name') for el in character_data['vehicles']]
            homeworld = await fetch_any(session, character_data['homeworld'], 'name')

            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO characters (birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, skin_color, species, starships, vehicles)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                character_data['birth_year'],
                character_data['eye_color'],
                ', '.join(films),
                character_data['gender'],
                character_data['hair_color'],
                character_data['height'],
                homeworld,
                character_data['mass'],
                character_data['name'],
                character_data['skin_color'],
                ', '.join(species),
                ', '.join(starships),
                ', '.join(vehicles)
            ))
            conn.commit()


async def main():
    conn = sqlite3.connect('contacts.db')

    res = requests.get(url='https://swapi.dev/api/people/', verify=False)
    count = res.json()['count']

    async with aiohttp.ClientSession() as session:
        tasks = [load_character_data(session, conn, character_id) for character_id in range(1, count)]
        await asyncio.gather(*tasks)

    conn.close()


if __name__ == '__main__':
    asyncio.run(main())
