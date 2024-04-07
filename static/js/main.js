let editor1 = CodeMirror.fromTextArea(document.getElementById("code1"), {
  lineNumbers: true
});

let editor2 = CodeMirror.fromTextArea(document.getElementById("code2"), {
  lineNumbers: true
});

let editor3 = CodeMirror.fromTextArea(document.getElementById("code3"), {
  lineNumbers: true
});

let editor4 = CodeMirror.fromTextArea(document.getElementById("code4"), {
  lineNumbers: true
});

let editor5 = CodeMirror.fromTextArea(document.getElementById("code5"), {
  lineNumbers: true
});

let editor_array = [editor1, editor2, editor3, editor4, editor5];

let qn_timer_status = [true, false, false, false, false];

let q1_btn = document.getElementById("q1_btn");
let q2_btn = document.getElementById("q2_btn");
let q3_btn = document.getElementById("q3_btn");
let q4_btn = document.getElementById("q4_btn");
let q5_btn = document.getElementById("q5_btn");

let q1_reset = document.getElementById("q1_reset");
let q2_reset = document.getElementById("q2_reset");
let q3_reset = document.getElementById("q3_reset");
let q4_reset = document.getElementById("q4_reset");
let q5_reset = document.getElementById("q5_reset");

let q1_timer = new easytimer.Timer();
let q2_timer = new easytimer.Timer();
let q3_timer = new easytimer.Timer();
let q4_timer = new easytimer.Timer();
let q5_timer = new easytimer.Timer();

let timer_array = [q1_timer, q2_timer, q3_timer, q4_timer, q5_timer];

if (localStorage.getItem(`#q1_timer`)) {
  q1_timer.start({ startValues: JSON.parse(localStorage.getItem(`#q1_timer`)) });
} else {
  q1_timer.start({ precision: 'seconds', target: { hours: 1 } });
}



timer_array.forEach((timer, index) => {
  timer.addEventListener('secondsUpdated', function (e) {
    let time = timer.getTimeValues();
    document.querySelector(`#q${index + 1}_timer`).innerHTML = time.toString();
    localStorage.setItem(`#q${index + 1}_timer`, JSON.stringify(time));

  });

  q2_timer.addEventListener('targetAchieved', function (e) {
    document.querySelector(`#q${index + 1}_timer`).innerHTML = 'Time UP!!';
  });

  if (localStorage.getItem(`#q${index + 1}_timer`)) {
    timer.start({ startValues: JSON.parse(localStorage.getItem(`#q${index + 1}_timer`)) });
  }
});



function toggle_editor(qn_num) {
  document.querySelector('.question-container.active').classList.remove('active');
  document.querySelector('#q' + qn_num).classList.add('active');
}

function toggle_qn_btn(qn_num) {
  document.querySelector('.question_tab.active').classList.remove('active');
  document.querySelector('#q' + qn_num + '_btn').classList.add('active');
}
q1_btn.addEventListener("click", function () {
  if (qn_timer_status[0] == false) {
    qn_timer_status[0] = true;
    q1_timer.start({ precision: 'seconds', target: { hours: 1 } });
  }
  toggle_editor(1);
  toggle_qn_btn(1);
});

q2_btn.addEventListener("click", function () {
  if (qn_timer_status[1] == false) {
    qn_timer_status[1] = true;
    q2_timer.start({ precision: 'seconds', target: { hours: 1 } });
  }
  toggle_editor(2);
  toggle_qn_btn(2);
});

q3_btn.addEventListener("click", function () {
  if (qn_timer_status[2] == false) {
    qn_timer_status[2] = true;
    q3_timer.start({ precision: 'seconds', target: { hours: 1 } });
  }
  toggle_editor(3);
  toggle_qn_btn(3);
});

q4_btn.addEventListener("click", function () {
  if (qn_timer_status[3] == false) {
    qn_timer_status[3] = true;
    q4_timer.start({ precision: 'seconds', target: { hours: 1 } });
  }
  toggle_editor(4);
  toggle_qn_btn(4);
});

