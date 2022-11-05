var word;
var firstSentenceID;
var secondSentenceID;
var firstTSentenceID;
var secondTSentenceID;
var sentence1;
var sentence2;
var previous1;
var previous2;
var next1;
var next2;
var words;
var position1;
var position2;
var tutsentence1;
var tutsentence2;
var tutheader;
var tutorialIndex = 0;
var identifier1;
var identifier2;
//
//window.location.hostname
//window.location.port
//var host = "http://193.196.53.175";
var host = "https://durel.ims.uni-stuttgart.de";
//var host = "http://192.168.1.36";
//var host = "http://localhost"
//var boot_port = ":8080";
var boot_port ="";
var vis_port = ":8050";


$(function () {
    $('#myList a:last-child').tab('show')
  })

$("#upload-form").submit( function( e ) {

    showThrobber('throb-upload');
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var formData = new FormData ( $("#upload-form")[0] ) ;
    var url = form.attr('action');

    $.ajax({
           type: "POST",
           url: url,
           data: formData ,
           dataType: 'json',
           processData: false,
           contentType: false,
           success: function( data )
           {
                location.reload();

               /* When the upload is successful, discard the modal and update the view */
//               var p = document.getElementById('uploadFailed') ;
//               p.innerHTML =  "" ;
//               document.getElementById("upload-form").reset();
//               dismissUploadModal() ;
//               loadProjects() ;
//               setupUserProjectsListBox();
//               annotationLanguageChanged() ;

           },
           error: function ( answer ) {
                hideThrobber('throb-upload');
                res = JSON.parse(answer.responseText);
                var p = document.getElementById('uploadFailed') ;
                p.innerHTML =  uploadFailed + " " +  res.message ;
           }
         });
});

function deleteProject ( ) {

//    e.preventDefault(); // avoid to execute the actual submit of the form.

    showThrobber('throb-project')
    var form = $("#delete-form");
    var url = form.attr('action');

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(),
           success: function( data )
           {

               location.reload();
               /* When the upload is successful, update the view */
//               loadProjects() ;
//               setupUserProjectsListBox();
//               annotationLanguageChanged() ;
//               disableDeleteButton() ;
           }
         });
}


/* In the modal view for the tutorial, load the languages the tutorial is available */
function tutorialModalShowLanguages() {

    var languageTutorialSelect = document.getElementById( "selected_language" );
    var languageUploadSelect = document.getElementById( "upload-language" );

    var languages = JSON.parse ( localStorage [ 'languages'] ) ;

    var locale = getCurrentLocale () ;
    console.log(locale)

    for ( var i = 0 ; i < languages.length ; i++ ) {
        var languageOptionTutorial = document.createElement("option");
        var languageOptionUpload = document.createElement("option");
                            languageOptionTutorial.value = "?lang=" + languages[i].code;
                            languageOptionTutorial.text = languages[i].name;

                            languageOptionUpload.value = languages[i].code;
                            languageOptionUpload.text = languages[i].name;

                            if ( locale.code == languages[i].code ) {
                                languageOptionTutorial.selected = true;
                            }

                            languageTutorialSelect.appendChild(languageOptionTutorial);

                            languageUploadSelect.appendChild(languageOptionUpload);
    }
}

// loads list of words from database
function loadProjects() {
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");
    xhr.open("get", host + boot_port + "/loadProjects",
        false
    );

    xhr.send();

    if (xhr.status === 200) {
        projects = JSON.parse(xhr.responseText);
        localStorage.setItem( 'availableProjects', JSON.stringify( projects ) ) ;
    }
}



