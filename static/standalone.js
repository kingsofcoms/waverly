// ios identifier
function isiOS() {
  var mobile = (navigator.userAgent.toLowerCase().includes('iphone') ||
                navigator.userAgent.toLowerCase().includes('ipad') ||
                navigator.userAgent.toLowerCase().includes('ipod'));
  return mobile;
}

function isMobile() {
  var mobile = (navigator.userAgent.toLowerCase().includes('iphone') ||
              navigator.userAgent.toLowerCase().includes('android') ||
              navigator.userAgent.toLowerCase().includes('ipad') ||
              navigator.userAgent.toLowerCase().includes('ipod'));
  return mobile;
}

// checking if the app was opened in an ios standalone mode
if (window.navigator.standalone){

  // changing header design to fit with status bar
  $('.header').css('height', '46px');
  $('.header').css('font-size', '18px');
  $('.header').css('padding-top', '18px');
  $('.logo').css('width', '30px');

}

// checking if the user is on a podcast page
if (window.location.href.includes('podcast')) {

  // add back option
  $( ".header" ).prepend( "<span id='back' style='vertical-align:middle;float:left;margin-left:20px;margin-right:-100px;text-transform:lowercase;font-size:24px;'>⬅️</span>" );
  var h = $( ".header" ).height() + 'px';
  $( "#back" ).css('line-height', h);
  $( ".header" ).css('cursor', 'pointer');
  $('.header').on("click", function(){
    window.history.back();
  });

// checking if the user on an account page
} else if ($('.post').length > 0) {

    // checking is user is on ios
    if (isiOS()) {
      // showing 'add to home screen' banner -- ⚠️ COMMENTED OUT ⚠️
      // $( "body" ).prepend( '<div class="homescreen"><img style="width:90vw;max-width:320px" src="/static/images/homescreen.png" alt=""></div>' );
      // $( "body" ).prepend( '<div class="black"></div>' );
      // $('.black').on("click", removeBlackAndMenu);
      // $('.homescreen').on("click", removeBlackAndMenu);
      //
      // $('.black').on("click", function(){
      //   $( ".homescreen" ).remove();
      //   $( ".black" ).remove();
      // });
      //
      // $('.homescreen').on("click", function(){
      //   $( ".homescreen" ).remove();
      //   $( ".black" ).remove();
      // });
    }

    // adding refresh option if there there are processing items
    if ($('.processing_item').length > 0) {
      // adding refresh option
      $('.header_title').text('🔄  tap here to refresh...');
      $('.header_title').css('text-transform', 'lowercase');
      $('.header_title').css('line-height', $('.header').css('height'));
      $('.logo').remove();
      $( ".header" ).css('cursor', 'pointer');
      $('.header').on("click", function(){
        if (location.href.includes('8000')) {
          location.href = location.href.split("8000")[1];
        } else {
          location.href = location.href.split(".com")[1];
        }
      });
    }
}


// menu items
function menuShareItems(){

  // checking if user is on a mobile device
  if (isMobile()) {

    // stop scrolling on the background content
    $('body').css('position', 'fixed');

  } else {
    $('body').css('overflow', 'hidden');
  }

  $('.menu_panel').css('overflow', 'scroll');
  $( ".menu_panel" ).prepend('<div class="menu_panel_title">Share Podcast</div><div id="share_01" class="menu_panel_item share">⤴️ Copy Link</div><a class="menu_panel_item share" href="whatsapp://send?text=' + window.location.href + '" data-action="share/whatsapp/share"><div id="share_02" class="menu_panel_item">⤴️ Share via WhatsApp</div></a>' );

}

