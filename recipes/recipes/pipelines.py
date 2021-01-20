# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

# After continers are made, lets send things to a storage location
# 1 Activate/Add inside settings
# 2 Every time and item is yeilded, it comes here

class RecipesPipeline:
    def __init__(self): # Called once or else the tables would be dropped and created every time
        '''
        Used to create connection, cursor, and tables
        '''
        self.conn = sqlite3.connect('recipes.db') # Creates connection to db
        self.cursor = self.conn.cursor() # Making sure cursor is created
        self.create_table()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS tbl_recipes""")
        self.cursor.execute("""
                        CREATE TABLE tbl_recipes(
                            title text ,
                            author text,
                            tags text,
                            image text,
                            recipe_notes,
                            url text
                        )
                    """)

    def store_db(self, item):
        self.cursor.execute("""INSERT INTO tbl_recipes VALUES (?, ?, ?, ?, ?, ?)""",
        (
            str(item['title']), # Type cast to string incase items is NoneType (None) with some images or tags
            str(item['author']), 
            str(item['tags']),
            str(item['image']),
            str(item['recipe_notes']),
            str(item['url'])       
        ))

        self.conn.commit()

    def process_item(self, item, spider): #Entrypoint for pipeline
        self.store_db(item)
        print('Writing to the DB!')
        return item
