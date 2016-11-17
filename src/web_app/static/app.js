let get_interest_answers = function() {
    let answers = []
    $('input:radio').each(function() {
      if($(this).is(':checked')) {
        answers.push($(this).val())
      }})
    return answers
};

let send_answers_json = function(answers) {
    $.ajax({
        url: '/score',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            console.log(data);
        },
        data: JSON.stringify(answers)
    });
};

$(document).ready(function() {

    $("button#submit").click(function() {
        let answers = get_interest_answers();
        send_answers_json(answers);
    })

})
