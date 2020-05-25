AUDIOMETER

Requirements:

* Python 3.8 or something similar
* FFmpeg, a recent and comprehensive build

Platform:

This is tested on Windows 10 only but also works on my ancient Linux Chromebook at lower frame rates. If you find it works elsewhere, great!

About:

Using the mpv player powered by the FFmpeg libraries (see elsewhere in my respositories or in the Internet), Audiometer.py
creates an on-screen set of meters to show you much information about a stereo audio signal.

This program works not only on files, but also on Internet streams: anything that the mpv player (and, therefore, FFmpeg) can read.

Make sure your Fontconfig cache is up to date: run fc-cache at some point (and, on Windows, this must be as Administrator).

The volume meter is calibrated to PPM = -18dBfS.

There are options:
  -f <int> gives int fps output frames
  -j directs audio output to the Jack audio daemon
  -l <float> attenuates the incoming signal by the given value in dB

Recent improvements include ensuring the output audio is a reproduction of the input without any change in sample-rate, and oversampling the 'volume' indicator at 192kHz to ensure it reads true peaks.

The graticule in the frequency meter now represents 5kHz increments from 0 to 25kHz, no matter what incoming sampling rate is used.

This software is GPLv3 open sourced. Please copy and amend and use anywhere provided that you share the source code and the source code of any modifications you make.