// loads header with selected word to annotate and fetches first sentence from database
function loadHeader() {
    //document.getElementById("header").innerHTML = "Bitte bewerten Sie den semantischen Bezug der beiden Verwendungen des markierten Wortes in den folgenden zwei Sätzen.";
    var xhr = new XMLHttpRequest();
//    console.log(localStorage.getItem("projectSelected"));
//    console.log(localStorage.getItem("word"));
    xhr.overrideMimeType("application/json");
    xhr.open("get", host + boot_port +  "/init" +
        "?word=" + localStorage.getItem("word") +
        "&project=" + localStorage.getItem("projectSelected"),
        false
    );

    xhr.send();

    if (xhr.status === 200) {
        res = JSON.parse(xhr.responseText);

        if ( res._status != "FAILED") {
                sentence1 = res._firstSentence.target.replace(/\[newline]/g, "<br>");
                sentence2 = res._secondSentence.target.replace(/\[newline]/g, "<br>");
                previous1 = res._firstSentence.previous.replace(/\[newline]/g, "<br>");
                previous2 = res._secondSentence.previous.replace(/\[newline]/g, "<br>");
                next1 = res._firstSentence.next.replace(/\[newline]/g, "<br>");
                next2 = res._secondSentence.next.replace(/\[newline]/g, "<br>");
                firstSentenceID = res._firstSentence.id;
                secondSentenceID = res._secondSentence.id;
                updateView();
        } else {
            alert("Sie haben alle Sätze für " + localStorage.getItem("word") + " annotiert. Bitte wählen Sie ein neues Wort!");
                    document.getElementById("sentence1").innerHTML = "-";
                    document.getElementById("sentence2").innerHTML = "-";

           window.location.href = '/menu'
        }



    }
}

//shows the two sentences in the annotation view
function updateView() {
    document.getElementById("sentence1").innerHTML = "<span style =\"color:rgb(170,170,170)\">" + previous1 + "</span> " + sentence1 + " <span style =\"color:rgb(170,170,170)\">"  + next1 + "</span>";
    document.getElementById("sentence2").innerHTML = "<span style =\"color:rgb(170,170,170)\">" + previous2 + "</span> " + sentence2 + " <span style =\"color:rgb(170,170,170)\">"  + next2 + "</span>";

}

//Processes the sentences to be annotated and the user's vote
function processVote() {
//    var vote = document.querySelector('input[name="vote"]:checked').id.split("_")[1];
    var vote = parseInt($("#rb-1").find(".rb-tab-active").attr("data-value"));
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");

   xhr.open("get", host + boot_port +  "/processVote" +
        "?vote=" + vote +
        "&firstSentenceID=" + firstSentenceID +
        "&secondSentenceID=" + secondSentenceID +
        "&word=" + localStorage.getItem("word") +
        "&project=" + localStorage.getItem("projectSelected"),
         false
         );

    xhr.send();

    if (xhr.status === 200) {
        res = JSON.parse(xhr.responseText);

        if ( res._status != "FAILED") {
                sentence1 = res._firstSentence.target;
                sentence2 = res._secondSentence.target;
                previous1 = res._firstSentence.previous;
                previous2 = res._secondSentence.previous;
                next1 = res._firstSentence.next;
                next2 = res._secondSentence.next;
                firstSentenceID = res._firstSentence.id;
                secondSentenceID = res._secondSentence.id;
                position1 = parseInt(res._firstSentence.pos);
                position2 = parseInt(res._secondSentence.pos);
        } else {
            alert("Sie haben alle Sätze für " + localStorage.getItem("word") + " annotiert. Bitte wählen Sie ein neues Wort!");
                    document.getElementById("sentence1").innerHTML = "-";
                    document.getElementById("sentence2").innerHTML = "-";

           window.location.href = '/menu'
        }

    }
    updateView();
    UnmarkAllAnn();
    markAnnotation(0);

}

//opens
function visualize() {


    showThrobber("throb-annotation");

    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");

    xhr.open("get", host + boot_port + "/visualize" +
        "?word=" + localStorage.getItem("word")  +
        "&project=" + localStorage.getItem("projectSelected"),
        true
    );

    xhr.onload = function () {
        if (xhr.status === 200) {

                res = JSON.parse(xhr.responseText);
                var win = window.open('about:blank', '_blank');
                win.document.write(res.message);
                win.focus();
                hideThrobber("throb-annotation");

            }
    };

    xhr.send();


}


