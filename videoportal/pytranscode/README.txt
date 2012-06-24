PyTranscode Readme
==================

Copyright (C) 2009  Martin P. Buhr (http://lonelycode.com / twitter: @lonelycode)

PyTranscode is a set of scripts to make handling ffmpeg easier in python,
it enables video information extraction, transcoding, presets, splash image
extraction (multiple) and state reporting (percentage complete)

Contents:
=========

1. What is this?
2. Hopeful Roadmap
3. How to use the scripts
4. License


1. What is this?
================

A while back I wrote a proof-of-concept webapp that basically replicated what
Brightcove and other online video management tools did, and at its heart was a
tool to control FFMPEG - one of the best command-line transcoders out there.

Now the webapp never took off (it was never launched, pending a rewrite), but
I had started on rewriting the engine that would control the transcoder software.

I've since moved my limited attention span to other, shineir things, but thought
I would release this piece of rather nifty and handy code to the public to help
others who want to do something with video and don;t want to fork out a fortune.

2. Hopeful Roadmap
==================

PyTranscode is hopefully going to be part of something bigger - the vision is to
produce a set of django applications which can do the following:

- A storage engine for local or cloud-based storage
- A queue manager for scaling, this again would have vairous back-ends for local
  queue management or something like Amazon Queue Service
- A transcode server that can be run on multpile machines and be managed via an
  API OR be run in a mode to interact with the queue service
- An API wrapper to control the transcode-server for common tasks

3. How to use the scripts
=========================

There are five files with PyTranscode, these have the following basic functionsality:

- ffmpeg.py:    Can be used to build a command line to run ffmpeg for various
                settings with input/output

- presets.py:   Some presets to use with ffmpeg if you can;t be bothered to
                write out the long dictionaries some transcodes require
                
- runner.py:    Runner basically allows you to run ffmpeg in a managed way and
                trap the output as well as the percentage complete

- splash.py:    This will let you pull thumbnails at equal intervals from the
                inpout file and return the filenames
                
- video_info:   Need to know everything about a video file? This basically parses
                the -i output from ffmpeg to get all the details and present
                them as a class

Depending on what you need, the documentation on how to use each one is in the
header of the file.

If you want to see a test run, there's the file test.py which should show an easy
way to get started with these classes.

4. License
==========

Copyright (C) 2009  Martin P. Buhr (http://lonelycode.com / twitter: @lonelycode)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

IF YOU USE THIS SOFTWARE DO US A FAVOR AND LET ME KNOW :-)


