const $targetEl = document.getElementById("defaultModal");
const modal = new Flowbite.default.Modal($targetEl);

const runContent = document.getElementById("run-content");

function reload() {
  window.location.reload();
}

function deleteTask(id) {
  let url = window.location.href + "tasks/delete/" + id;
  fetch(url)
    .then((data) => {
      return data.json();
    })
    .then((result) => {
      console.log(result);
      if (result.deleted == true) {
        reload();
      } else {
        alert("Error to delete!!");
      }
    });
}

function executeTask(id, token) {
  let url = window.location.href + "tasks/execute/" + id;
  fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ token: token }),
  })
    .then((data) => {
      return data.json();
    })
    .then((result) => {
      if (result.Error) {
        alert(result.Error);
      } else {
        modal.show();
        result.forEach((element) => {
          runContent.innerText += `${element} \n`;
        });
      }
    });
}

function copyToken(id) {
  let copyInput = document.getElementById(`token-${id}`);

  copyInput.select();
  copyInput.setSelectionRange(0, 99999);

  navigator.clipboard.writeText(copyInput.value);
}

document.getElementById("add-task-form").addEventListener(
  "submit",
  function (event) {
    event.preventDefault();

    const form = event.target;
    const formFields = form.elements;

    let url = window.location.href + "tasks/create";

    fetch(url, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: formFields.name.value,
        command: formFields.command.value,
        directory: formFields.directory.value,
      }),
    })
      .then((data) => {
        return data.json();
      })
      .then((result) => {
        console.log(result);
        reload();
      });
  },
  false
);
