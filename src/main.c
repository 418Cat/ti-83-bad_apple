#include "graphx.h"
#include "ti/getcsc.h"
#include "sys/timers.h"
#include "bad_apple.h"


/**
 * Here's the compression :
 * A byte is used for anywhere
 * from 1 to 128 pixels.
 * 
 * The least signficant bit is the color
 * The other 7 bits represent how many 
 * pixels in a row have that color, minus one :
 * 0000 000- means 1 pixel
 * 0000 001- means 2 pixels
 * ...
 * 1111 111- means 128 pixels
 * 
 * To get the color, simply 
 * bitmask with 0b1
 * 
 * To get the number of pixels,
 * bitshift to the right once
 * and add 1
 */
void drawCompressedFrame(const unsigned char frames[], int pixel_size[], int current_frame_indices[])
{

	// compute the number of entries the array has for this specific frame
	int frame_length = current_frame_indices[1] - current_frame_indices[0];

	// Keep track of the cursor's position
	int current_x = 0;
	int current_y = 0;

	for(int i = 0; i < frame_length; i++)
	{
		// Bitmask to get the least significant bit.
		// If least least significant bit is 1 then
		// set color to white, else black
		int color = (frames[i + current_frame_indices[0]] & 0b1) * 0xFF;
		gfx_SetColor(color);

		// compute the width of the soon to be drawn pixels
		int pixel_width = ((1 + (frames[i + current_frame_indices[0]] >> 1)) * pixel_size[0]);

		// If the pixel line is on the edge of the video
		if(current_x + pixel_width >= (BADAPPLE_WIDTH * pixel_size[0]))
		{
			// The number of y-lines the pixel line is going to cover
			int y_lines_progressed = (current_x + pixel_width)  /  (BADAPPLE_WIDTH * pixel_size[0]);
			
			// draw the rectangle until the end of the current y-line
			gfx_FillRectangle(current_x, current_y, (BADAPPLE_WIDTH * pixel_size[0]) - current_x, pixel_size[1]);

			// If the line goes over multiple y-lines, draw a big rectangle
			gfx_FillRectangle(0, current_y + pixel_size[1], (BADAPPLE_WIDTH * pixel_size[0]), pixel_size[1] * (y_lines_progressed -1));

			// update the cursor y position
			current_y += pixel_size[1] * y_lines_progressed;

			// draw the rest of the rectangle on the new line
			gfx_FillRectangle(0, current_y, (current_x + pixel_width) % (BADAPPLE_WIDTH * pixel_size[0]), pixel_size[1]);

			// update the cursor x position
			current_x = (current_x + pixel_width) % (BADAPPLE_WIDTH * pixel_size[0]);
		}
		else
		{
			// draw the complete rectangle
			gfx_FillRectangle(current_x, current_y, pixel_width, pixel_size[1]);

			// update the cursor position
			current_x += pixel_width;
		}

		// Draw a frame around the video
		/*gfx_SetColor(0x77);
		gfx_FillRectangle(BADAPPLE_WIDTH*pixel_size[0], 0, 3, BADAPPLE_HEIGHT*pixel_size[1] +3);
		gfx_FillRectangle(0, BADAPPLE_HEIGHT*pixel_size[1], BADAPPLE_WIDTH*pixel_size[0], 3);*/
	}

}

int main()
{
	gfx_Begin();	

	/*
	 * I'm going to use either black or white.
	 * By default, the transparent color is at
	 * index 0xFF so white.
	 * Changed to some unused index
	 */
	gfx_SetTransparentColor(2);

	int pixel_size[] =
	{
		GFX_LCD_WIDTH / BADAPPLE_WIDTH,
		GFX_LCD_HEIGHT / BADAPPLE_HEIGHT
	};

	int sleep_ms = (int)(1000./BADAPPLE_FPS);

	bool pause = false;
	int current_frame = 0;
	// Keep track of where the loop is in the list
	int list_offset = 0;
	while(true)
	{

		// While pause is true, wait until a key is pressed
		int key = os_GetCSC();
		while(key != 3 && key != 2 && key != 4 && key != 9 && pause)
		{
			key = os_GetCSC();
		}

		switch (key)
		{
		// Do nothing, go forward one frame
		case 3: // Right arrow
			break;
		
		// Go back two frames
		case 2: // Left arrow
			current_frame-=2;
			list_offset-= frameLengths[current_frame+1];
			list_offset-= frameLengths[current_frame];

			// Don't go below 0, bad things could happen. Really bad things.
			// You don't want to know what.
			if(current_frame < 0)
			{
				current_frame = 0;
				list_offset = 0;
			}

			// Resume :D
			break;
		
		// Pause/Unpause
		case 4: // Up arrow
			pause = !pause;
			break;
		
		// Disable graph mode and exit
		case 9: // Enter key
			gfx_End();
			return 0;
			break;
		
		default:
			break;
		}

		// Get the frame's bottom and top indices
		int current_frame_indices[] = {list_offset, list_offset+frameLengths[current_frame]};

		drawCompressedFrame(badApple, pixel_size, current_frame_indices);

		msleep(sleep_ms);
		
		list_offset += frameLengths[current_frame];
		current_frame++;

		// Loop around
		if(current_frame == BADAPPLE_FRAMES)
		{
			list_offset = 0;
			current_frame = 0;

			gfx_End();
			return 0;
		}
	}

	gfx_End();
	return 0;
	
}