q5_btn.addEventListener("click", function () {
  if (qn_timer_status[4] == false) {
    qn_timer_status[4] = true;
    q5_timer.start({ precision: 'seconds', target: { hours: 1 } });
  }
  toggle_editor(5);
  toggle_qn_btn(5);
});


let q1_submit = document.getElementById("q1_submit");
let q2_submit = document.getElementById("q2_submit");
let q3_submit = document.getElementById("q3_submit");
let q4_submit = document.getElementById("q4_submit");
let q5_submit = document.getElementById("q5_submit");

let submit_btns = [q1_submit, q2_submit, q3_submit, q4_submit, q5_submit];

submit_btns.forEach((btn, index) => {
  btn.addEventListener("click", function () {
    let code = editor_array[index].getValue();
    let formData = new FormData();
    formData.append("code", code);
    formData.append("qn_num", index + 1);
    formData.append("submitted_time", new Date().toLocaleString());
    formData.append("time", JSON.stringify(timer_array[index].getTimeValues()));
    btn.querySelector('#spinner').style = 'display: inline-block;'
    fetch('/submit', {
      method: 'POST',
      body: formData
    }).then(response => response.json())
      .then(data => {
        if (data.result.error == 0) {
          Swal.fire({
            title: "Submitted Successfully!",
            text: `All Testcases Passesd. Solved Question ${index + 1} !! 🥳🎉`,
            icon: "success"
          });
          document.querySelector(`#q${index + 1}_solved`).style = 'display: inline-flex;'

        } else {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: data.result.err_desc,
          });
        }
        btn.querySelector('#spinner').style = 'display: none;'
      });
  });
}
);



// q1_submit.addEventListener("click", function () {
//   let code = editor1.getValue();
//   let formData = new FormData();
//   formData.append("code", code);
//   formData.append("qn_num", 1);
//   formData.append("submitted_time", new Date().toLocaleString());
//   formData.append("submitted_by", "user1");
//   q1_submit.querySelector('#spinner').style = 'display: inline-block;'
//   fetch('/submit', {
//     method: 'POST',
//     body: formData
//   }).then(response => response.json())
//     .then(data => {
//       if (data.result.error == 0) {
//         Swal.fire({
//           title: "Submitted Successfully!",
//           text: "All Testcases Passesd. Solved 1st Question! 🥳🎉",
//           icon: "success"
//         });
//         document.querySelector('#q1_solved').style = 'display: inline-flex;'

//       } else {
//         Swal.fire({
//           icon: "error",
//           title: "Oops...",
//           text: data.result.err_desc,
//         });
//       }
//       q1_submit.querySelector('#spinner').style = 'display: none;'
//     });
// }
// );


// q2_submit.addEventListener("click", function () {
//   let code = editor2.getValue();
//   let formData = new FormData();
//   formData.append("code", code);
//   formData.append("qn_num", 2);
//   formData.append("submitted_time", new Date().toLocaleString());
//   formData.append("submitted_by", "user1");
//   q2_submit.querySelector('#spinner').style = 'display: inline-block;'
//   fetch('/submit', {
//     method: 'POST',
//     body: formData
//   }).then(response => response.json())
//     .then(data => {
//       if (data.result.error == 0) {
//         Swal.fire({
//           title: "Submitted Successfully!",
//           text: "All Testcases Passesd. Solved 2nd Question! 🥳🎉",
//           icon: "success"
//         });
//         document.querySelector('#q2_solved').style = 'display: inline-flex;'

//       } else {
//         Swal.fire({
//           icon: "error",
//           title: "Oops...",
//           text: data.result.err_desc,
//         });
//       }
//       q2_submit.querySelector('#spinner').style = 'display: none;'

//     });
// });