//checks if the user has done the tutorial and shows the tutorial starting view if not
function checkTut() {

    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");

   xhr.open("get", host + boot_port + "/checktut",
        false
    );

    xhr.send();

    if (xhr.status === 200) {

        res = JSON.parse(xhr.responseText);
        if(res._tutdone == false || (res._tutdone == true && res._tutpassed == false)) {

            localStorage.setItem('tutorial_passed',false) ;
            document.getElementById("tutorialpane").className="card";
            document.getElementById("tutorialButton").className="active";
        } else {
            localStorage.setItem('tutorial_passed',true) ;
            document.getElementById("annotationpane").className="card";
            document.getElementById("tutItem").className="hinnen";
            document.getElementById("annotationButton").className="active";
        }
    }


    localStorage.setItem("project", "all");
    tutorialModalShowLanguages();
    loadProjects();

}


//loads the elements of the tutorial for the view
function startTut() {

    // Save the votes in a local map.
    var votes = {};
    localStorage.setItem("tutorialVotes", JSON.stringify(votes));

    tutorialIndex = 0;

    getNextTSentences(0);

    document.getElementById("sentence1").innerHTML = tutsentence1 ;
    document.getElementById("sentence2").innerHTML = tutsentence2 ;
    document.getElementById("header").innerHTML = tutheader + " - " +  msg;

}


//goes to the next tutorial sentence pair
function getNextTSentences(index) {
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");

    xhr.open("get", host + boot_port + "/tutorialSentence" +
        "?index=" + index,
        false
    );

    xhr.send();

    if (xhr.status === 200) {
        res = JSON.parse(xhr.responseText);
        tutsentence1 = "<span style =\"color:rgb(200,200,200)\">" + res._firstSentence.previous + "</span> " + res._firstSentence.target + " <span style =\"color:rgb(200,200,200)\">"  + res._firstSentence.next + "</span>";
        tutsentence2 = "<span style =\"color:rgb(200,200,200)\">" + res._secondSentence.previous + "</span> " + res._secondSentence.target + " <span style =\"color:rgb(200,200,200)\">"  + res._secondSentence.next + "</span>";
        tutheader = "Tutorial (" + ((tutorialIndex + 1)) + " / " + tutorial_length + ")";
        firstSentenceID = res._firstSentence.id;
        secondSentenceID = res._secondSentence.id;
        identifier1 = res._firstSentence.identifier;
        identifier2 = res._secondSentence.identifier;
    }
}


//Processes sentences and votes in the tutorial
function processTVote() {

//    var vote = document.querySelector('input[name="vote"]:checked').id.split("_")[1];
    var vote = parseInt($("#rb-1").find(".rb-tab-active").attr("data-value"));
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");

    console.log("id1: " + identifier1 + " - " + "id2: " + identifier2);

//false in der folgenden Zeile ist für Asynchron Aufruf, funktioniert momentan nicht anders, mögliche Lösung: https://stackoverflow.com/questions/4672691/ajax-responsetext-comes-back-as-undefined
//    xhr.open("get", host + boot_port + "/processTutorialVote" +
//        "?vote=" + vote +
//        "&index=" + tutorialIndex +
//        "&identifier_1=" + identifier1 +
//        "&identifier_2=" + identifier2,
//        false
//    );

    // Store the new annotation into the local map.
    var storedVotes = JSON.parse(localStorage.getItem("tutorialVotes"))
    storedVotes[tutorialIndex] = vote ;

    localStorage.setItem("tutorialVotes", JSON.stringify(storedVotes));

    console.log(storedVotes)



    tutorialIndex = tutorialIndex + 1 ;
    xhr.open("get", host + boot_port + "/tutorialSentence" +
        "?index=" + tutorialIndex,
        false
    );


    xhr.send();

    if (xhr.status === 200) {
        res = JSON.parse(xhr.responseText);
        if (res._firstSentence != null) {

//            tutorialIndex = tutorialIndex + 1;

            tutsentence1 = "<span style =\"color:rgb(200,200,200)\">" + res._firstSentence.previous + "</span> " + res._firstSentence.target + " <span style =\"color:rgb(200,200,200)\">" + res._firstSentence.next + "</span>";
            tutsentence2 = "<span style =\"color:rgb(200,200,200)\">" + res._secondSentence.previous + "</span> " + res._secondSentence.target + " <span style =\"color:rgb(200,200,200)\">" + res._secondSentence.next + "</span>";
            tutheader = "Tutorial (" + ((tutorialIndex + 1)) + " / " + tutorial_length + ")";

            document.getElementById("header").innerHTML = tutheader + " - " + msg;
            document.getElementById("sentence1").innerHTML = tutsentence1;
            document.getElementById("sentence2").innerHTML = tutsentence2;
            identifier1 = res._firstSentence.identifier;
            identifier2 = res._secondSentence.identifier;

        } else {
            processTutorial();
        }
    }
}

