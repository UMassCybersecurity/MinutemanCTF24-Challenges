var _____WB$wombat$assign$function_____ = function(name) {return (self._wb_wombat && self._wb_wombat.local_init && self._wb_wombat.local_init(name)) || self[name]; };
if (!self.__WB_pmw) { self.__WB_pmw = function(obj) { this.__WB_source = obj; return this; } }
{
  let window = _____WB$wombat$assign$function_____("window");
  let self = _____WB$wombat$assign$function_____("self");
  let document = _____WB$wombat$assign$function_____("document");
  let location = _____WB$wombat$assign$function_____("location");
  let top = _____WB$wombat$assign$function_____("top");
  let parent = _____WB$wombat$assign$function_____("parent");
  let frames = _____WB$wombat$assign$function_____("frames");
  let opener = _____WB$wombat$assign$function_____("opener");

function options() {
  addhtml("<div style='position:fixed; top:0; left:0; text-align:center; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:1.5; color:white; background-color:black; font-size:125%;' id='options'>Do you want to <button class='button'onclick='change()'>Change the flashing text</button><button onclick='openwindowform()' class='button'>Open window form</button><button onclick='closeoptions()' class='button'>Close options</button></div>");
}
function enablenarrations() {
alert("thing")
  } 
function change() {
  text = prompt("what should the flashing text be?");
  document.getElementById("flashingtext").innerText = text;
  document.cookie = "text=" + text 
  if(text == "" || text == null) {
    change();
  }
  remove("options")
}
function openwindowform() {
    remove("options")
    window.open("https://web.archive.org/web/20220724185056/https://minecraft--duck132912.repl.co", "", "width=10000,height=10000");
}
function closeoptions() {
  remove("options")
}
function quit() {
  close();
  window.location = "";
}
function how() {
  addhtml("<div id='stophow' style='color: red; position:absolute; left:0; bottom:0; font-weight: bold; font-size: 60px;z-index: 2;cursor: pointer;' onclick='stophow();'>x</div><div style='position:fixed; top:0; left:0; text-align:center; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:1; color:white; background-color:black; font-size:125%;' id='instructions'>Use WASD to move around, T to talk, 1 to 9 to change blocks, B to get new blocks, mouse to look around, R to respawn, ESC to pause and G to teleport a random player into your world. To go back to the starting screen when you are in-game press ESC and CLICK THE RED X IN THE CORNER OF THE SCREEN TO CLOSE IN THE REAL GAME THE RED X IS ON THE TOP RIGHT</div>")
}

}
/*
     FILE ARCHIVED ON 18:50:56 Jul 24, 2022 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 20:20:35 Oct 05, 2024.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  captures_list: 0.969
  exclusion.robots: 0.047
  exclusion.robots.policy: 0.037
  esindex: 0.009
  cdx.remote: 323.453
  LoadShardBlock: 1978.492 (3)
  PetaboxLoader3.resolve: 862.863 (5)
  PetaboxLoader3.datanode: 1962.777 (6)
  load_resource: 1179.452 (2)
  loaddict: 30.759
*/