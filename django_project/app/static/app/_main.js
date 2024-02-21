$("#username").change(function () {
        var username = $(this).val();
        console.log('username changed')
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });
        $.ajax({
        url: 'validate',
        method: 'POST',
        data: {
          'username': username
        },
        dataType: 'json',
        success: function (data) {
          if (data.taken) {
            alert("Username taken");
          }
        }
      });
    });

$('#user-form').on('submit', function(event) {
        event.preventDefault();
        console.log('username submitted')
        var username = $("#username").val();
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });
        $.ajax({
        url: 'get_text',
        method: 'POST',
        data: {
          'username': username
        },
        dataType: 'json',
        success: function (data) {
          alert(data.username)
        }
      });
    });

$('#submit-button').click(function(){
    var username = $("#username").val();
    console.log('username submitted: ' + username)
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
    $.ajax({
    url: 'get-text',
    method: 'POST',
    data: {
      'username': username
    },
    dataType: 'json',
    success: function (data) {
      alert(data.username);
    }
  });
});