//checks if the user has passed at the end of the tutorial and reacts accordingly
function processTutorial() {
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");

    var storedVotes = localStorage.getItem("tutorialVotes");


    console.log(storedVotes)

    $.ajax({
         type : "POST",
         url :  "/processTutorial",
         contentType : "application/json",
         dataType : "json",
         data : storedVotes,
        success: function( res )
        {
                 if (res._tutpassed == false) {

                     var modal = document.getElementById("alert-tutorial-failed");
                     modal.style.display = "block";


                 } else {

                     var modal = document.getElementById("alert-tutorial-succeeded");
                     modal.style.display = "block";

                 }

        }
         });

////false in der folgenden Zeile ist für Asynchron Aufruf, funktioniert momentan nicht anders, mögliche Lösung: https://stackoverflow.com/questions/4672691/ajax-responsetext-comes-back-as-undefined
//    xhr.open("get", host + boot_port + "/processTutorial",
//        false
//    );
//
//    xhr.send();
//
//    if (xhr.status === 200) {
//        res = JSON.parse(xhr.responseText);
//
//        if (res._tutpassed == false) {
//
//            var modal = document.getElementById("alert-tutorial-failed");
//            modal.style.display = "block";
//
//
//        } else {
//
//            var modal = document.getElementById("alert-tutorial-succeeded");
//            modal.style.display = "block";
//
//        }
//
//    }
}


//closes the tutorial again
function closeTut() {
    var modal = document.getElementById("tutorial");
    modal.style.display = "none";
}


