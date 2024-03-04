import os
import requests
from tqdm import tqdm
import configparser
import sqlite3


class VideoDownloader:
    def __init__(self, query, per_page=10, orientation="portrait"):
        self.url = "https://api.pexels.com/videos/search"
        self.query_params = {
            "query": query,
            "per_page": per_page,
            "orientation": orientation,
        }
        self.headers = self._load_api_key()
        self.total_videos = per_page
        self.video_folder = "videos"
        self.db_file = "video_ids.db"

    def _load_api_key(self):
        config = configparser.ConfigParser()
        config.read("config.conf")

        try:
            api_key = config.get("API", "api_key")
            return {"Authorization": api_key}
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            raise ValueError(f"Error loading API key from config.conf: {e}")

    def _create_video_folder(self):
        if not os.path.exists(self.video_folder):
            os.makedirs(self.video_folder)

    def _create_db_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS video_ids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL UNIQUE
            )
        """
        )

        conn.commit()
        conn.close()

    def _load_stored_video_ids(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute("SELECT video_id FROM video_ids")
        stored_video_ids = set(row[0] for row in cursor.fetchall())

        conn.close()
        return stored_video_ids

    def _save_video_id(self, video_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO video_ids (video_id) VALUES (?)", (video_id,))
        conn.commit()

        conn.close()
        print(f"Stored Video ID: {video_id}")

    def download_videos(self):
        try:
            self._create_video_folder()

            self._create_db_table()

            response = requests.get(
                self.url, params=self.query_params, headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                videos = data.get("videos", [])[: self.total_videos]

                stored_video_ids = self._load_stored_video_ids()

                for idx, item in enumerate(videos):
                    video_id = item.get("id", "")
                    video_name = item.get("url", "").split("/")[-2]

                    if video_id in stored_video_ids:
                        print(f"Video ID {video_id} already downloaded. Skipping.")
                        continue

                    new_url = f"https://www.pexels.com/download/video/{video_id}"

                    video_filename = os.path.join(
                        self.video_folder, f"{video_name}.mp4"
                    )

                    try:
                        with tqdm(
                            desc=f"Downloading",
                            unit="B",
                            unit_scale=True,
                            dynamic_ncols=True,
                        ) as progress_bar:
                            video_response = requests.get(
                                new_url, headers=self.headers, stream=True
                            )

                            with open(video_filename, "wb") as video_file:
                                for data in video_response.iter_content(
                                    chunk_size=1024
                                ):
                                    video_file.write(data)
                                    progress_bar.update(len(data))

                        self._save_video_id(video_id)

                        print(f"Downloaded: {video_filename} (Video ID: {video_id})")

                    except Exception as e:
                        print(f"Error downloading {new_url}: {e}")

            else:
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Error downloading videos: {e}")
