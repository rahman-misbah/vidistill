from typing import Optional, Union
from pathlib import Path

import yt_dlp

from vidistill.models import VideoMetadata

_ydl_fetch_metadata_opts = {
    "quiet": True,
    "no_warnings": True,
    "logger": None,
}

_ydl_download_video_opts = {
    "quiet": True,
    "no_warnings": True,
    "logger": None,
    "format": "bestvideo[ext=mp4],bestaudio[ext=m4a]/best[ext=mp4]/best",
}

_output_template = "%(id)s.%(ext)s"


def fetch_metadata(url: str) -> VideoMetadata:
    """Fetches video metadata from the given URL using yt-dlp.

    Args:
        url (str): The URL of the video to fetch metadata for.

    Returns:
        VideoMetadata: A VideoMetadata object containing the video metadata.

    Raises:
        yt_dlp.utils.DownloadError: If the video cannot be fetched.
    """
    with yt_dlp.YoutubeDL(_ydl_fetch_metadata_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return VideoMetadata(
            video_id=info["id"],
            title=info["title"],
            duration=info.get("duration"),
            channel=info.get("uploader"),
        )


def download(
    url: str, dest: Union[str, Path], metadata: Optional[VideoMetadata] = None
) -> tuple[Path, Path]:
    """Downloads a video and audio separately from the given URL to the specified destination directory.

    Args:
        url (str): The URL of the video to download.
        dest (Union[str, Path]): The destination directory where the video should be saved.
        metadata (Optional[VideoMetadata]): The metadata for the video to download.

    Returns:
        tuple[Path, Path]: A tuple containing the file paths of the downloaded video and audio.

    Raises:
        yt_dlp.utils.DownloadError: If the video cannot be fetched.
    """
    if metadata is None:
        metadata = fetch_metadata(url)

    dest_path = Path(dest)
    dest_path.mkdir(parents=True, exist_ok=True)

    output_path = dest_path / _output_template
    download_opts = dict(_ydl_download_video_opts, outtmpl=str(output_path))

    with yt_dlp.YoutubeDL(download_opts) as ydl:
        ydl.download([url])

    video_output = dest_path / f"{metadata.video_id}.mp4"
    audio_output = dest_path / f"{metadata.video_id}.m4a"

    return video_output, audio_output


# Test
if __name__ == "__main__":
    from vidistill.config import DATA_DIR

    url = "https://youtu.be/IXbFa2rQk3A?si=UIv7sJl9Rt_dVv3S"
    destination = DATA_DIR / "test_download"
    video_path, audio_path = download(url, destination, None)
    print(f"Video downloaded to: {video_path}")
    print(f"Audio downloaded to: {audio_path}")