//handles user registration from the form
function register() {
    if (document.getElementById("usernameInput").value == "") {
        document.getElementById("signinMessage").innerHTML = "<span style=\"color:red\">Bitte geben Sie einen Benutzernamen ein.</span>";
        window.location.href = "#signinMessage";
        varreturn = false;
    // } else if (document.getElementById("nameInput").value == "") {
    //     document.getElementById("signinMessage").innerHTML = "<span style=\"color:red\">Bitte geben Sie einen Namen ein.</span>";
    //     window.location.href = "#signinMessage";
    //     varreturn = false;
    // } else if (document.getElementById("lastnameInput").value == "") {
    //     document.getElementById("signinMessage").innerHTML = "<span style=\"color:red\">Bitte geben Sie einen Nachnamen ein.</span>";
    //     window.location.href = "#signinMessage";
    //     varreturn = false;
    } else if (document.getElementById("passInput").value == "") {
        document.getElementById("signinMessage").innerHTML = "<span style=\"color:red\">Bitte geben Sie ein Passwort ein.</span>";
        window.location.href = "#signinMessage";
        varreturn = false;
    } else if (document.getElementById("emailInput").value == "") {
        document.getElementById("signinMessage").innerHTML = "<span style=\"color:red\">Bitte geben Sie eine Mailadresse ein.</span>";
        window.location.href = "#signinMessage";
        varreturn = false;
    // } else if (document.getElementById("institutionInput").value == "") {
    //     document.getElementById("signinMessage").innerHTML = "<span style=\"color:red\">Bitte geben Sie eine Institution ein.</span>";
    //     window.location.href = "#signinMessage";
    //     varreturn = false;
    } else if ( document.getElementById("passInput").value != document.getElementById("passAgain").value ) {
        document.getElementById("signinMessage").innerHTML = "<span style=\"color:red\">Die Passwörter stimmen nicht überein.</span>";
        document.getElementById("passInput").value = "" ;
        document.getElementById("passAgain").value = "" ;
        varreturn = false;
    } else if ( !document.getElementById("privacycheck").checked ) {

        document.getElementById("signinMessage").innerHTML = "<span style=\"color:red\">Die Datenschutzerklärung muss akzeptiert werden.</span>";
        window.location.href = "#signinMessage";
    } else {

        var xhr = new XMLHttpRequest();
        xhr.overrideMimeType("application/json");
        var username = document.getElementById("usernameInput").value;

        xhr.open("get", host + boot_port + "/checkuser" +
            "?username=" + username,
            false
        );

        xhr.send();
        let varreturn = false;
        if (xhr.status === 200) {
            res = JSON.parse(xhr.responseText);
            if (res._usernamestatus == false) {
                document.getElementById("signinMessage").innerHTML = "<span style=\"color:red\">Dieser Benutzername wird bereits verwendet. Bitte wählen Sie einen anderen Benutzernamen.</span>";
                window.location.href = "#signinMessage";
                varreturn = false;
            } else {
                //alert("Ihr Benutzer wurde registriert. Um Ihren Benutzer freizuschaltenw enden Sie sich bitte an dominik.schlechtweg@ims.uni-stuttgart.de..")
                window.location.href = "/";
                varreturn = true;
            }
        }
    }
    return varreturn;

}

function checkWord() {
   // alert(localStorage.getItem("word"));
    if (localStorage.getItem("word") == "" || localStorage.getItem("word") == null) {
        alert("Bitte wählen Sie ein Wort aus!");
        return false;
    } else {
        return true;
    }
}



