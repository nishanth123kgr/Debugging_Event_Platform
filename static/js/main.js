let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    value: `#include <stdio.h>\nint main() {\n// printf() displays the string inside quotation\nprintf("Hello, World!");\nreturn 0;\n}`,
    mode: "text/x-csrc", // Specify the mode as "text/x-csrc" for C code
    lineNumbers: true
  });