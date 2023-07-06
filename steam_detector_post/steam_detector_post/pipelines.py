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
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            port=3307,  # Replace with the desired port number (e.g., 3307)
            user='root',
            password='password',
            database='steamDB'
        )
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS steam_discussion (
                steam_discussion_id int NOT NULL AUTO_INCREMENT,
                title_post text,
                profile VARCHAR(255),
                date_and_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(steam_discussion_id),
                UNIQUE KEY (title_post(255), profile(255))
            )
        """)

    def process_item(self, item, spider):
        if not self.item_exists(item):
            self.insert_post(item)
        return item

    def insert_post(self, item):
        query = """
            INSERT INTO steam_discussion (title_post, profile)
            VALUES (%s, %s)
        """
        values = (item["title"], item["profile"])
        self.cur.execute(query, values)
        self.conn.commit()

    def item_exists(self, item):
        query = """
            SELECT COUNT(*) FROM steam_discussion
            WHERE title_post = %s AND profile = %s
        """
        values = (item["title"], item["profile"])
        self.cur.execute(query, values)
        result = self.cur.fetchone()
        return result[0] > 0

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()