/* When the user clicks on the language button,
toggle between hiding and showing the dropdown content */
function showLanguages() {
  document.getElementById("languageDropDown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
//window.onclick = function(event) {
//  if (!event.target.matches('.dropbtn')) {
//    var dropdowns = document.getElementsByClassName("dropdown-content");
//    var i;
//    for (i = 0; i < dropdowns.length; i++) {
//      var openDropdown = dropdowns[i];
//      if (openDropdown.classList.contains('show')) {
//        openDropdown.classList.remove('show');
//      }
//    }
//  }
//}

/* Request the available languages, and cache them into localStorage. */
function requestLanguages() {
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");
    xhr.open("get", host + boot_port + "/getLanguages",
            false
        );

    xhr.send();
    if (xhr.status === 200) {
        /* cache the list of available languages. */
        localStorage.setItem('languages', JSON.stringify( JSON.parse( xhr.responseText ) ) ) ;
    }
}

/* Request and return the current locale. */
function getCurrentLocale() {
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");
    xhr.open("get", host + boot_port + "/getLocale",
            false
        );

    xhr.send();
    if (xhr.status === 200) {
        return JSON.parse(xhr.responseText) ;
    }
}

/* Populates the list of available languages. */
function populateLanguages() {

    /* If languages are not cached, get them from the server side. */
    if ( localStorage.getItem("languages") == null ) {
        requestLanguages() ;
    }

    var languageDropDown = document.getElementById("languageDropDown") ;

    var languages = JSON.parse ( localStorage["languages"] ) ;
    /* Iterate the languages and create the corresponding link. */
    for ( var i = 0 ; i < languages.length ; i++ ) {
        var languageLabel = "<a href=\"?lang="+languages[i].code+"\">"+languages[i].name+"</a>" ;
        languageDropDown.innerHTML += languageLabel ;
    }

}

/* Fills the language of the annotation listbox */
function setupAnnotationListbox () {
    var languageSelect = document.getElementById("lang-select") ;

    var languages = JSON.parse ( localStorage["languages"] ) ;

    for ( var i = 0 ; i < languages.length ; i++ ) {
        var languageOption = "<option class=\"nonLeafOption\" value=\""+languages[i].code+"\">"+languages[i].name+"</option>" ;
        languageSelect.innerHTML += languageOption ;
    }

}

function setupUserProjectsListBox() {

   var userProjectSelect = document.getElementById("user-projects") ;
   resetListBox ( userProjectSelect ) ;

    var allProjects = JSON.parse ( localStorage["availableProjects"] ) ;

    for ( var i = 0 ; i < allProjects.length ; i++ ) {
            var languageOption = "<option class=\"concentricCirleOption\" value=\""+allProjects[i].name+"\">"+allProjects[i].name+"</option>" ;
                    userProjectSelect.innerHTML += languageOption ;
    }
}

/* Reacts to the change of language, filling the available projects */
function annotationLanguageChanged ( ) {

    var e = document.getElementById("lang-select") ;
    var langCode = e.options[e.selectedIndex].value ;

    resetListBox( document.getElementById("word-select") ) ;


    showProjectsListbox ( langCode ) ;

}

/* Reacts to the change of project, filling the available words */
function annotationProjectChanged () {

    var e = document.getElementById("project-select") ;
    var projectName = e.options[e.selectedIndex].value ;
    showWordsListbox ( projectName ) ;
}

/* Fills up the project listbox */
function showProjectsListbox( langCode ) {

    var projects = JSON.parse ( localStorage["availableProjects"] ) ;
    var select = document.getElementById("project-select") ;
    resetListBox ( select ) ;

    for (var i = 0; i<projects.length; i++) {
        if (projects [i].langCode == langCode ) {
            var o = document.createElement("option");
            o.value = projects[i].name;
            o.text = projects[i].name;
            o.className = 'nonLeafOption' ;
            select.appendChild(o);
        }
    }
    showSliderIfNecessary(select, projects.length) ;

}
/* Fills up the word listbox */
function showWordsListbox( projectName ) {

    var xhr = new XMLHttpRequest();
        xhr.overrideMimeType("application/json");
        xhr.open("get", host + boot_port + "/loadWords?project=" + projectName,
            false
        );

        xhr.send();

        if (xhr.status === 200) {
            res = JSON.parse(xhr.responseText);

            words = res._words;
            var select = document.getElementById("word-select") ;
            resetListBox ( select ) ;

            for (var i = 0; i<words.length; i++) {
                    var o = document.createElement("option");
                    o.value = words[i];
                    o.text = words[i];
                    o.className = 'leafOption' ;
                    select.appendChild(o);
            }

            showSliderIfNecessary(select, words.length) ;
        }
}

/* Empties a given listbox */
function resetListBox( selectElement ) {

    for ( var i = selectElement.options.length-1; i > 0; i-- ) {
        selectElement.remove(i) ;

    }

    selectElement.style.overflow = "hidden";
    disableAnnotationButtons();
}

/* Shows the slider of a listbox if the number of options exceed the number of rows */
function showSliderIfNecessary ( selectElement, numOptions ) {
    if ( numOptions > selectElement.size ) {
        selectElement.style.overflow = "scroll";
    } else {
        selectElement.style.overflow = "hidden";
    }

}

/* Save the selected word into the database */
function wordSelected () {
    var e = document.getElementById("word-select") ;
    localStorage.setItem("word", e.options[e.selectedIndex].value) ;
}

function projectSelected () {
    var e = document.getElementById("project-select") ;
    localStorage.setItem("projectSelected", e.options[e.selectedIndex].value) ;
}


/* Enables and disables the annotation and the visualization buttons */
function enableAnnotationButtons () {
    if ( localStorage.getItem('tutorial_passed') === 'true' ) {
        document.getElementById("beginAnnotation").className = '' ;
        document.getElementById("linkBeginAnnotation").className = '' ;
    }

    document.getElementById("beginVisualization").className = '' ;
}

function disableAnnotationButtons () {
    document.getElementById("beginAnnotation").className = 'disabled-link' ;
    document.getElementById("linkBeginAnnotation").className = 'disabled-link' ;
    document.getElementById("beginVisualization").className = 'disabled-link' ;
}

function enableDeleteButton () {
    document.getElementById("delete").className = 'red-button' ;
}

function enableUpdateButton () {
    document.getElementById("update").className = 'button' ;
}

function enableDownloadButton () {
    document.getElementById("download").className = 'button' ;
}

function disableDeleteButton () {
    document.getElementById("delete").className = 'disabled-link red-button' ;
}

function showUploadModal () {
    document.getElementById("upload-modal").style.display = "block";
}

function dismissUploadModal () {
    document.getElementById("upload-modal").style.display = "";
}

function getUserName () {
//    if ( localStorage.getItem("username") == null ) {
            requestUserName() ;
//    }
    return localStorage.getItem("username") ;
}


/* Request the available languages, and cache them into localStorage. */
function requestUserName() {
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");
        xhr.open("get", host + boot_port + "/myusername",
            false
        );

    xhr.send();
    if (xhr.status === 200) {
        localStorage.setItem('username',  xhr.responseText) ;
    }
}


function reloadMenu() {
    window.location.href = "/menu";
    return true;
}


function selectCard (clicked_id) {
    console.log(clicked_id);
    var cards = document.getElementsByClassName("card") ;
    for ( var i = 0 ; i < cards.length; ++i ) {
        cards[i].className = "card hinnen";
    }

    var buttons = document.getElementsByClassName("active") ;
    for ( var i = 0 ; i < buttons.length; ++i ) {
            buttons[i].className = "";
        }

    document.getElementById(clicked_id).className = "active";



    var pane = document.getElementById(clicked_id.replace('Button','pane'));

    pane.className = pane.className.replace('hinnen','');
}


function updateProject() {

    console.log(yourProjects) ;
}

function showProjectUpdatePane(list) {

    var projectname = list.options[list.selectedIndex].value ;

    for ( var i = 0 ; i < yourProjects.length; i++ ) {

        if ( yourProjects [i].name == projectname ) {

            document.getElementById("projectNameUpdate").value = yourProjects [i].name ;
            document.getElementById("projectNameUpdate").disabled = false ;



            var languages = JSON.parse ( localStorage["languages"] ) ;

            var select = document.getElementById("update-language") ;
            removeOptions(select) ;
            select.disabled = false ;
            for ( var j = 0 ; j < languages.length ; j++ ) {
                    var languageOptionUpdate = document.createElement("option");
                    languageOptionUpdate.value = languages[j].code;
                    languageOptionUpdate.text = languages[j].name;

                    if ( yourProjects [i].langCode == languages[j].code ) {
                        languageOptionUpdate.selected = true;
                    }

                    select.appendChild(languageOptionUpdate);
            }



            document.getElementById("update-visibility").disabled = false ;


            console.log(yourProjects [i].visibility);
            if ( yourProjects [i].visibility == true ) {
                disableGrantAccessCheckboxes () ;
                document.getElementById("publicProject").selected = true ;
                document.getElementById("privateProject").selected = false ;

            } else {
                document.getElementById("privateProject").selected = true ;
                document.getElementById("publicProject").selected = false ;
                enableGrantAccessCheckboxes( yourProjects [i] ) ;
            }

            break;

        }
    }

    enableDeleteButton();
    enableUpdateButton();
    enableDownloadButton();



}


function disableGrantAccessCheckboxes ( ) {
    var cbs = document.getElementsByName("accessCheckbox") ;

    for ( var i = 0 ; i < cbs.length ; i++ ) {

        cbs[i].checked = false ;
        cbs[i].disabled = true ;
    }
}

function enableGrantAccessCheckboxes ( project ) {

    var cbs = document.getElementsByName("accessCheckbox") ;

    for ( var i = 0 ; i < cbs.length ; i++ ) {

        cbs[i].checked = false ;
        cbs[i].disabled = false ;
    }

    for ( var i = 0 ; i < project.grants.length ; i++ ) {
        var li =  document.getElementById("cbsid:"+project.grants[i]);

        // This is only for ADMIN. Their user might not appear in the list, but they might have been granted access anyways.
        if (li != null) {
            li.checked = true ;
        }

    }

}

function enableGrantAccessCheckboxesEmpty ( ) {

    var cbs = document.getElementsByName("accessCheckbox") ;

    for ( var i = 0 ; i < cbs.length ; i++ ) {

        cbs[i].checked = false ;
        cbs[i].disabled = false ;
    }

}


function visibilityChanged ( list ) {

    var visibility = list.options[list.selectedIndex].value ;

    if ( visibility == "private" ) {

        enableGrantAccessCheckboxesEmpty (  ) ;
    } else {

        disableGrantAccessCheckboxes ( ) ;
    }



}


function updateProject ( ) {

//    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $("#update-form");
    var url = form.attr('action');

    var dataForm = form.serializeArray();

    var list = document.getElementById("user-projects")
    var projectname = list.options[list.selectedIndex].value ;
    console.log(projectname);
    dataForm.push({name: 'project', value: projectname });

//    var paragraphCount = document.evaluate( '//*[@name="accessCheckbox" and not(not(@checked))]', document, null, XPathResult.ANY_TYPE, null );

//    var thisHeading = paragraphCount.iterateNext();
//    var thisHeading = paragraphCount.iterateNext();
//    console.log(thisHeading);

    var cbs = document.getElementsByName("accessCheckbox") ;

    var arr = [] ;
    for ( var i = 0 ; i < cbs.length ; i++ ) {


        if ( cbs[i].checked ) {

            arr.push (cbs[i].value) ;
        }
//        dataForm.push({name: 'project', value: projectname });
//        cbs[i].checked = false ;
//        cbs[i].disabled = false ;
    }

    console.log(arr);

    dataForm.push({name: 'grants', value: arr });


    $.ajax({
           type: "POST",
           url: url,
           data: dataForm,
           success: function( data )
           {

            location.reload();
               /* When the upload is successful, update the view */
//               loadProjects() ;
//               setupUserProjectsListBox();
//               annotationLanguageChanged() ;
//               disableDeleteButton() ;
           }
         });
}


function removeOptions(selectElement) {
   var i, L = selectElement.options.length - 1;
   for(i = L; i >= 0; i--) {
      selectElement.remove(i);
   }
}



function myFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("usersList");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("label")[0];
        txtValue = a.innerHTML ;
        console.log(txtValue);
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}


function closeModalMessage( ) {

    var window = document.getElementById("modal-message");
    window.style.display='none';
}

function showModalMessage( title, content, buttonName, buttonOp=closeModalMessage, link=s ) {


    var window = document.getElementById("modal-message");
    window.style.display='block';


    document.getElementById("message-title").innerHTML=title;
    document.getElementById("message-content").innerHTML=content;
    document.getElementById("message-link").href=link;
    document.getElementById("message-button").innerHTML=buttonName;
    document.getElementById("message-title").onclick=buttonOp;


}

function showThrobber(throbberID) {
    var element = document.getElementById(throbberID);
    element.classList.remove("hinnen");
}

function hideThrobber(throbberID) {
    var element = document.getElementById(throbberID);
        element.classList.add("hinnen");
}

function downloadProject() {

    showThrobber('throb-project');

    var form = $("#update-form");
    var projname = $('select[name=projectName] option').filter(':selected').val();

    var win = window.open("/download?projectName="+projname);
    win.blur();
    window.focus();
    var timer = setInterval(function() {
            if (win.closed) {
                clearInterval(timer);
                hideThrobber('throb-project');
            }
        }, 300);


//    window.location.href="/download?projectName="+projname;




}