let editor1 = CodeMirror.fromTextArea(document.getElementById("code1"), {
    value: `#include <stdio.h>\nint main() {\n// printf() displays the string inside quotation\nprintf("Hello, World!");\nreturn 0;\n}`,
    lineNumbers: true
  });

  let editor2 = CodeMirror.fromTextArea(document.getElementById("code2"), {
    value: `#include <stdio.h>\nint main() {\n// printf() displays the string inside quotation\nprintf("Hello, World!");\nreturn 0;\n}`,
    mode: "text/x-csrc", // Specify the mode as "text/x-csrc" for C code
    lineNumbers: true
  });

  let editor3 = CodeMirror.fromTextArea(document.getElementById("code3"), {
    value: `#include <stdio.h>\nint main() {\n// printf() displays the string inside quotation\nprintf("Hello, World!");\nreturn 0;\n}`,
    mode: "text/x-csrc", // Specify the mode as "text/x-csrc" for C code
    lineNumbers: true
  });

  let q1_btn = document.getElementById("q1_btn");
  let q2_btn = document.getElementById("q2_btn");
  let q3_btn = document.getElementById("q3_btn");

function toggle_editor(qn_num){
  document.querySelector('.question-container.active').classList.remove('active');
  document.querySelector('#q'+qn_num).classList.add('active');
}

  q1_btn.addEventListener("click", function() {
    let code = editor1.getValue();
    console.log(code);
    toggle_editor(1);
  }
  );

  q2_btn.addEventListener("click", function() {
    let code = editor2.getValue();
    console.log(code);
    toggle_editor(2);
  });

  q3_btn.addEventListener("click", function() {
    let code = editor3.getValue();
    console.log(code);
    toggle_editor(3);
  });