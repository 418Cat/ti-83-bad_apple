
# Bad Apple on TI 83 Premium CE 

A program compressing and decompressing the <a href="https://www.youtube.com/watch?v=9lNZ_Rnr7Jc">Bad Apple</a> video on the <a href="https://fr.wikipedia.org/wiki/TI-83_Premium_CE">TI 83 Premium CE</a>.
<br/>
<br/>
The compression algorithm isn't too fancy, it can store anywhere from 1 to 128 pixels per byte.
<br/>
*I might improve it using more advanced fft algorithm in the future if I remember to do so*
<br/>

---
## How to use ?
####Disclaimer : your calculator needs an OS version < 5.5, as this version and upwards <a href="https://tiplanet.org/forum/viewtopic.php?t=24216">blocks the possibility to run assembly code</a>. You can downgrade the OS version using <a href="https://yvantt.github.io/arTIfiCE/">arTIfiCE</a>.
<br/>
1 - First, download a <a href="https://www.youtube.com/watch?v=9lNZ_Rnr7Jc">bad apple apple video</a> using any youtube to mp4 website and place it in the `./py` directory. The file **needs** to be named "bad_apple.mp4".
<p style="text-align: center;"><i>If you want to try with any other video, make sure to modify the constants <a href="https://github.com/418Cat/ti-83-bad_apple/blob/main/py/convert.py#L13-L17C0">here</a> before running the program as they are hard-coded for bad apple.</i></p>
<br/>
<br/>
2 - Once the video is in the `./py` directory, run the python program. It will output `./src/bad_apple.h` containing the compressed video
<br/>
<br/>
<br/>
<br/>
3 - Compiling and sending to calculator :
<br/>
You'll need <a href="https://www.gnu.org/software/make/">Make</a> (<a href="https://gnuwin32.sourceforge.net/packages/make.htm">here for the windows version</a>) and the <a href="https://ce-programming.github.io/toolchain/static/getting-started.html">CE-dev compiler</a>.
<h5> - Using the run.sh script on Linux</h5>
With the calculator plugged in your computer, the last step is to run the `./run.sh` script. It will compile the program using the <a href="https://ce-programming.github.io/toolchain/static/getting-started.html">CE-dev compiler</a> and transfer it to the calculator using <a href="https://fr.wikipedia.org/wiki/TiLP">TiLP</a>.
<br/>
<h5> - Manually </h5>
To compile the project, first create the `./obj` and `./bin`, then directories  .
<br/>Using a terminal in the root directory, type `make`. The compiled files will be in `./bin`.
<br/>Once that's done, you can transfer them to your calculator using any software that allows you to do so (<a href="https://fr.wikipedia.org/wiki/TiLP">TiLP</a>, <a href="https://education.ti.com/en/products/computer-software/ti-connect-sw">Ti-Connect</a>).
<br/>
<br/>
<br/>
4 - Then, on your calculator, you can run the program. If you get a memory error, try modifying the constants <a href="https://github.com/418Cat/ti-83-bad_apple/blob/main/py/convert.py#L13-L17C0">here</a>, running the python program again, compiling the C program and transfering the files to the calculator. You might need to tweak those a few times.
<br/>
<br/>

---
### Controls :
#### Right arrow : next frame
#### Left arrow : previous frame
#### Up arrow : pause video
#### Enter key : stop program
<br/>
<br/>

---
Thank you to <a href="https://thepythoncode.com/author/abdou-rockikz">Abdeladim Fadheli</a> as a big part of the code in `./py/convert.py` comes from <a href="https://thepythoncode.com/article/extract-frames-from-videos-in-python">this python article to read video files</a>.
<br/>
<br/>

---
This code is distributed under <a href="https://www.gnu.org/licenses/quick-guide-gplv3.html">GPLv3 license</a>.