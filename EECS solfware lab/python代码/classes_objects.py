class point:
    x='x坐标'
    y='y坐标'
class rectangle:
    width='宽度'
    height='长度'
    corner='顶点'
box=rectangle()
box.width=100
box.height=200
box.corner=point()
box.corner.x=0.0
box.corner.y=0.0
def find_center(rect):
    p=point()
    p.x=rect.corner.x+rect.width/2
    p.y=rect.corner.y+rect.height/2
    return p
def print_point(p):
    print('%g,%g'%p.x,p.y)
  
print_point(find_center(box))
