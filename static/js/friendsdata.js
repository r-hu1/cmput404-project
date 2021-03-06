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
  sendAJAX("GET", "/checkUnfriended", "", function(response) {
                           //  console.log("clicked");
           
  var myauthorid = getCookieid();
  var myauthorlink = "/author/" + myauthorid;
//                  console.log(myauthorlink);
  sendAJAX("GET", myauthorlink, "", function(events) {
    for(var i=0; i < events.friends.length; ++i) {
      //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
      var friendsTemplate = document.getElementById('friends-container');
      friendsTemplate.content.querySelector(".friendid").textContent = events.friends[i].id;
      friendsTemplate.content.querySelector(".friendhost").textContent = events.friends[i].host;
      friendsTemplate.content.querySelector(".frienddisplayName").textContent = events.friends[i].displayName;
//        console.log(events.friends[i].displayName);
      friendsTemplate.content.querySelector(".friendurl").href = events.friends[i].url;

      document.cookie = "request_author_id="+events.friends[i].id;

      //friendsTemplate.content.querySelector(".friendp1link").href = "authorpage.html";
      var friendprofileBtn = friendsTemplate.content.querySelector(".friendp1link");
      friendprofileBtn.setAttribute("thisuserid", events.friends[i].id);
      //friendsTemplate.content.querySelector("#friendp2link").href = "authorpage.html";

      var unfriendbtn = friendsTemplate.content.querySelector(".unfriendauthor");
      unfriendbtn.name = events.friends[i].id;
      unfriendbtn.setAttribute("friendhostname", events.friends[i].host);

      var normalContent = document.getElementById('friendstab');

      var clonedTemplate = friendsTemplate.content.cloneNode(true);
      normalContent.appendChild(clonedTemplate);

    }

    $(".friendp1link").click(function (e) {

       e.preventDefault();

       localStorage.setItem("fetch-author-id", $(this).attr("thisuserid"));
       window.location.href = "authorpage.html";

    });

    // Set which unfriend the user clicked
    $(".unfriendauthor").click(function (e) {

       e.preventDefault();

       localStorage.setItem("fetch-unfriend-id", $(this).attr("name"));
       localStorage.setItem("fetch-unfriend-host", $(this).attr("friendhostname"));
       unfriendauthor();

    });
  });
  });
});


$("#reqtab").click(function(e) {
  e.preventDefault();
  document.getElementById("frequest").innerHTML = "";

  sendAJAX("GET", "/getFriendRequests", "", function(events) {
    for(var i=0; i < events.friendRequestList.length; ++i) {
    var requestTemplate = document.getElementById('request-container');
    requestTemplate.content.querySelector("#thisusername").textContent = events.friendRequestList[i].fromAuthorDisplayName;
    requestTemplate.content.querySelector("#profilepagelink").href = events.friendRequestList[i].url;
    requestTemplate.content.querySelector("#requesthost").textContent = events.friendRequestList[i].fromServerIP;
    //console.log(events.friendRequestList[i].fromServerIP);
    requestTemplate.content.querySelector("#author2id").textContent = events.friendRequestList[i].fromAuthor_id;

    var rpBtn = requestTemplate.content.querySelector(".reqprofile");
    rpBtn.setAttribute("reqprofileid", events.friendRequestList[i].fromAuthor_id);

    var addingfriendbtn = requestTemplate.content.querySelector(".friend-accept");
    addingfriendbtn.name = events.friendRequestList[i].fromAuthor_id;
    addingfriendbtn.setAttribute("friendhostserver", events.friendRequestList[i].fromServerIP);
    addingfriendbtn.setAttribute("addname", events.friendRequestList[i].fromAuthorDisplayName);

    var normalContent = document.getElementById('frequest');

    var clonedTemplate = requestTemplate.content.cloneNode(true);
    normalContent.appendChild(clonedTemplate);

    // bind the buttons
    $(".friend-accept").click(function (e) {

      e.preventDefault();

      localStorage.setItem("fetch-addfriend-id", $(this).attr("name"));
      localStorage.setItem("fetch-addfriend-name", $(this).attr("addname"));

      localStorage.setItem("fetch-addfriend-host", $(this).attr("friendhostserver"));
      //acceptfriend();
      var acceptfrienddata = {};
      acceptfrienddata["author"] = localStorage.getItem("fetch-addfriend-id");
      acceptfrienddata["server_address"] = localStorage.getItem("fetch-addfriend-host");

      // touqir wants these
      acceptfrienddata["author1_name"] = localStorage.getItem("fetch-addfriend-name");
      acceptfrienddata["author2_name"] = localStorage.getItem("display_name");

      sendAJAX("POST", "/acceptFriendRequest", acceptfrienddata, function(response) {
//                   console.log(response);
        window.location.href="friendspage.html";
      });
    });

   $(".reqprofile").click(function(e) {
       e.preventDefault();
       // set this for authorpage to use
       localStorage.setItem("fetch-author-id", $(this).attr("reqprofileid"));
       //console.log("clicked");
       window.location.href = "authorpage.html";
    });

}

  });
  // clear friends tab so the template does not duplicate
  document.getElementById("friendstab").innerHTML = "";
});