// menu setup
if ($('.post').length === 0) {
  $('.menu_button').on("click", function (){

    // check status
    var url = window.location.href + 'voicestatus/';
    $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {

              // adding share items (if needed)
              menuShareItems();

              // split data based on coutry
              us_voices = [];
              uk_voices = [];

              for (var i=0; i<data.length; i++) {

                if (data[i].country === 'us') {
                  us_voices.push(data[i]);
                }

                if (data[i].country === 'uk') {
                  uk_voices.push(data[i]);
                }
              }

              // adding the general voices title
              $('.menu_panel').append('<div class="menu_panel_title" id="voices_title">Change Voice</div>');

              // adding the US title
              $('.menu_panel').append('<div class="menu_panel_title" id="us" style="font-size:18px;">🇺🇸</div>');

              var counter = 0;

              // adding US voices
              for (i=0; i<us_voices.length; i++) {

                // checking if this is the current voice_id
                // creating the voice title
                var title = us_voices[i].title;
                if (us_voices[i].status == $('#audio')[0].src){
                  title = title + '  ✅';
                }

                // checking status
                var status_text = "ready";
                var status_class = "voice_ready";
                if ( (us_voices[i].status === null) || (us_voices[i].status === '') ){
                  status_text = 'select to start process...';
                  status_class = 'voice_not';
                } else if (us_voices[i].status === 'http://0.com') {
                  status_text = '<span style="vertical-align: middle;font-size:14px;">🔄</span> processing...';
                  status_class = 'voice_not';
                }

                // appending the div
                $('.menu_panel').append('<div class="menu_panel_item" id="' + counter + '"><div class="voice_name">' + title +'</div><div class="status" id="' + status_class +'">'+ status_text +'</div></div>');
                counter++;

              }


              // adding the UK title
              $('.menu_panel').append('<div class="menu_panel_title" style="height:12px;margin-top: 0px;"></div>');
              $('.menu_panel').append('<div class="menu_panel_title" id="uk" style="font-size:18px;">🇬🇧</div>');

              // adding UK voices
              for (i=0; i<uk_voices.length; i++) {

                // checking if this is the current voice_id
                // creating the voice title
                title_uk = uk_voices[i].title;
                if (uk_voices[i].status == $('#audio')[0].src){
                  title_uk = title_uk + '  ✅';
                }

                // checking status
                var status_text_uk = "ready";
                var status_class_uk = "voice_ready";
                if ( (uk_voices[i].status === null) || (uk_voices[i].status === '') ){
                  status_text_uk = 'select to start process...';
                  status_class_uk = 'voice_not';
                } else if (uk_voices[i].status === 'http://0.com') {
                  status_text_uk = '🔄 processing...';
                  status_class_uk = 'voice_not';
                }

                // appending the div
                $('.menu_panel').append('<div class="menu_panel_item" id="' + counter + '"><div class="voice_name">' + title_uk +'</div><div class="status" id="' + status_class_uk +'">'+ status_text_uk +'</div></div>');
                counter++;
              }

              // adding padding at the bottom
              $('.menu_panel').append('<div class="menu_panel_title" style="height:12px;margin-top: 0px;"></div>');

              // adding event listeners
              menuActions(data);

              // showing the menu
              $( '<div class="black"></div>' ).insertAfter('.header');
              $( ".menu_panel" ).slideDown();
              $('.black').on("click", removeBlackAndMenu);

            }
          });

  });
}


// menu actions
function menuActions(data){
  $( '.menu_panel_item' ).on('click', function(){

    var id = $(this).attr('id');
    id = parseInt(id);

    if (isNaN(id) === false) {

      // checking status
      if ($(this).children('.status').text() === "select to start process...") {
        voice(id);
        removeBlackAndMenu();
        return;
      } else if ($(this).children('.status').text() === "ready") {
        $('#audio').attr('src',data[id].status);
        removeBlackAndMenu();
        return;
      } else {
        removeBlackAndMenu();
        return;
      }

    }

  });

  $( '#share_01' ).on('click', function(){

    // thanks to rphv from https://stackoverflow.com/questions/37308210/copy-current-url-button-javascript
    function copyTextToClipboard(text) {
    var textArea = document.createElement("textarea");

    // Place in top-left corner of screen regardless of scroll position.
    textArea.style.position = 'fixed';
    textArea.style.top = 0;
    textArea.style.left = 0;

    // Ensure it has a small width and height. Setting to 1px / 1em
    // doesn't work as this gives a negative w/h on some browsers.
    textArea.style.width = '2em';
    textArea.style.height = '2em';

    // We don't need padding, reducing the size if it does flash render.
    textArea.style.padding = 0;

    // Clean up any borders.
    textArea.style.border = 'none';
    textArea.style.outline = 'none';
    textArea.style.boxShadow = 'none';

    // Avoid flash of white box if rendered for any reason.
    textArea.style.background = 'transparent';


    textArea.value = text;

    document.body.appendChild(textArea);

    textArea.select();

    try {
      var successful = document.execCommand('copy');
      var msg = successful ? 'successful' : 'unsuccessful';
    } catch (err) {
    }

    document.body.removeChild(textArea);
    }

    function CopyLink() {
      copyTextToClipboard(location.href);
    }

    CopyLink();
    removeBlackAndMenu();

  });

  $( '#share_02' ).on('click', function(){
    removeBlackAndMenu();
  });
}

