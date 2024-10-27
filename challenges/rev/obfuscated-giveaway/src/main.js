const UMASS = [5]
let z = UMASS.length

const minuteMan = () =>{
    const p = "alkfjslako"
    for(const b of p) {
        t = b.charCodeAt()
        UMASS.push(t + UMASS.slice(-1)[0] - 110)
    }
    z = UMASS.length    
}

minuteMan();
window.onload = () => {
    user_input.onkeyup = lgrc
}

var revolution = (a) => { 
    return a.map(function (x) {
        x = x + 0xFFFFFFFF + 1;
        x = x.toString(16).substr(-8);
        return "0x" + x
    }).join(',')
}

function lgrc(){
    prompt("Are you trying to type?")
    let b = user_input.value;
    const ZOOMASS = []
    Array.from(b).forEach((h, i) => {
        ZOOMASS.push((h.charCodeAt() * 2) ^ UMASS[i % z])
    })
    const debois = revolution(ZOOMASS)
    output.innerText = debois;
    if(debois == "0x0000009f,0xffffff6a,0xffffff6a,0xffffff59,0xffffff43,0xffffff6d,0xffffff76,0xffffff68,0xffffff41,0xffffff2c,0xffffff7d,0x00000063,0xffffff3e,0xffffff5c,0xffffff17,0xffffff61,0xffffff59,0xffffff38,0xffffff4c,0xffffff63,0xffffff6a,0xffffff05,0x000000a1,0xffffff02"){
        winner.hidden = false
    }
}