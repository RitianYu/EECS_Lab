#11.1.1

possibleColors = ['black', 'white', 'red', 'green' ,'blue']

#无法区分白色和绿色并且看到绿色和白色的概率相等。
def whiteEqGreenObsDist(actualColor):
    
    #在绿色或者白色的方形里，返回绿色和白色的概率分别是0.5。
    
    if actualColor == 'white' or actualColor=='greem':   
        return dist.DDist({white: 0.5, green: 0.5})
    else:                           #在其他颜色的房间里返回房间的实际颜色，即实际颜色的概率为1。
        return dist.DDist({actualColor: 1})

#将白色看成绿色。将绿色看成白色。
def whiteVsGreenObsDist(actualColor):
    if actualColor == 'white':      #白色房间内看到绿色，返回绿色的概率为1。
        return dist.DDist({green:1})
    if actualColor == 'green':      #绿色房间看到白色，返回白色的概率为1。
        return dist.DDist({white:1})
    else:                           #其他房间看到真实颜色，真实颜色的概率为1。
        return dist.DDist({actualColor:1})

#0.8的概率观察到真实颜色，0.2的概率观察到其他颜色且每种颜色被观察到的概率相等。
def noisyObs(actualColor):
    d={}
    for Colors in possibleColors:   #0.2的概率观察到possibleColors中的剩余颜色
        d[Colors] = (1.0-0.8)/(len(possibleColors)-1.0)   #先对possibleColors中的颜色都赋以概率，概率的值为
                                                          #0.2/possibleColors中的非真实颜色数，即总颜色数-1
    d[actualColor] = 0.8            #再重新覆盖，定义看到真实颜色的概率为0.8。
    return dist.DDist(d)

noisyObsModel = makeObservationModel(standardHallway, noisyObs)

#step5
#11.1.2

def ringDynamic(loc, act, hallwayLength):
    if loc+act >=0 and loc+act <= hallwayLength-1 :   #如果loc+act没有超出0至hallwayLength-1，返回三者中间值
        return util.clip(loc + act , 0 , hallwayLength - 1)
    elif loc+act > hallwayLength-1:     #如果(loc+act)>hallwayLength-1,相当于向右运动并且至hallwayLength-1向右的下一步从跳跃到0
                                        #(loc+act)是假如hallwayLength是无限时的坐标，其与hallwayLength的余数即为有限hallwayLength实际坐标。
        return (loc+act) % hallwayLength
  
    else:       #如果(loc+act)<0，相当于向左运动并且至0向左的下一步从跳跃到hallwayLength-1
                #其方法与上一步类似，但因为是从右向左运动所以实际坐标应该用hallwayLength减去余数。
        return hallwayLength-abs(loc+act) % hallwayLength


def leftSlipTrans(nominalLoc, hallwayLength):
    if nominalLoc >0 :      #当理论位置大于0时，由于向左滑动概率为0.1，所以在理论位置概率为0.9，在其左边位置的概率为0.1
        return dist.DDist({nominalLoc:0.9, nominalLoc-1:0.1}
    else:                   #当理论位置小于等于0时，由于无法向左移动，所以留在0处的概率为1。
        return dist.DDist({nominalLoc:1})

def noisyTrans(nominalLoc, hallwayLength):  
    if nominalLoc >0 and nominalLoc <hallwayLength-1:   #当理论位置在非中间时刻的位置时，返回在理论位置的概率为0.8，在理论位置左右的概率各为0.1。
        return dist.DDist({nominalLoc:0.8,nominalLoc-1:0.1,nominalLoc+1:0.1})
    elif nominalLoc == hallwayLength-1:     #当理论位置在最右边时，由于无法向右运动，所以在其左边位置的概率为0.1，在其理论位置的概率为0.9。
        return dist.DDist({nominalLoc:0.9,nominalLoc-1:0.1})
    else:       #当理论位置在最左边时，由于无法向左运动，所以在其右边位置的概率为0.1，在其理论位置的概率为0.9。
        return dist.DDist({nominalLoc:0.9,nominalLoc+1:0.1})

noisyTransModel = makeTransitionModel(standardDynamics, noisyTrans, standardHallway)