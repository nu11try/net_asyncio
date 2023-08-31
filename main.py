import aiohttp
import asyncio
import requests
import sqlite3


async def fetch_character(session, character_id):
    url = f'https://swapi.dev/api/people/{character_id}/'
    async with session.get(url) as response:
        return await response.json()


async def load_character_data(session, conn, character_id):
    character_data = await fetch_character(session, character_id)
    if character_data.get('url'):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO characters (birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, skin_color, species, starships, vehicles)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            character_data['birth_year'],
            character_data['eye_color'],
            ','.join(character_data['films']),
            character_data['gender'],
            character_data['hair_color'],
            character_data['height'],
            character_data['homeworld'],
            character_data['mass'],
            character_data['name'],
            character_data['skin_color'],
            ','.join(character_data['species']),
            ','.join(character_data['starships']),
            ','.join(character_data['vehicles'])
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
