# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SteamDetectorPostPipeline:
    def process_item(self, item, spider):
        return item


import mysql.connector
class SaveSQLPipeLine:

    def __init__(self) -> None:
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'password',
            database = 'steamDB',
        )
        ##Create cursor, used to execute commands
        self.cur = self.conn.cursor()


        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS steam_discussion (
                steam_discussion_id int NOT NULL auto_increment,
                title_post text,
                profile VARCHAR(255),
                date_and_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(steam_discussion_id)
            )
        """)

    def insert_post(self, item, spider):
        query = """
            INSERT INTO steam_discussion (title_post, profile)
            VALUES (%s, %s)
        """
        values = (item["title"], item["profile"])

        self.cur.execute(query, values)
        self.conn.commit()

        return item

    def close_connection(self,spider):
        #Close cursor & connection database
        self.cur.close()
        self.conn.close()