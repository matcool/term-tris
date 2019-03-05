def line(screen,x1,y1,x2,y2,**options):
    screen.move(int(x1),int(y1))
    screen.draw(int(x2),int(y2),**options)

def fancyRect(screen,x,y,w,h):
	tiles = ['│','─','┌','┐','└','┘']
	line(screen,x,y,x+w,y,char=tiles[1])
	line(screen,x,y,x,y+h,char=tiles[0])
	line(screen,x,y+h,x+w,y+h,char=tiles[1])
	line(screen,x+w,y,x+w,y+h,char=tiles[0])
	screen.print_at(tiles[2],x,y)
	screen.print_at(tiles[3],x+w,y)
	screen.print_at(tiles[4],x,y+h)
	screen.print_at(tiles[5],x+w,y+h)