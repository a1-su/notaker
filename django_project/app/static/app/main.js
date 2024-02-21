$('#suggest-button-loader').hide();
$('#suggest-button-text')[0].innerText = 'Suggest';

//$('.source-section-div').children().addClass('source-section');

$(function () {
  $('[data-toggle="popover"]').popover()
})

function getSelectionText() {
    var text = "";
    if (window.getSelection) {
        text = window.getSelection().toString();
    } else if (document.selection && document.selection.type != "Control") {
        text = document.selection.createRange().text;
    }
    return text;
}

tinymce.init({
        selector: 'textarea',
        plugins: 'anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount',
        toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | align lineheight | tinycomments | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
        tinycomments_mode: 'embedded',
        tinycomments_author: 'Author name',
        mergetags_list: [
          { value: 'First.Name', title: 'First Name' },
          { value: 'Email', title: 'Email' },
        ],
        ai_request: (request, respondWith) => respondWith.string(() => Promise.reject("See docs to implement AI Assistant")),
      });

//$("#note-form-content").change(function () {
//        var content = $(this).val();
//        $.ajaxSetup({
//            headers: {
//                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
//            }
//        });
//        $.ajax({
//        url: 'autosuggest/',
//        method: 'POST',
//        data: {
//          'content': content
//        },
//        dataType: 'json',
//        success: function (data) {
//          alert(data.suggestion)
//        }
//      });
//    });

function ajax_summarize(section){
    if (section.length >= 150){
        $('#suggest-button').popover('hide');
        index = $("#note-form-content")[0].selectionStart
        $.ajaxSetup({
          beforeSend: function() {
             $('#suggest-button-loader').show();
             $('#suggest-button').attr("disabled", true);
             $('#suggest-button-text')[0].innerText = 'Loading';
          },
          complete: function(){
             $('#suggest-button-loader').hide();
             $('#suggest-button').attr("disabled", false);
             $('#suggest-button-text')[0].innerText = 'Suggest';
          },
          success: function() {}
        });
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });
        $.ajax({
        url: 'suggest/',
        method: 'POST',
        data: {
          'section': section
        },
        dataType: 'json',
        success: function (data) {
            console.log(data.suggestion)
            console.log($("#note-form-content")[0].innerText)
            content = $("#note-form-content")[0].innerText
//            $("#note-form-content")[0].innerText = content.slice(0, index) + data.suggestion + content.slice(index)
//            console.log($("#note-form-content")[0].innerText)
            tinymce.activeEditor.execCommand('mceInsertContent', false, data.suggestion);
        }
      });
    } else {
//        alert('Selected text too short')
        $('#suggest-button').popover('show');
        setTimeout(() => {
          $('#suggest-button').popover('hide');
        }, 1000);
    }
}


$('.source-section').click(function(){
    section = $(this)[0].innerText
    if (getSelection().type == 'Caret'){
        ajax_summarize(section)
    } else {
        $('#suggest-button').popover('hide');
    }
});


$('#suggest-button').click(function(){
    section = getSelectionText()
    ajax_summarize(section)
});


$('#save-button').click(function(){
    var title = $("#note-form-title").val();
//    var content = $("#note-form-content").val();
    var content = tinymce.activeEditor.getContent();
//    var content = tinymce.activeEditor.getContent({format : 'raw'});
    console.log(content)
    $.ajaxSetup({
      beforeSend: function() {
      },
      complete: function(){
      },
      success: function() {}
    });
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
    $.ajax({
    url: 'save/',
    method: 'POST',
    data: {
        'csrfmiddlewaretoken' : document.querySelector('[name=csrfmiddlewaretoken]').value,
        'title': title,
        'content': content,
    },
    dataType: 'json',
    success: function (data) {
//      alert(data.message);
        $('#save-button').popover('show');
        setTimeout(() => {
          $('#save-button').popover('hide');
        }, 1000);
    }
  });
});


$('.source-dropdown-item').click(function(){
    $("#source-form-title")[0].innerText = $(this)[0].attributes.value.value
    var drpdwn = $(this).data("select-dropdown");
    $('.finder-form__dropdown:not(' + drpdwn + ')').addClass('hide');
    $(drpdwn).removeClass("hide");
});
