"""
THIS CODE MAINLY COMES FROM https://thepythoncode.com/article/extract-frames-from-videos-in-python
AND WAS MODIFIED TO SUIT MY NEEDS.
A big thank you to Abdeladim Fadheli from thepythoncode.com for writing this code.
"""

from datetime import timedelta
import cv2
import numpy as np
import os

# i.e if video of duration 30 seconds, saves 10 frame per second = 300 frames saved in total
SAVING_FRAMES_PER_SECOND = 4
RATIO = 4/3
RES_HEIGHT = 40
RES_WIDTH = int(RES_HEIGHT * RATIO)
VIDEO_FILE = "bad_apple.mp4"
"""
# If you get a memory error on the calculator, try lowering those
"""


def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")

def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def endFile(f, frame_count, frame_lengths):
    f.writelines("};\n")
    f.writelines("\n\n#define BADAPPLE_FRAMES " + str(frame_count))
    f.writelines("\n\nint frameLengths[BADAPPLE_FRAMES]={\n")
    
    for frame in frame_lengths:
        f.writelines(str(frame) + ",")
    f.writelines("};")

    f.writelines("\n\n#define BADAPPLE_BYTESIZE " + str(sum(frame_lengths)))
    
    f.writelines("\n\n#endif")

def main(VIDEO_FILE):    
    filename, _ = os.path.splitext(VIDEO_FILE)
    filename = "../src/" +  filename + ".h"
    
    if os.path.exists(filename):
        os.remove(filename)
    
    with open(filename, 'a') as f:
        
        # The length in unsigned char
        # for each frame added, so
        # when iterating over the whole array
        # the c program knows the length of
        # current frame
        frame_lengths = []
        
        f.writelines("#ifndef __BADAPPLE_H__\n")
        f.writelines("#define __BADAPPLE_H__\n")
        f.writelines("#define BADAPPLE_WIDTH " + str(RES_WIDTH) + "\n")
        f.writelines("#define BADAPPLE_HEIGHT " + str(RES_HEIGHT) + "\n")
        f.writelines("#define BADAPPLE_FPS " + str(SAVING_FRAMES_PER_SECOND) + "\n")
        #f.writelines("const unsigned char badApple[][" + str(RES_WIDTH * RES_HEIGHT) + "] = {\n")
        f.writelines("const unsigned char badApple[] = {\n")
        
        # read the video file    
        cap = cv2.VideoCapture(VIDEO_FILE)
        # get the FPS of the video
        fps = cap.get(cv2.CAP_PROP_FPS)
        # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
        saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
        # get the list of duration spots to save
        saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
        
        # start the loop
        count = 0
        
        frames_added = 0
        
        while True:
            is_read, frame = cap.read()
            
            frame_duration = count / fps
            
            #if frames_added >= 100:
                #endFile(f, frames_added, frame_lengths)
                #break
            
            try:
                # get the earliest duration to save
                closest_duration = saving_frames_durations[0]
            except IndexError:
                # the list is empty, all duration frames were saved
                endFile(f, frames_added, frame_lengths)
                
                break
            if frame_duration >= closest_duration:
                frames_added+=1
                written_pixels = 0
                # if closest duration is less than or equals the frame duration, 
                # then save the frame
                
                height, width, channels = frame.shape
                
                
                #f.writelines("{")
                
                # Previous pixel color. 'n' for null, 'w' for white, 'b' for black
                prev_pix = 'n'
                
                # The number of pixels in a row that have the same color
                pix_counter = 0
                
                for y in range(RES_HEIGHT):
                    for x in range(RES_WIDTH):
                        if(frame[int(y * height/RES_HEIGHT), int(x * width/RES_WIDTH), 1] > 200):
                            
                            # If it's the beginning of the frame,
                            # set the pixel to the first color
                            if(prev_pix == 'n'):
                                prev_pix = 'w'
                                
                            # If the previous pixel was black,
                            # Print the last row of same pixel
                            # (the least significant bit is the color)
                            # then reset counter and set prev color
                            elif(prev_pix == 'b'):
                                f.writelines(hex((pix_counter -1) << 1) + ",")
                                written_pixels+=1
                                
                                pix_counter = 0
                                prev_pix = 'w'
                            
                            else:
                                # If the row count reaches 127 (including this one)
                                # print it to the file and reset counter
                                if(pix_counter == 127):
                                    f.writelines(hex((0x7F << 1) + 1) + ",")
                                    written_pixels+=1
                                    
                                    pix_counter = 0
                        
                        else:
                            
                            # If it's the beginning of the frame,
                            # set the pixel to the first color
                            if(prev_pix == 'n'):
                                prev_pix = 'b'
                            
                            
                            # If the previous pixel was white,
                            # Print the last row of same pixel
                            # (the least significant bit is the color)
                            # then reset counter and set prev color
                            elif(prev_pix == 'w'):
                                f.writelines(hex(((pix_counter -1) << 1) + 1) + ",")
                                written_pixels+=1
                                
                                pix_counter = 0
                                prev_pix = 'b'
                            
                            # If the row count reaches 128 (including this one)
                            # print it to the file and reset counter
                            else:
                                if(pix_counter == 127):
                                    f.writelines(hex(0x7F << 1) + ",")
                                    written_pixels+=1
                                    
                                    pix_counter = 0
                        
                        pix_counter+=1
                
                f.writelines(hex(((pix_counter -1) << 1) + (0 if prev_pix == 'b' else 1)) + ",")
                written_pixels+=1
                
                frame_lengths.append(written_pixels)
                
                #frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
                #cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame) 
                # drop the duration spot from the list, since this duration spot is already saved
                try:
                    saving_frames_durations.pop(0)
                except IndexError:
                    pass
            # increment the frame count
            count += 1

if __name__ == "__main__":
    main(VIDEO_FILE)