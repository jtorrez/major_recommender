let get_interest_answers = function() {
    let answers = []
    $('input.interest').each(function() {
      if($(this).is(':checked')) {
        answers.push($(this).val())
      }})
    return answers
};

let get_risk_answers = function() {
    let answers = []
    $('input.risk').each(function() {
      if($(this).is(':checked')) {
        answers.push($(this).val())
      }})
    return answers
};

let get_income_answers = function() {
    let answers = []
    $('input.income').each(function() {
      if($(this).is(':checked')) {
        answers.push($(this).val())
      }})
    return answers
};

let send_answers_json = function(int_answers, risk_score, inc_score) {
    $.ajax({
        url: '/score',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            console.log(data);
        },
        data: JSON.stringify([int_answers, risk_score, inc_score])
    });
};

$(document).ready(function() {

    $("a.btn.btn-default.btn-lg.submit").click(function() {
        let int_answers = get_interest_answers();
        let risk_score = get_risk_answers();
        let inc_score = get_income_answers();
        send_answers_json(int_answers, risk_score, inc_score);
    })

})
