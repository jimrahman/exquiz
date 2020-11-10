id = location.hash.slice(1);
console.log(id);

var id = location.hash.slice(1);
console.log(id);

correctform = document.getElementById("correct");

url = "http://localhost:8989/answer/" + id;

fetch(url)
  .then(function (res) {
    return res.json();
  })
  .then(function (data) {
    correctSelection(data);
  });

function correctSelection(resp) {
  console.log(resp);
  answer1 = JSON.stringify(resp["answer"][0]["text"]);
  answer2 = JSON.stringify(resp["answer"][1]["text"]);
  answer3 = JSON.stringify(resp["answer"][2]["text"]);
  ans_selection = [answer1, answer2, answer3];

  correctstr = "";
  correctstr += "The Correct Answer is shown below";
  correctstr += "<br>";

  for (let i = 0; i < resp["answer"].length; i++) {
    if (resp["answer"][i]["selectedBySender"] == true) {
      correctstr +=
        i +
        1 +
        ") " +
        ans_selection[i].substring(1, ans_selection[i].length - 1) +
        " (Correct)";
      correctstr += "<br>";
    } else {
      correctstr +=
        i +
        1 +
        ") " +
        ans_selection[i].substring(1, ans_selection[i].length - 1);
      correctstr += "<br>";
    }
  }
  var div = document.createElement("div");
  div.innerHTML = correctstr;

  correctform.appendChild(div);
}
