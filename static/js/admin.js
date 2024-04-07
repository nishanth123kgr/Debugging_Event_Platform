let q1_btn = document.getElementById("q1_btn");
let q2_btn = document.getElementById("q2_btn");
let q3_btn = document.getElementById("q3_btn");
let q4_btn = document.getElementById("q4_btn");
let q5_btn = document.getElementById("q5_btn");
let q6_btn = document.getElementById("q6_btn");

function toggle_editor(qn_num) {
    document.querySelector('.question-container.active').classList.remove('active');
    document.querySelector('#q' + qn_num).classList.add('active');
}

function toggle_qn_btn(qn_num) {
    document.querySelector('.question_tab.active').classList.remove('active');
    document.querySelector('#q' + qn_num + '_btn').classList.add('active');
}
q1_btn.addEventListener("click", function () {
    toggle_editor(1);
    toggle_qn_btn(1);
});

q2_btn.addEventListener("click", function () {

    toggle_editor(2);
    toggle_qn_btn(2);
});

q3_btn.addEventListener("click", function () {

    toggle_editor(3);
    toggle_qn_btn(3);
});

q4_btn.addEventListener("click", function () {

    toggle_editor(4);
    toggle_qn_btn(4);
});

q5_btn.addEventListener("click", function () {

    toggle_editor(5);
    toggle_qn_btn(5);
});

q6_btn.addEventListener("click", function () {

    toggle_editor(6);
    toggle_qn_btn(6);
});

const socket = io();

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('refresh_admin', () => {
    location.reload();
});