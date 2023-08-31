import aiosqlite


async def create_table():
    async with aiosqlite.connect("contacts.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                birth_year TEXT,
                eye_color TEXT,
                films TEXT,
                gender TEXT,
                hair_color TEXT,
                height TEXT,
                homeworld TEXT,
                mass TEXT,
                name TEXT,
                skin_color TEXT,
                species TEXT,
                starships TEXT,
                vehicles TEXT
            )
        ''')
        await db.commit()


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_table())
