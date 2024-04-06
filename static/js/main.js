let editor1 = CodeMirror.fromTextArea(document.getElementById("code1"), {
    lineNumbers: true
  });

  let editor2 = CodeMirror.fromTextArea(document.getElementById("code2"), {
    lineNumbers: true
  });

  let editor3 = CodeMirror.fromTextArea(document.getElementById("code3"), {
    lineNumbers: true
  });

  let q1_btn = document.getElementById("q1_btn");
  let q2_btn = document.getElementById("q2_btn");
  let q3_btn = document.getElementById("q3_btn");

function toggle_editor(qn_num){
  document.querySelector('.question-container.active').classList.remove('active');
  document.querySelector('#q'+qn_num).classList.add('active');
  
}

function toggle_qn_btn(qn_num){
  document.querySelector('.question_tab.active').classList.remove('active');
  document.querySelector('#q'+qn_num+'_btn').classList.add('active');
}
  q1_btn.addEventListener("click", function() {
    toggle_editor(1);
    toggle_qn_btn(1);
  }
  );

  q2_btn.addEventListener("click", function() {
    toggle_editor(2);
    toggle_qn_btn(2);
  });

  q3_btn.addEventListener("click", function() {
    toggle_editor(3);
    toggle_qn_btn(3);
  });