// accept the friend request from author
function acceptfriend() {

  var acceptfrienddata = {};
  acceptfrienddata["author"] = localStorage.getItem("fetch-addfriend-id");
  acceptfrienddata["server_address"] = localStorage.getItem("fetch-addfriend-host");

  // touqir wants these
  acceptfrienddata["author1_name"] = localStorage.getItem("fetch-addfriend-name");
  acceptfrienddata["author2_name"] = localStorage.getItem("display_name");

//  console.log(acceptfrienddata);
  sendAJAX("POST", "/acceptFriendRequest", acceptfrienddata, function(response) {
//    console.log(response);
    window.location.href="friendspage.html";
  });
}


// Do this when the user click on the friend tab
$("#fdtab").click(function(e) {
  e.preventDefault();
  document.getElementById("friendstab").innerHTML = "";

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
  sendAJAX("GET", "/checkUnfriended", "", function(response) {
  var myauthorid = getCookieid();
  var myauthorlink = "/author/" + myauthorid;
    //                  console.log(myauthorlink);
  sendAJAX("GET", myauthorlink, "", function(events) {
     //      console.log(events.friends);
    for(var i=0; i < events.friends.length; ++i) {
       //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
       var friendsTemplate = document.getElementById('friends-container');
       friendsTemplate.content.querySelector(".friendid").textContent = events.friends[i].id;
       friendsTemplate.content.querySelector(".friendhost").textContent = events.friends[i].host;
       friendsTemplate.content.querySelector(".frienddisplayName").textContent = events.friends[i].displayName;
       //        console.log(events.friends[i].displayName);
       friendsTemplate.content.querySelector(".friendurl").href = events.friends[i].url;

       document.cookie = "request_author_id="+events.friends[i].id;

       //friendsTemplate.content.querySelector(".friendp1link").href = "authorpage.html";
       var friendprofileBtn = friendsTemplate.content.querySelector(".friendp1link");
       friendprofileBtn.setAttribute("thisuserid", events.friends[i].id);
       //friendsTemplate.content.querySelector("#friendp2link").href = "authorpage.html";

       var unfriendbtn = friendsTemplate.content.querySelector(".unfriendauthor");
       unfriendbtn.name = events.friends[i].id;
       unfriendbtn.setAttribute("friendhostname", events.friends[i].host);

       var normalContent = document.getElementById('friendstab');

       var clonedTemplate = friendsTemplate.content.cloneNode(true);
       normalContent.appendChild(clonedTemplate);
    }

       $(".friendp1link").click(function (e) {

          e.preventDefault();

          localStorage.setItem("fetch-author-id", $(this).attr("thisuserid"));
          window.location.href = "authorpage.html";


        });

       // Set which unfriend the user clicked
       $(".unfriendauthor").click(function (e) {

          e.preventDefault();

          localStorage.setItem("fetch-unfriend-id", $(this).attr("name"));
          localStorage.setItem("fetch-unfriend-host", $(this).attr("friendhostname"));
          unfriendauthor();

          });
       });
    });

  document.getElementById("frequest").innerHTML = "";
});


// unfriend this author from the friend list of user
function unfriendauthor() {

  var unfrienddata = {};
  //unfrienddata["author"] = document.getElementById("friendid").textContent;
  unfrienddata["author"] = localStorage.getItem("fetch-unfriend-id");
  unfrienddata["server_address"] = localStorage.getItem("fetch-unfriend-host");

  // console.log(unfrienddata);

  sendAJAX("POST", "/unFriend", unfrienddata, function(response) {
//    console.log(response);
    window.location.href="friendspage.html";
  });

}
//
//$("#refresh").click(function (e) {
//  e.preventDefault();
//  sendAJAX("GET", "/checkUnfriended", "", function(response) {
//          //  console.log("clicked");
//  });
//})