// q3_submit.addEventListener("click", function () {
//   let code = editor3.getValue();
//   let formData = new FormData();
//   formData.append("code", code);
//   formData.append("qn_num", 3);
//   formData.append("submitted_time", new Date().toLocaleString());
//   formData.append("submitted_by", "user1");
//   q3_submit.querySelector('#spinner').style = 'display: inline-block;'
//   fetch('/submit', {
//     method: 'POST',
//     body: formData
//   }).then(response => response.json())
//     .then(data => {
//       if (data.result.error == 0) {
//         Swal.fire({
//           title: "Submitted Successfully!",
//           text: "All Testcases Passesd. Solved 3rd Question! 🥳🎉",
//           icon: "success"
//         });
//         document.querySelector('#q3_solved').style = 'display: inline-flex;'
//       } else {
//         Swal.fire({
//           icon: "error",
//           title: "Oops",
//           text: data.result.err_desc,
//         });
//       }
//       q3_submit.querySelector('#spinner').style = 'display: none;'

//     });
// });


// q4_submit.addEventListener("click", function () {
//   let code = editor4.getValue();
//   let formData = new FormData();
//   formData.append("code", code);
//   formData.append("qn_num", 4);
//   formData.append("submitted_time", new Date().toLocaleString());
//   formData.append("submitted_by", "user1");
//   q4_submit.querySelector('#spinner').style = 'display: inline-block;'
//   fetch('/submit', {
//     method: 'POST',
//     body: formData
//   }).then(response => response.json())
//     .then(data => {
//       if (data.result.error == 0) {
//         Swal.fire({
//           title: "Submitted Successfully!",
//           text: "All Testcases Passesd. Solved 4th Question! 🥳🎉",
//           icon: "success"
//         });
//         document.querySelector('#q4_solved').style = 'display: inline-flex;'

//       } else {
//         Swal.fire({
//           icon: "error",
//           title: "Oops",
//           text: data.result.err_desc,
//         });
//       }
//       q4_submit.querySelector('#spinner').style = 'display: none;'
//     });
// }
// );

// q5_submit.addEventListener("click", function () {
//   let code = editor5.getValue();
//   let formData = new FormData();
//   formData.append("code", code);
//   formData.append("qn_num", 5);
//   formData.append("submitted_time", new Date().toLocaleString());
//   formData.append("submitted_by", "user1");
//   q5_submit.querySelector('#spinner').style = 'display: inline-block;'
//   fetch('/submit', {
//     method: 'POST',
//     body: formData
//   }).then(response => response.json())
//     .then(data => {
//       if (data.result.error == 0) {
//         Swal.fire({
//           title: "Submitted Successfully!",
//           text: "All Testcases Passesd. Solved 5th Question! 🥳🎉",
//           icon: "success"
//         });
//         document.querySelector('#q5_solved').style = 'display: inline-flex;'

//       } else {
//         Swal.fire({
//           icon: "error",
//           title: "Oops",
//           text: data.result.err_desc,
//         });
//       }
//       q5_submit.querySelector('#spinner').style = 'display: none;'
//     });
// }
// );

q1_reset.addEventListener("click", function () {
  editor1.setValue(default_codes[0]);
});

q2_reset.addEventListener("click", function () {
  editor2.setValue(default_codes[1]);
});

q3_reset.addEventListener("click", function () {
  editor3.setValue(default_codes[2]);
});

q4_reset.addEventListener("click", function () {
  editor4.setValue(default_codes[3]);
});

q5_reset.addEventListener("click", function () {
  editor5.setValue(default_codes[4]);
});


var timer = new easytimer.Timer();
if (localStorage.getItem('time')) {
  timer.start({ countdown: true, startValues: JSON.parse(localStorage.getItem('time')) });
} else {
  timer.start({ countdown: true, startValues: { hours: 1 } });
}

document.querySelector('#timer').innerHTML = timer.getTimeValues().toString();

timer.addEventListener('secondsUpdated', function (e) {
  let time = timer.getTimeValues();
  document.querySelector('#timer').innerHTML = time.toString();
  localStorage.setItem('time', JSON.stringify(time));

});

timer.addEventListener('targetAchieved', function (e) {
  document.querySelector('#timer').innerHTML = 'Time UP!!';
});




