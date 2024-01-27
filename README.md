# Generate summary of any video

Generate a clean Markdown document of any video 📺 anywhere and anytime
Markdownification works through its subtitles, sumerization locating the important bits.

You can [![Run on Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/opencoca/vidsum/blob/master/Video_to_Markdown.ipynb) or setup localy...

## Installing vidsum

In order to install vidsum, simply clone the repository to a local directory. You can do this by running the following commands:

```sh
git clone https://github.com/OpenGenus/vidsum.git
cd vidsum/code
```

Please note that vidsum requires the following packages to be installed:

- [pysrt](https://github.com/byroot/pysrt)
- [imageio](https://imageio.github.io/)
- [moviepy](https://zulko.github.io/moviepy/)
- [pytube](https://github.com/nficano/pytube)
- [sumy](https://github.com/miso-belica/sumy)

Prerequisites:

-   Install Required Packages:

    Before starting, ensure you have the necessary packages installed. Run the following command in your terminal:

    ```

    pip install -r requirements.txt

    ```

Usage:

Generating a Summary from a Local Video File and Subtitle:

1.  Specify video and subtitle files:

    ```

    python sum.py -i <video_file_path> -s <subtitle_file_path>

    ```

    -   Replace `<video_file_path>` with the actual path to your video file (e.g., `sample.mp4`).
    -   Replace `<subtitle_file_path>` with the path to the corresponding subtitle file (e.g., `subtitle.srt`).
    

Summarizing a YouTube Video:
============================

1.  Provide the video URL:

    ```

    python sum.py -u <youtube_video_url>

    ```

    -   Replace `<youtube_video_url>` with the actual URL of the YouTube video you want to summarize.

Optional: Retaining Downloaded YouTube Video and Subtitles:

-   To keep the downloaded video and subtitles after summarization, add the `-k` flag:

    ```

    python sum.py -u <youtube_video_url> -k

    ```

**Key Points:**

-   The `sum.py` script handles both local video files and YouTube videos.
-   For YouTube videos, it automatically downloads the video and subtitles (if available).
-   The `-k` flag is optional and only used to preserve downloaded YouTube content.

**Additional Notes:**

-   Ensure you have a stable internet connection for summarizing YouTube videos.
-   The quality of the summary depends on the quality of the input video and subtitles.
-   Consider exploring additional options or parameters offered by the `sum.py` script for further customization.

Future Developments
===================

For more information on future developments to this approach, please see the [Wiki](https://github.com/opencoca/vidsum/wiki/Future_developments) page. You can also check out other [approaches](https://github.com/OpenGenus/vidsum/wiki/Other-approaches) that have been implemented.

Contributions
=============

All contributions are welcome! If you would like to make a pull request to this repository, please review the [COMMIT_TEMPLATE.md](https://github.com/opencoca/vidsum/blob/master/.github/COMMIT_TEMPLATE.md) file before doing so. This will help ensure that your contribution meets the project's guidelines and can be easily reviewed and merged.

You can see a list of all contributors to this project [here](https://github.com/opencoca/vidsum/graphs/contributors). Thank you for considering contributing to vidsum! We appreciate your help in making this project the best it can be.
