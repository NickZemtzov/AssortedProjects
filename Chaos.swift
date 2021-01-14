//
//  ChaosVisualizer.swift
//  ChaosSaver
//
//  Created by Nick Zemtzov on 12/2/20.
//

import ScreenSaver

class Chaos: ScreenSaverView {
    struct point {
        var position = CGPoint.zero
        var color: NSColor
        //var isInFrame: Bool
        //var velocity = CGVector.zero
    }
    private var time: CGFloat = -3
    private var iterations = 800
    private var PointArray = [point]()
    private var parameters = [CGFloat]()
    private var hasStarted = false
    private var restart = false
    //override var isOpaque: Bool {
      //  return false
    //}

    override init?(frame: NSRect, isPreview: Bool) {
        super.init(frame: frame, isPreview: isPreview)
        //self.isOpaque
        //if self.isOpaque == false{
        //    iterations = 50
        //}
        
        for _ in 0..<18 {//18 is the number of current parameters
            let r = Int.random(in: -1..<2)
            parameters.append(CGFloat(r))
        }
        let displayString = makeStringFromParameters()
        
        let debugTextView = NSTextView(frame: frame)
        debugTextView.font = .labelFont(ofSize: 20)
        debugTextView.string = displayString
        debugTextView.drawsBackground = false
        self.addSubview(debugTextView)
        
        for i in 0..<iterations {//the color wheel to rgb is in six steps, starting with red at full: G->1,R->0,B->1,G->0,R->1,B->0
            if i<iterations/6 {
                PointArray.append(point(position:CGPoint.zero, color: NSColor.init(red: 1.0, green: CGFloat(i)/CGFloat(iterations/6), blue: 0.0, alpha: 1.0)))
            } else if i>iterations/6 && i<2*iterations/6{
                PointArray.append(point(position:CGPoint.zero, color: NSColor.init(red: 1-(CGFloat(i)-CGFloat(iterations/6))/CGFloat(iterations/6), green: 1.0, blue: 0.0, alpha: 1.0)))
            } else if i>2*iterations/6 && i<3*iterations/6{
                PointArray.append(point(position:CGPoint.zero, color: NSColor.init(red: 0.0, green: 1.0, blue: (CGFloat(i)-CGFloat(2*iterations/6))/CGFloat(iterations/6), alpha: 1.0)))
            } else if i>3*iterations/6 && i<4*iterations/6{
                PointArray.append(point(position:CGPoint.zero, color: NSColor.init(red: 0.0, green: 1-(CGFloat(i)-CGFloat(3*iterations/6))/CGFloat(iterations/6), blue: 1.0, alpha: 1.0)))
            } else if i>4*iterations/6 && i<5*iterations/6{
                PointArray.append(point(position:CGPoint.zero, color: NSColor.init(red: (CGFloat(i)-CGFloat(4*iterations/6))/CGFloat(iterations/6), green: 0.0, blue: 1.0, alpha: 1.0)))
            } else if i>5*iterations/6 && i<iterations/6{
                PointArray.append(point(position:CGPoint.zero, color: NSColor.init(red: 1.0, green: 0.0, blue: 1-(CGFloat(i)-CGFloat(5*iterations/6))/CGFloat(iterations/6), alpha: 1.0)))
            }
        }
    }
    @available(*, unavailable)
    required init?(coder decoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    override func animateOneFrame() {
        if restart == true {
            restart = false
            hasStarted = false
            time = -3
            for i in 0..<18 {//18 is the number of current parameters
                let r = Int.random(in: -1..<2)
                parameters[i]=CGFloat(r)
            }
            let displayString = makeStringFromParameters()
            
            let debugTextView = NSTextView(frame: frame)
            debugTextView.font = .labelFont(ofSize: 20)
            debugTextView.string = displayString
            debugTextView.drawsBackground = false
            self.replaceSubview(self.subviews[0], with: debugTextView)
            
            for i in 0..<PointArray.count {//the color wheel to rgb is in six steps, starting with red at full: G->1,R->0,B->1,G->0,R->1,B->0
                if i<iterations/6 {
                    PointArray[i] = point(position:CGPoint.zero, color: NSColor.init(red: 1.0, green: CGFloat(i)/CGFloat(iterations/6), blue: 0.0, alpha: 1.0))
                } else if i>iterations/6 && i<2*iterations/6{
                    PointArray[i] = point(position:CGPoint.zero, color: NSColor.init(red: 1-(CGFloat(i)-CGFloat(iterations/6))/CGFloat(iterations/6), green: 1.0, blue: 0.0, alpha: 1.0))
                } else if i>2*iterations/6 && i<3*iterations/6{
                    PointArray[i] = point(position:CGPoint.zero, color: NSColor.init(red: 0.0, green: 1.0, blue: (CGFloat(i)-CGFloat(2*iterations/6))/CGFloat(iterations/6), alpha: 1.0))
                } else if i>3*iterations/6 && i<4*iterations/6{
                    PointArray[i] = point(position:CGPoint.zero, color: NSColor.init(red: 0.0, green: 1-(CGFloat(i)-CGFloat(3*iterations/6))/CGFloat(iterations/6), blue: 1.0, alpha: 1.0))
                } else if i>4*iterations/6 && i<5*iterations/6{
                    PointArray[i] = point(position:CGPoint.zero, color: NSColor.init(red: (CGFloat(i)-CGFloat(4*iterations/6))/CGFloat(iterations/6), green: 0.0, blue: 1.0, alpha: 1.0))
                } else if i>5*iterations/6 && i<iterations/6{
                    PointArray[i] = point(position:CGPoint.zero, color: NSColor.init(red: 1.0, green: 0.0, blue: 1-(CGFloat(i)-CGFloat(5*iterations/6))/CGFloat(iterations/6), alpha: 1.0))
                }
            }
        }
        
        super.animateOneFrame()
        var xPos = time
        var yPos = time
        for i in 0..<PointArray.count {
            PointArray[i] = point(position: CGPoint(x:xPos*frame.width+frame.width/2, y:yPos*frame.height+frame.height/2), color: PointArray[i].color)
            let temp = xPos
            xPos = parameters[0]*xPos + parameters[3]*xPos*yPos + parameters[4]*xPos*time + parameters[6]*xPos*xPos + parameters[1]*yPos + parameters[2]*time + parameters[5]*yPos*time + parameters[7]*yPos*yPos + parameters[8]*time*time
            yPos = parameters[9]*temp + parameters[10]*yPos + parameters[11]*time + parameters[12]*temp*yPos + parameters[13]*temp*time + parameters[14]*yPos*time + parameters[15]*temp*temp + parameters[16]*yPos*yPos + parameters[17]*time*time
        }
        time += CalculateTimeStep()
        setNeedsDisplay(bounds)
    }
    
    override func draw(_ rect: NSRect) {
        //drawBackground(NSColor.init(red: 0.0, green: 0.0, blue: 0.0, alpha: 0.1))
        //super.draw(rect)
        for point in 1..<PointArray.count {
            drawPoint(p: PointArray[point])
        }
    }
    
    private func drawBackground(_ color: NSColor) {
        let background = NSBezierPath(rect: bounds)
        color.setFill()
        background.fill()
    }
    private func drawPoint(p: point) {
        let pixel = NSRect(x: p.position.x,
                              y: p.position.y,
                              width: 3,
                              height: 3)
        p.color.setFill()
        pixel.fill()
    }
    
    private func CalculateTimeStep() -> CGFloat{
        var pointsInFrame = 0
        //var netDensity: CGFloat = 0
        for i in 0..<PointArray.count {
            if PointArray[i].position.x>0 && PointArray[i].position.x<bounds.width && PointArray[i].position.y>0 && PointArray[i].position.y<bounds.height {
                pointsInFrame += 1
                //calculate distance to closest point to measure density
                //var max: CGFloat = 100000
                //for j in 0..<PointArray.count {
                //    if j==i {// && distanceBetweenTwoPoints(p1: PointArray[i], p2: PointArray[j])<max {
                //    } else if distanceBetweenTwoPoints(p1: PointArray[i], p2: PointArray[j])<max {
                //        max = distanceBetweenTwoPoints(p1: PointArray[i], p2: PointArray[j])
                //    }
                //}
                //netDensity += max
            }
        }
        if pointsInFrame == 0 {
            if hasStarted == true {
                restart = true
            }
            return 0.3 //this is the base timestep if theres nothing in frame
        } else {
            hasStarted = true
            //here's the specifics of how the timestep is calculated. It works optimally with 800 points
            var multiplier = CGFloat(0.85)//modify this depending on how well time works
            for _ in 0..<pointsInFrame {
                multiplier = multiplier*0.85//also here
            }
            if 0.1*multiplier < 0.0015 {//lower limit
                return 0.0015
            } else {
                return 0.1*multiplier
            }
        }
        
    }
    
    private func distanceBetweenTwoPoints(p1: point, p2: point) -> CGFloat{
        return (pow(p1.position.x - p2.position.x,2) + pow(p1.position.y - p2.position.y,2)).squareRoot()
    }
    
    private func makeStringFromParameters() -> String{
        //create equation using randomness here. It has the form x or y = _x _y _t _xt _yt _xy _yy _xx _tt
        //so you need 9 randoms between 0 and 2 so create a dictionary with keys as those random numbers and the entries as
        var displayString = "x'="
        var hasFirst = false
        if parameters[0] == CGFloat(1) {
            displayString += " x"
            hasFirst = true
        } else if parameters[0] == CGFloat(-1) {
            displayString += " - x"
            hasFirst = true
        }
        if parameters[1] == CGFloat(1) && hasFirst == true {
            displayString += " + y"
            hasFirst = true
        } else if parameters[1] == CGFloat(1) && hasFirst == false {
            displayString += " y"
            hasFirst = true
        } else if parameters[1] == CGFloat(-1) {
            displayString += " - y"
            hasFirst = true
        }
        if parameters[2] == CGFloat(1) && hasFirst == true {
            displayString += " + t"
            hasFirst = true
        } else if parameters[2] == CGFloat(1) && hasFirst == false {
            displayString += " t"
            hasFirst = true
        } else if parameters[2] == CGFloat(-1) {
            displayString += " - t"
            hasFirst = true
        }
        if parameters[3] == CGFloat(1) && hasFirst == true {
            displayString += " + xt"
            hasFirst = true
        } else if parameters[3] == CGFloat(1) && hasFirst == false {
            displayString += " xt"
            hasFirst = true
        } else if parameters[3] == CGFloat(-1) {
            displayString += " - xt"
            hasFirst = true
        }
        if parameters[4] == CGFloat(1) && hasFirst == true {
            displayString += " + yt"
            hasFirst = true
        } else if parameters[4] == CGFloat(1) && hasFirst == false {
            displayString += " yt"
            hasFirst = true
        } else if parameters[4] == CGFloat(-1) {
            displayString += " - yt"
            hasFirst = true
        }
        if parameters[5] == CGFloat(1) && hasFirst == true {
            displayString += " + xy"
            hasFirst = true
        } else if parameters[5] == CGFloat(1) && hasFirst == false {
            displayString += " xy"
            hasFirst = true
        } else if parameters[3] == CGFloat(-1) {
            displayString += " - xy"
            hasFirst = true
        }
        if parameters[6] == CGFloat(1) && hasFirst == true {
            displayString += " + x^2"
            hasFirst = true
        } else if parameters[6] == CGFloat(1) && hasFirst == false {
            displayString += " x^2"
            hasFirst = true
        } else if parameters[6] == CGFloat(-1) {
            displayString += " - x^2"
            hasFirst = true
        }
        if parameters[7] == CGFloat(1) && hasFirst == true {
            displayString += " + y^2"
            hasFirst = true
        } else if parameters[7] == CGFloat(1) && hasFirst == false {
            displayString += " y^2"
            hasFirst = true
        } else if parameters[7] == CGFloat(-1) {
            displayString += " - y^2"
            hasFirst = true
        }
        if parameters[8] == CGFloat(1) && hasFirst == true {
            displayString += " + t^2"
            hasFirst = true
        } else if parameters[8] == CGFloat(1) && hasFirst == false {
            displayString += " t^2"
            hasFirst = true
        } else if parameters[8] == CGFloat(-1) {
            displayString += " - t^2"
            hasFirst = true
        }
        if hasFirst == false {
            displayString += "0"
        }
        displayString += "\n"
        displayString += "y'="
        hasFirst = false
        if parameters[9] == CGFloat(1) {
            displayString += " x"
            hasFirst = true
        } else if parameters[9] == CGFloat(-1) {
            displayString += " - x"
            hasFirst = true
        }
        if parameters[10] == CGFloat(1) && hasFirst == true {
            displayString += " + y"
            hasFirst = true
        } else if parameters[10] == CGFloat(1) && hasFirst == false {
            displayString += " y"
            hasFirst = true
        } else if parameters[10] == CGFloat(-1) {
            displayString += " - y"
            hasFirst = true
        }
        if parameters[11] == CGFloat(1) && hasFirst == true {
            displayString += " + t"
            hasFirst = true
        } else if parameters[11] == CGFloat(1) && hasFirst == false {
            displayString += " t"
            hasFirst = true
        } else if parameters[11] == CGFloat(-1) {
            displayString += " - t"
            hasFirst = true
        }
        if parameters[12] == CGFloat(1) && hasFirst == true {
            displayString += " + xt"
            hasFirst = true
        } else if parameters[12] == CGFloat(1) && hasFirst == false {
            displayString += " xt"
            hasFirst = true
        } else if parameters[12] == CGFloat(-1) {
            displayString += " - xt"
            hasFirst = true
        }
        if parameters[13] == CGFloat(1) && hasFirst == true {
            displayString += " + yt"
            hasFirst = true
        } else if parameters[13] == CGFloat(1) && hasFirst == false {
            displayString += " yt"
            hasFirst = true
        } else if parameters[13] == CGFloat(-1) {
            displayString += " - yt"
            hasFirst = true
        }
        if parameters[14] == CGFloat(1) && hasFirst == true {
            displayString += " + xy"
            hasFirst = true
        } else if parameters[14] == CGFloat(1) && hasFirst == false {
            displayString += " xy"
            hasFirst = true
        } else if parameters[14] == CGFloat(-1) {
            displayString += " - xy"
            hasFirst = true
        }
        if parameters[15] == CGFloat(1) && hasFirst == true {
            displayString += " + x^2"
            hasFirst = true
        } else if parameters[15] == CGFloat(1) && hasFirst == false {
            displayString += " x^2"
            hasFirst = true
        } else if parameters[15] == CGFloat(-1) {
            displayString += " - x^2"
            hasFirst = true
        }
        if parameters[16] == CGFloat(1) && hasFirst == true {
            displayString += " + y^2"
            hasFirst = true
        } else if parameters[16] == CGFloat(1) && hasFirst == false {
            displayString += " y^2"
            hasFirst = true
        } else if parameters[16] == CGFloat(-1) {
            displayString += " - y^2"
            hasFirst = true
        }
        if parameters[17] == CGFloat(1) && hasFirst == true {
            displayString += " + t^2"
            hasFirst = true
        } else if parameters[17] == CGFloat(1) && hasFirst == false {
            displayString += " t^2"
            hasFirst = true
        } else if parameters[17] == CGFloat(-1) {
            displayString += " - t^2"
            hasFirst = true
        }
        if hasFirst == false {
            displayString += "0"
        }
        return displayString
    }
}
