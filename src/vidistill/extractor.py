import subprocess
from typing import Union, Optional
from pathlib import Path


def extract_frames(
    video_path: Union[Path, str],
    destination_dir: Union[Path, str],
    frame_per_second: Optional[str] = None,
    start_time: Optional[str] = None,
    duration: Optional[str] = None,
    end_time: Optional[str] = None,
    end_trim: Optional[str] = None,
    output_padding: Optional[int] = 4,
    output_format: Optional[str] = "jpg",
) -> None:
    """
    Extract frames from a video file and save them as images in the destination directory.

    Args:
        video_path (Union[Path, str]): The path to the video file.
        destination_dir (Union[Path, str]): The directory where the extracted frames will be saved.

    Returns:
        None

    Raises:
        subprocess.CalledProcessError: If the ffmpeg command fails.
    """
    video_path = Path(video_path)
    destination_dir = Path(destination_dir)
    output_template = destination_dir / f"frame_%0{output_padding}d.{output_format}"

    # 1. Start with global/input configurations
    ffmpeg_command = ["ffmpeg"]

    # 2. Add input-seeking parameters (Must come BEFORE -i)
    if end_trim is not None:
        # Fetch duration and compute: Start -> (Total Duration - Trim Offset)
        total_duration = _get_video_duration(video_path)
        calculated_end = max(0.0, total_duration - float(end_trim))
        ffmpeg_command.extend(["-to", str(calculated_end)])
    elif start_time is not None:
        # Fast seeking (placed before input)
        ffmpeg_command.extend(["-ss", start_time])

    # 3. Add the input file target
    ffmpeg_command.extend(["-i", str(video_path)])

    # 4. Add output/processing parameters (Must come AFTER -i)
    if frame_per_second is not None:
        ffmpeg_command.extend(["-vf", f"fps={frame_per_second}"])

    # Handle mutually exclusive timing parameters safely
    if duration is not None:
        ffmpeg_command.extend(["-t", duration])
    elif end_time is not None:
        ffmpeg_command.extend(["-to", end_time])

    # 5. Add the output destination
    ffmpeg_command.append(str(output_template))

    # Ensure the destination directory exists
    destination_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)


def _get_video_duration(video_path: Path) -> float:
    """Helper function to fetch exact video duration in seconds via ffprobe."""
    ffprobe_command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    result = subprocess.run(ffprobe_command, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())
