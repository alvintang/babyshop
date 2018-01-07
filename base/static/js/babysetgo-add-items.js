// alert("babysetgo!");

// var modal=`
//         <i class="close icon"></i>
//         <div class="header">
//             Confirm Action <span class="header-sub">- No Local Patient Profile Record</span>
//         </div>
//         <div class="image content">
//             <div class="syncProfile description">
//                 A description can appear on the right
//             </div>
//         </div>
//         <div class="actions">
//             <div class="ui button" id="cancel">Cancel</div>
//             <a class="ui button sync-profile">Request Access and Sync</a>
//         </div>`;

// s=document.createElement('div');
// s.class="modal babysetgoModal";
// s.innerHTML=modal;

// document.body.appendChild(s);

var modal = document.createElement('iframe');
var reg_id = $('#babysetgo').attr('reg_id');
var url = encodeURIComponent(window.location.href)
modal.setAttribute('src', 'https://babysetgo.ph/external/add/?url='+url+'&reg_id='+reg_id);
modal.setAttribute('scrolling', 'yes'); // no scroll bars on the iframe please
modal.className = 'modal';
modal.id = 'babysetgo-iframe';
document.body.appendChild(modal);

$(document).add(parent.document).click(function(e) {
    var iframe = $('iframe');
    if (!iframe.is(e.target) && iframe.has(e.target).length === 0) {
        modal.parentNode.removeChild(modal);
    }
});

window.onmessage=function(msg) {
      var fra=document.getElementById("babysetgo-iframe");
      if(msg.data && msg.data.name=="Close" && msg.source==fra.contentWindow) {
          fra.style.display="none";
          }
      };
