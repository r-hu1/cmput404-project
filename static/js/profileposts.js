function getCookieid() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0].trim() == "cookie_cmput404_author_id") {
      return gname[1];
    }
  }
  return "";
}

function getCookiehost() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0] == "cookie_cmput404_author_host") {
      return gname[1];
    }
  }
  return "";
}

function getFriendcookieid() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0] == "request_author_id") {
      return gname[1];
    }
  }
  return "";
}

// clear posts tab when user is on profile tab
$("#profiletab").click(function(e) {
  e.preventDefault();
  document.getElementById("posts").innerHTML = "";
});

// When user click post tab
$("#posttab").click(function(e) {
  e.preventDefault();
  document.getElementById("posts").innerHTML = "";

  var myauthorid = getCookieid();

  var myprofileposts = "/author/" + myauthorid + "/posts?size=50";

  var postList = document.getElementById("posts");
  var postTemplate = document.getElementById("post-container");
  // page=<Page_No>&size=<Page_Zize>
  sendAJAX("GET", myprofileposts, "", function(results) {
    for(var i=0; i < results.posts.length; ++i) {
       // fill the container with details
       postTemplate.content.querySelector(".post-title").textContent = results.posts[i].title;
       //console.log(results.posts[i].title);
       postTemplate.content.querySelector(".post-description").textContent = results.posts[i].description;
  //           console.log(results.posts[i].description);
       postTemplate.content.querySelector(".post-author").textContent = results.posts[i].author.displayName;

       if(results.posts[i].contentType == "text/markdown" || results.posts[i].contentType == "text/x-markdown") {
         var cmreader = new commonmark.Parser();
         var writer = new commonmark.HtmlRenderer();
         var parsed = cmreader.parse(results.posts[i].content); // parsed is a 'Node' tree
         // transform parsed if you like...
         var commonmarkresult = writer.render(parsed);
         postTemplate.content.querySelector(".post-content").innerHTML = commonmarkresult;
       }
       else {
         postTemplate.content.querySelector(".post-content").innerHTML = results.posts[i].content;
       }

       if (results.posts[i].count > 0) {
         postTemplate.content.querySelector(".comments-num").textContent = "("+results.posts[i].count+")";
       } else {
         postTemplate.content.querySelector(".comments-num").textContent = "";
       }
       // attach data to the links so it can be referenced when clicked
       var authorBtn = postTemplate.content.querySelector(".post-author");
       authorBtn.setAttribute("post-author-id", results.posts[i].author.id);

       var commentsBtn = postTemplate.content.querySelector(".comments");
       commentsBtn.setAttribute("post-id", results.posts[i].id);

       var deletepostBtn = postTemplate.content.querySelector(".deletepost");
       deletepostBtn.setAttribute("delete-post-id", results.posts[i].id);

       var clone = document.importNode(postTemplate.content, true);
       postList.appendChild(clone);
     }

     // bind the onclick to set post host and id in localStorage
     // and link the user to the post's page
     $(".comments").click(function(e) {
       e.preventDefault();
       // set this for later
        // localStorage.setItem("fetch-post-host", $(this).data("post-host"));
       localStorage.setItem("fetch-post-id", $(this).attr("post-id"));
       window.location.href = "post.html";
    });

     // bind the onclick to set author id in localStorage
     // and link the user to the author's profile
     $(".post-author-url").click(function(e) {
       e.preventDefault();
       // set this for authorpage to use
       localStorage.setItem("fetch-author-id", $(this).attr("post-author-id"));
       window.location.href= "authorpage.html";
       });

     //$("#deletepost").click(function(e) {
     $(".deletepost").on('click', (function(e) {
        e.preventDefault();

        localStorage.setItem("delete-post-id", $(this).attr("delete-post-id"))
        deletepost();
        location.reload();
     }));
   });
});


// delete the post
function deletepost() {
  var thispostid = localStorage.getItem("delete-post-id");
  var deletepostlink = "/posts/" + thispostid;

  sendAJAX("DELETE", deletepostlink, "", function(result) {
//           console.log(result);
           //location.reload();
           });
}
