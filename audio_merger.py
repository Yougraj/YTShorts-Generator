import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip


class VideoProcessor:
    def __init__(self, video_directory, audio_directory, output_directory):
        self.video_directory = video_directory
        self.audio_directory = audio_directory
        self.output_directory = output_directory

    def clear_terminal(self):
        os.system("cls" if os.name == "nt" else "clear")

    def find_random_audio_file(self):
        audio_files = [
            f for f in os.listdir(self.audio_directory) if f.endswith(".wav")
        ]
        if not audio_files:
            raise ValueError("No audio files found in the specified directory.")

        return os.path.join(self.audio_directory, random.choice(audio_files))

    def trim_audio_to_video_duration(self, audio_clip, video_clip):
        audio_duration = audio_clip.duration if hasattr(audio_clip, "duration") else 0
        video_duration = video_clip.duration

        if audio_duration > video_duration:
            return audio_clip.subclip(0, video_duration)
        else:
            return audio_clip

    def merge_video_with_random_audio(self):
        try:
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory)

            while True:
                video_files = [
                    f
                    for f in os.listdir(self.video_directory)
                    if f.endswith((".mp4", ".avi", ".mkv", ".mov"))
                ]

                print("Available videos:")
                for i, video_file in enumerate(video_files, start=1):
                    print(f"{i}. {video_file}")

                try:
                    video_choice = int(
                        input(
                            "Enter the number of the video file to use (or 0 to exit): "
                        )
                    )

                    if video_choice == 0:
                        print("Exiting...")
                        break

                    if 1 <= video_choice <= len(video_files):
                        chosen_video = video_files[video_choice - 1]
                        video_path = os.path.join(self.video_directory, chosen_video)

                        audio_path = self.find_random_audio_file()

                        audio_clip = AudioFileClip(audio_path)
                        video_clip = VideoFileClip(video_path)

                        audio_clip = self.trim_audio_to_video_duration(
                            audio_clip, video_clip
                        )

                        video_clip_with_audio = video_clip.set_audio(audio_clip)

                        output_path = os.path.join(
                            self.output_directory,
                            os.path.splitext(chosen_video)[0] + "_merged.mp4",
                        )
                        video_clip_with_audio.write_videofile(
                            output_path, codec="libx264", audio_codec="aac"
                        )

                        print(f"Video merged with audio and saved to: {output_path}")

                        os.remove(video_path)
                        print(f"Removed {chosen_video} from the video folder.")

                        self.clear_terminal()

                    else:
                        print("Invalid choice. Please enter a valid number.")

                except ValueError:
                    print("Invalid input. Please enter a valid number.")

        except Exception as e:
            print(f"Error merging video with audio: {e}")
