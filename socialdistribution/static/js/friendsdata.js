//function sendAJAX(method, url, message, session_id, callback) {
//  var xhr = new XMLHttpRequest();
//  xhr.open(method, url);
//  xhr.onreadystatechange = function(){
//    if (xhr.readyState==4) {
//      try {
//        if (xhr.status==200) {
//          if(callback) {
//            callback(JSON.parse(xhr.responseText));
//          }
//        }
//      }
//      catch(e) {
//        alert('Error: ' + e.name);
//      }
//    }
//  }
//  if(message) {
//    xhr.setHeader("Content-Type", "application/json");
//  }
//  xhr.send(JSON.stringify(message));
//}

function getCookieid() {
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0].trim() == "cookie_cmput404_author_id") {
      return gname[1];
      
    }
  }
  return "";
}

$(document).ready(function() {
                  
                  
                  function getCookieid() {
                  var cookies = document.cookie.split(";");
                  for(var i=0; i < cookies.length; i++) {
                  var gname = cookies[i].split("=");
                  if(gname[0].trim() == "cookie_cmput404_author_id") {
                  return gname[1];
                  
                  }
                  }
                  return "";
                  }
                  
                  var myauthorid = getCookieid();
                  //console.log(getCookieid());
                  
                  
                  //var myauthorlink = "/author/52ec225c39b24d6896ffba3176e71a37";// + myauthorid;
                  var myauthorlink = "/author/" + myauthorid;
                   //console.log(myauthorlink);
                  
                  sendAJAX("GET", myauthorlink, "", function(events) {
//                           console.log("this?");
//                           console.log(events);
//                           console.log(events.friends.length);
//                           console.log(events.friends[0]);
//                           console.log(">>>");
                    for(var i=0; i < events.friends.length; ++i) {
                           //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
                           var friendsTemplate = document.getElementById('friends-container');
                           friendsTemplate.content.querySelector("#friendid").textContent = events.friends[i].id;
                           friendsTemplate.content.querySelector("#friendhost").textContent = events.friends[i].host;
                           friendsTemplate.content.querySelector("#frienddisplayName").textContent = events.friends[i].displayName;
                           //console.log(events.friends[i].displayName);
                           friendsTemplate.content.querySelector("#friendurl").href = events.friends[i].url;
                           
                           var normalContent = document.getElementById('friendstab');
                           
                           var clonedTemplate = friendsTemplate.content.cloneNode(true);
                           normalContent.appendChild(clonedTemplate);
                           
                           }
                  });
                  
//                  sendAJAX("GET", "/getFriendRequests", "", function(events) {
//                           console.log(events);
//                           console.log(events.friendRequestList[0].fromAuthor_id);
//                           console.log(events.friendRequestList.length);
//                           for(var i=0; i < events.friendRequestList.length; ++i) {
//                           var requestTemplate = document.getElementById('request-container');
//                           //friendRequestList.content.querySelector("#friend-accept").value = "btn"+i;
//                           //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
//                           requestTemplate.content.querySelector("#thisusername").textContent = events.friendRequestList[i].fromAuthor_id;
//                           requestTemplate.content.querySelector("#profilepagelink").href = events.friendRequestList[i].url;
//                           requestTemplate.content.querySelector("#requesthost").href = events.friendRequestList[i].fromServerIP;
//                           requestTemplate.content.querySelector("#author2id").textContent = events.friendRequestList[i].fromAuthor_id;
//                           
//                           var normalContent = document.getElementById('frequest');
//                           
//                           var clonedTemplate = requestTemplate.content.cloneNode(true);
//                           normalContent.appendChild(clonedTemplate);
//                           //window.location.href="friendspage.html";
//                           }
//                           
//                           });

});


$("#reqtab").click(function(e) {
                   e.preventDefault();
                   sendAJAX("GET", "/getFriendRequests", "", function(events) {
                            console.log(events);
                            //console.log(events.friendRequestList[0].fromAuthor_id);
                            console.log(events.friendRequestList.length);
                            for(var i=0; i < events.friendRequestList.length; ++i) {
                            var requestTemplate = document.getElementById('request-container');
                            //friendRequestList.content.querySelector("#friend-accept").value = "btn"+i;
                            //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
                            requestTemplate.content.querySelector("#thisusername").textContent = events.friendRequestList[i].fromAuthor_id;
                            requestTemplate.content.querySelector("#profilepagelink").href = events.friendRequestList[i].url;
                            requestTemplate.content.querySelector("#requesthost").textContent = events.friendRequestList[i].fromServerIP;
                            //console.log(events.friendRequestList[i].fromServerIP);
                            requestTemplate.content.querySelector("#author2id").textContent = events.friendRequestList[i].fromAuthor_id;
                            
                            var normalContent = document.getElementById('frequest');
                            
                            var clonedTemplate = requestTemplate.content.cloneNode(true);
                            normalContent.appendChild(clonedTemplate);
                            }
                            
                            
                            });
                   document.getElementById("friendstab").innerHTML = "";
                    });

$("#fdtab").click(function(e) {
                  e.preventDefault();
                  function getCookieid() {
                  var cookies = document.cookie.split(";");
                  for(var i=0; i < cookies.length; i++) {
                  var gname = cookies[i].split("=");
                  if(gname[0].trim() == "cookie_cmput404_author_id") {
                  return gname[1];
                  
                  }
                  }
                  return "";
                  }
                  
                  var myauthorid = getCookieid();
                  var myauthorlink = "/author/" + myauthorid;
                  //console.log(myauthorlink);
                  
                  sendAJAX("GET", myauthorlink, "", function(events) {
//                           console.log("this?");
//                           console.log(events.friends.length);
//                           console.log(events.friends[0]);
//                           console.log(">>>");
                           for(var i=0; i < events.length; ++i) {
                           //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
                           var friendsTemplate = document.getElementById('friends-container');
                           friendsTemplate.content.querySelector("#friendid").textContent = events.friends[i].id;
                           friendsTemplate.content.querySelector("#friendhost").textContent = events.friends[i].host;
                           friendsTemplate.content.querySelector("#frienddisplayName").textContent = events.friends[i].displayName;
                           friendsTemplate.content.querySelector("#friendurl").href = events.friends[i].url;
                           
                           var normalContent = document.getElementById('friendstab');
                           
                           var clonedTemplate = friendsTemplate.content.cloneNode(true);
                           normalContent.appendChild(clonedTemplate);
                           
                           
                           
                           }
                           });
                  document.getElementById("frequest").innerHTML = "";
  });



//$("#unfriendauthor").click(function(e) {
//                           
//                   e.preventDefault();
function unfriendauthor() {
//                           var friendsTemplate = document.getElementById('friends-container');
//
//                           var normalContent = document.getElementById('friendstab');
//                           
//                           var clonedTemplate = friendsTemplate.content.cloneNode(true);
//                           normalContent.appendChild(clonedTemplate)
                           //console.log(document.getElementById("friendhost").href);
                   
                           var unfrienddata = {};
                           unfrienddata["author"] = document.getElementById("friendid").textContent;
                           unfrienddata["server_address"] = document.getElementById("friendhost").textContent;
                           
                           console.log(unfrienddata);
                           
                           sendAJAX("POST", "/unfriend", unfrienddata, function(response) {
                                    console.log(response);
                                    window.location.href="friendspage.html";
                                    
                                    });
                           
                           }


