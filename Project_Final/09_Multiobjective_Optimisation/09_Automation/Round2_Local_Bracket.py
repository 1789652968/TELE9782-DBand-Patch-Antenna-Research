"""One last Y-position bracket on the measured E-plane beam reversal, at unchanged port plane."""
from Round2_Search import *
def local(de):
    rows={q['name']:q for q in completed()}
    v=rows['ShiftBracket75'];u=rows['FeedShiftPlus'];x=config(v)['shift_y'];b=config(u)['shift_y']
    signed=lambda q:q['theta']*math.sin(math.radians(q['phi']))
    a1=signed(v);a2=signed(u)
    if a1*a2>=0:return
    pos=round(x+(b-x)*a1/(a1-a2),4)
    core=run(de,Y,'ShiftNull75',{'shift_y':pos})
    # Use the moderate 85 um substrate. Change lateral spacing and ground only within the trialled range.
    h=rows['ShiftBracket85']
    if h['theta']>4 or h['G0']<8:
        sg=signed(h);adjust=max(-.04,min(.06,sg*(b-x)/(a1-a2)))
        off=round(config(h)['shift_y']+adjust,4)
        run(de,Y,'ShiftNull85Lateral',thick(.085)|dict(shift_y=off,ground_width=3.0,array_spacing=1.20))

