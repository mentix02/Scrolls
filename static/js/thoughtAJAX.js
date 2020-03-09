let thinkForm = $('#thinkForm');
let csrftoken = $("[name=csrfmiddlewaretoken]").val();

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function () {
    $('#thinkModal').on('shown.bs.modal', function () {
        $(this).find('#body').focus();
    });
});

$('#thinkButton').click(function (_) {
    thinkForm.submit();
});

thinkForm.submit(function (e) {

    e.preventDefault();

    if (localStorage.getItem('token')) {

        let body = $('#body').val();

        let data = {
            body: body,
            token: localStorage.getItem('token')
        }
    
        $.ajax({
            data: data,
            method: 'post',
            url: '/thoughts/new/',
            success: function(thought) {
                thinkForm.trigger('reset');
                // noinspection JSUnresolvedVariable
                $('#thoughts').prepend(`<div class="col-md-4" id="thought${thought.pk}">
                                          <div class="card mb-4 shadow-lg">
                                            <div class="card-body">
                                              <p class="card-text">${thought.body}</p>
                                            </div>
                                            <div class="card-footer text-center">
                                              <p class="card-text float-left">${thought.timestamp}</p>
                                              <button id="delete${thought.pk}" class="btn btn-outline-danger btn-sm float-right">
                                                <i class="fas fa-trash"></i>
                                              </button>
                                            </div>
                                          </div>
                                        </div>`);
                $('#thinkModal').modal('hide');
            },
            error: function(data) {
                console.log(data);
            }
        });
    }
});

$('.btn-outline-danger').click(function() {

    let thought_pk = this.id.match(/[0-9]+/)[0];

    if (localStorage.getItem('token')) {

        let thoughtAlert = $('#genericThoughtAlert');

        $.ajax({
            method: 'post',

            url: '/thoughts/delete/',

            data: {
                thought_pk: thought_pk,
                token: localStorage.getItem('token'),
            },

            success: function (data) {
                console.log(data);
                if (data['deleted']) {
                    $(`#thought${thought_pk}`).remove();
                    $('#thoughtAlertMessage').text('Thought deleted successfully!');
                    thoughtAlert.css('display', '');
                    thoughtAlert.addClass('alert-success');
                }
            },

            error: function (xhr, _, __) {
                let error = JSON.parse(xhr.responseText);
                thoughtAlert.addClass('alert-danger');
                $('#thoughtAlertMessage').text(`Error : ${error.error}`);
                thoughtAlert.css('display', '');
            }

        });

    }
});
