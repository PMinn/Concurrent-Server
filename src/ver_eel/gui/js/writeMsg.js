const container = document.getElementById('container');
eel.expose(writeMsg);
function writeMsg(code, msg) {
    var li = document.createElement('div');
    li.classList.add('li');
    if (code == 1) { // recv
        li.innerHTML = `<span class="code recv">recv</span>data: ${msg}`;
    } else if (code == 0) { // send
        li.innerHTML = `<span class="code send">send</span>data: ${msg}`;
    } else if (code == 2) { // set
        li.innerHTML = `<span class="code set">set</span> ${msg}`;
    } else if (code == 3) { // ok
        li.innerHTML = `<span class="code recv">ok</span> ${msg}`;
    } else if (code == 4) { // error
        li.innerHTML = `<span class="code timeout">error</span> ${msg}`;
    } else if (code == 5) { // waiting
        li.innerHTML = `<span class="code set">wait</span> ${msg}`;
    }
    container.appendChild(li);
    // li.scrollIntoView(false);
    return 0;
}