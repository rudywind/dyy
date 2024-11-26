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

function GetClock(elm){
    var tzOffset = +7,
        d  = new Date(),
        dx = d.toGMTString(),
        dx = dx.substr(0,dx.length -3);
    
    d.setTime(Date.parse(dx))
    d.setHours(d.getHours()+tzOffset);

    var nday   = d.getDay(),
        nmonth = d.getMonth(),
        ndate  = d.getDate(),
        nyear  = d.getYear(),
        nhour  = d.getHours(),
        nmin   = d.getMinutes(),
        nsec   = d.getSeconds(), ap;
    if (nhour == 0){ ap = " AM"; nhour = 12; }
    else if (nhour< 12){ ap = " AM"; }
    else if (nhour == 12){ ap = " PM"; }
    else if (nhour > 12){ ap = " PM"; nhour -= 12; }

    if (nyear < 1000) nyear+=1900;
    if (nmin <= 9) nmin="0"+nmin;
    if (nsec <= 9) nsec="0"+nsec;

    document.getElementById(elm).innerHTML = nhour+":"+nmin+":"+nsec+ap+"";
}

function load_history(days) {
    $('#main-wrapper').html($('#loader').children().clone());
    $.ajax({
        type     : 'POST',
        url      : $('#website_url').val() + '/wp-admin/admin-ajax.php',
        data     : { 'action' : 'pools_history', 'days' : days },
        // dataType : 'json',
        success  : function(pools_history) {
            $('#main-wrapper').html(pools_history);
        }
    });
}

$(document).ready(function() {
    $('.nav-link').on('click', function(e) {
        e.preventDefault();
        
        var nLink = $(this).attr('href');
        var nText = $(this).attr('title');

        if (nLink === '#ajax') {
            load_history(nText);
        } else {
            window.location.href = nLink;
        }
    });
});

}
/*
     FILE ARCHIVED ON 10:17:31 Apr 11, 2024 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 14:41:19 Nov 26, 2024.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  captures_list: 0.688
  exclusion.robots: 0.024
  exclusion.robots.policy: 0.01
  esindex: 0.015
  cdx.remote: 21.533
  LoadShardBlock: 54.488 (3)
  PetaboxLoader3.datanode: 86.263 (5)
  load_resource: 158.403
  PetaboxLoader3.resolve: 118.538
  loaddict: 21.88
*/