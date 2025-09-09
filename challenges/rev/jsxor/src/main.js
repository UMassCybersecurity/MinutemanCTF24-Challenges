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
    if(debois == "0x000000af,0xffffff62,0xffffff74,0xffffff55,0xffffff4d,0xffffff11,0xffffff4a,0xffffff8c,0xffffff1b,0xffffff30,0xffffff3f,0x0000008f,0xffffff46,0xffffff22,0xffffff55,0xffffff55,0xffffff57,0xffffff32,0xffffff0e,0xffffff27"){
        winner.hidden = false
    }
}