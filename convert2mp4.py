"""
convert2mp4.py

Wrapper for FFMPEG. Convert to MP4 video format.

Required argument(s) is a list of input files to convert (including wildcards).
Source video format is auto-detected by FFMPEG.
Output format is fixed to MP4.
Optional argument '--destination' allows setting the target directory.

This was mainly written to provide batch-conversion for OpenMV mjpeg
videos, avoiding the manual use of the OpenMV IDE video conversion tool
("Tools" -> "Video Tools" -> "Convert Video File"). FFPMEG is used with the
same arguments as when run through the OpenMV IDE.

Expects an 'FFMPEG_PATH' environment variable defined with the path to
the ffmpeg executable.

(C) 2024 Felix Althaus

"""




import os
import sys
import glob
import subprocess
import argparse




if __name__ == "__main__":

    print()

    # Path to FFMPEG executable is expected to be defined in an environment
    # variable (to avoid hard-coding it in the soruce code)
    try:
        ffmpeg_path = os.environ["FFMPEG_PATH"]
    except KeyError as error:
        print("ERROR: Environment variable {:s} not defined.".format(str(error)))
        sys.exit(-1)

    ffmpeg_binary = "ffmpeg.exe"


    parser = argparse.ArgumentParser()
    parser.add_argument("inputs")
    parser.add_argument("--destination")
    args = parser.parse_args()

    input_files = glob.glob(args.inputs)


    for input_file in input_files:

        # extract path and basename of source file
        path, name = os.path.split(os.path.abspath(input_file))
        root, ext = os.path.splitext(name)

        # assemble target output filename
        if args.destination is not None:
            output_file = os.path.join(args.destination, root + ".mp4")
        else:
            output_file = os.path.join(path, root + ".mp4")

        # Convert to MP4, with the same conversion arguments as OpenMV IDE
        # see https://ffmpeg.org/ffmpeg.html for the full FFMPEG documentation
        #
        arguments = ["-hide_banner",        # suppress printing banner
                     "-loglevel", "error",  # only show errors
                     "-nostats",            # do not print any statistics
                     "-y",                  # overwrite output file without asking
                     "-i", input_file,      # input file
                     "-q:v", "1",           # fixed video stream quality scale (as by OpenMV IDE)
                     output_file]           # output file

        print("", ffmpeg_binary, *arguments)
        result = subprocess.run([os.path.join(ffmpeg_path, ffmpeg_binary), *arguments],
                                check=False, capture_output=True, text=True)

        if result.returncode:
            print(" ERROR:", result.stderr)
        else:
            print(" OK")

        print()
