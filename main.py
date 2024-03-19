import os
from audio_merger import VideoProcessor
from video_downloader import VideoDownloader


def upload_to_youtube(upload_script_path):
    final_videos_folder = "finalVideo"
    uploaded_videos_folder = "uploadedVideos"

    if not os.path.exists(uploaded_videos_folder):
        os.makedirs(uploaded_videos_folder)

    final_video_files = [
        f
        for f in os.listdir(final_videos_folder)
        if f.endswith((".mp4", ".avi", ".mkv", ".mov"))
    ]

    print("Available videos for upload:")
    for i, video_file in enumerate(final_video_files, start=1):
        print(f"{i}. {video_file}")

    try:
        video_choice = int(
            input(
                "Enter the number of the video file to upload to YouTube (or 0 to exit): "
            )
        )

        if video_choice == 0:
            print("Exiting...")
            return

        if 1 <= video_choice <= len(final_video_files):
            chosen_video = final_video_files[video_choice - 1]
            video_path = os.path.join(final_videos_folder, chosen_video)

            title = os.path.splitext(chosen_video)[0]

            upload_command = f"python {upload_script_path} --file='{video_path}' --title='{title}' --description='' --keywords='cat, catsofinstagram, cats, catstagram, catlover, kitty, instacat, love, kitten, catlovers, catvideos, playingcat, cutecat, catoftheday, funnycatvideos, catmeme, world, catloversclub, kittycat' --category='22' --privacyStatus='public'"
            result = os.system(upload_command)

            if result == 0:
                uploaded_video_path = os.path.join(uploaded_videos_folder, chosen_video)
                os.rename(video_path, uploaded_video_path)
                print(f"Video moved to {uploaded_videos_folder}: {chosen_video}")
            else:
                print("Error during upload. Video not moved.")

        else:
            print("Invalid choice. Please enter a valid number.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")


def main():
    query = "cat"
    per_page = 10
    upload_script_path = "upload.py"

    print("Select an option:")
    print("1. Download videos")
    print("2. Merge videos with random audio")
    print("3. Upload video to YouTube")
    option = input("Enter the number of your choice (1, 2, or 3): ")

    if option == "1":
        downloader = VideoDownloader(query, per_page)
        downloader.download_videos()

    elif option == "2":
        video_directory = "videos"
        audio_directory = "audio"
        output_directory = "finalVideo"
        processor = VideoProcessor(video_directory, audio_directory, output_directory)
        processor.merge_video_with_random_audio()

    elif option == "3":
        upload_to_youtube(upload_script_path)

    else:
        print("Invalid option. Please enter either 1, 2, or 3.")


if __name__ == "__main__":
    main()