// change playback speed
$( '.playback_button' ).on('click', function(){

  // getting the audio element
  var audio = document.getElementById("audio");

  switch ($('.playback_button').text()) {

    case "⏩  x1.0":
      audio.playbackRate = 1.1;
      $('.playback_button').html("⏩  x1.1");
      console.log(audio.playbackRate);
      break;

    case "⏩  x1.1":
      audio.playbackRate = 1.2;
      $('.playback_button').html("⏩  x1.2");
      console.log(audio.playbackRate);
      break;

    case "⏩  x1.2":
      audio.playbackRate = 1.3;
      $('.playback_button').html("⏩  x1.3");
      console.log(audio.playbackRate);
      break;

    case "⏩  x1.3":
      audio.playbackRate = 1.4;
      $('.playback_button').html("⏩  x1.4");
      console.log(audio.playbackRate);
      break;

    case "⏩  x1.4":
      audio.playbackRate = 1.5;
      $('.playback_button').html("⏩  x1.5");
      console.log(audio.playbackRate);
      break;

    case "⏩  x1.5":
      audio.playbackRate = 1.6;
      $('.playback_button').html("⏩  x1.6");
      console.log(audio.playbackRate);
      break;

    case "⏩  x1.6":
      audio.playbackRate = 2.0;
      $('.playback_button').html("⏩  x2.0");
      console.log(audio.playbackRate);
      break;

    case "⏩  x2.0":
      audio.playbackRate = 1.0;
      $('.playback_button').html("⏩  x1.0");
      console.log(audio.playbackRate);
      break;

  }

});



// clear screen
function removeBlackAndMenu(){
  if ($('.menu_panel').length > 0) {
    $( ".menu_panel" ).slideUp('fast', function(){
      $('.menu_panel').empty();
    });
  }

  $( ".homescreen" ).remove();
  $( ".black" ).remove();
  $('body').css('overflow', 'auto');
  $('body').css('position', '');
  $('.menu_panel_item').off();
}


// debug
function debug(state){
  if (state === true) {
    $('body').click(function(e){
        console.log(e.target);
    });
  } else if (state === false) {
    $('body').off();
  }
}

// test for adding a voice
function voice(id) {

  // checking if the user is on a podcast page
  if (window.location.href.includes('podcast')) {
    var url = window.location.href + 'voiceadd/' + id;
    // console.log('☸️ this is the url: ' + url);
    $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {
              console.log('☸️ server says:');
              console.log(data);
            },
            error: function (err) {
              console.log('❗️ something went wrong..');
              console.log(err);
            }
          });
  }
  else {
    console.log('❗️ please navigate to a podcast page.');
  }

}



// test for getting voice statuses
function status() {

  // checking if the user is on a podcast page
  if (window.location.href.includes('podcast')) {
    var url = window.location.href + 'voicestatus/';
    console.log('☸️ checking statuses for: ' + url);
    $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {
              console.log('☸️ this is the return value:');
              console.log(data);
            },
            error: function (err) {
              console.log('❗️ something went wrong..');
              console.log(err);
            }
          });
  }
  else {
    console.log('❗️ please navigate to a podcast page.');
  }

}
