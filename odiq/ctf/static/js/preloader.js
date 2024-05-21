var strings = [
    ""
  ];
  
  var preloader = document.getElementById('preloader');
  var delay = 1000;
  var count = 0;
  var repeat = 0;
  
  function addLog() {
    var row = createLog('', count);
    preloader.appendChild(row);
    
    goScrollToBottom();
    
    count++;
    
    if (repeat == 0) {
      if (count > 3) {
        delay = 10;
      }
      
      if (count > 6) {
        delay = 10;
      }
      
      if (count > 8) {
        delay = 10;
      }
      
      if (count > 10) {
        delay = 10;
      }
    } else {
      if (count > 3) {
        delay = 10;
      }
    }
    
    if (count < strings.length) {
      setTimeout(function() {
        return addLog();
      }, delay);
    } else {
      setTimeout(function() {
        delay = 1000;
        return createLog("ok");
      }, 1000);
    }
  }
  
  function createLog(type, index) {
    var row = document.createElement('div');
    
    var spanStatus = document.createElement('span');
    spanStatus.className = type;
    spanStatus.innerHTML = type.toUpperCase();
    
    var message = (index != null) 
                ? strings[index] 
                : 'kernel: Initializing...';

    if(index == null) 
    {
      var preloader = $('#preloader');
      jQuery(preloader).fadeOut("slow");
      jQuery("#main").fadeIn("slow");
    }
    
    var spanMessage = document.createElement('span');
    spanMessage.innerHTML = message;
    
    row.appendChild(spanStatus);
    row.appendChild(spanMessage);
    
    return row;
  }
  
  function goScrollToBottom() {
    $(document).scrollTop($(document).height()); 
  }
  
  addLog();
  
  