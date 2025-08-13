#River

/Hearts of Iron IV/map/rivers.bmp is an 8-bit indexed bitmap file that decides the positioning of rivers. Rivers must be exactly one pixel thick and only go in orthogonal directions: pixels do not connect diagonally. As the river counts as a level 1 railway[6], particularly long rivers can cause the game to slow down or run unstably. The river map is a 8-bit indexed bitmap with the same dimensions as the provinces bitmap.
To correctly render, each river must have exactly one, by default green, start marker. In this case a river is taken as a single contiguous block of river pixels: those connected with red flow-in or yellow flow-out sources count as the same river as the main flow. Only the 'main branch' of the river should have the green source pixel, any branch connected to it via the red flow-in shouldn't have it.
Colours used in rivers.bmp
Index	Colour	Function
0	(0, 255, 0)	The source of a river
1	(255, 0, 0)	Flow-in source. Used to join multiple 'source' paths into one river.
2	(255, 252, 0)	Flow-out source. Used to branch outwards from one river.
3	(0, 225, 255)	River with narrowest texture.
4	(0, 200, 255)	River with narrow texture
5	(0, 150, 255)	
6	(0, 100, 255)	River with wide texture.
7	(0, 0, 255)	
8	(0, 0, 225)	
9	(0, 0, 200)	
10	(0, 0, 150)	
11	(0, 0, 100)	River with widest texture.
By default, indexes 0[7] up to including 6[8] are treated as small rivers for game mechanics, indexes up to including 11[9] as large rivers. Pixels with any other index within the file do not get read in-game and serve as 'comments', usually used to signify the land province outlines to make it easier to place rivers.
If the path connecting the centres of two provinces overlaps at least one river pixel, it is considered a river crossing. If it intersects multiple river pixels of different types, the crossing type is implementation defined. To avoid player confusion, province paths should either clearly cut or stay clear of a river.
A possible error to encounter is MAP_ERROR: Palette in rivers.bmp is probably not correct. This can entirely be ignored: the rivers.bmp file will be loaded regardless and, unlike other map errors, this does not prevent the game from loading without debug mode.
This error is caused by GIMP: editing in Photoshop does not produce this. By default, the DIB header is set to say that the colourmap has 0 colours despite the fact that the colourmap still contains 256 colours. This is to ensure that the game does not spend time reading colours within the BMP file and instead skips straight to the bitmap itself. GIMP instead sets the DIB header to say that there are 256 colours in the palette, which is unexpected by the game. This cannot be fixed within GIMP itself, however, assuming that the rivers bitmap is otherwise correct (Saved in 8-bit indexed mode with BITMAPINFOHEADER) this can also be fixed by opening the rivers bitmap within a hex editor and changing two values: addresses 00 00 00 2F and 00 00 00 33 should both be 00 instead of 01 as set by GIMP.