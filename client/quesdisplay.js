var id = location.hash.slice(1);
quesTable = document.getElementById("questable");

url = "http://localhost:8989/questions/" + id;

{
  fetch(url)
    .then(function (res) {
      return res.json();
    })
    .then(function (data) {
      if (data["answered"] == "yes") {
        window.location.replace("resubmit.html#" + id);
      } else {
        renderHTML(data);
      }
    });
}

function renderHTML(allData) {
  question = allData["question"];
  answer1 = JSON.stringify(allData["answer"][0]);
  answer2 = JSON.stringify(allData["answer"][1]);
  answer3 = JSON.stringify(allData["answer"][2]);

  var addingString = "";
  addingString += "Question: " + question;
  addingString += "<br>";
  addingString += '<input id="check1" type="checkbox">';
  addingString += " " + answer1.substring(1, answer1.length - 1);
  addingString += "<br>";
  addingString += '<input id="check2" type="checkbox">';
  addingString += " " + answer2.substring(1, answer2.length - 1);
  addingString += "<br>";
  addingString += '<input id="check3" type="checkbox">';
  addingString += " " + answer3.substring(1, answer3.length - 1);

  var div = document.createElement("div");
  div.innerHTML = addingString;

  quesTable.appendChild(div);
}

quesDisplay = document.getElementById("quesdisplay");

quesDisplay.onsubmit = (element) => {
  element.preventDefault();

  user2ans1 = document.getElementById("check1");
  user2ans2 = document.getElementById("check2");
  user2ans3 = document.getElementById("check3");

  answerSelection = [
    { selectedByReceiver: false },
    { selectedByReceiver: false },
    { selectedByReceiver: false },
  ];
  if (user2ans1.checked == true) {
    answerSelection[0]["selectedByReceiver"] = true;
  }
  if (user2ans2.checked == true) {
    answerSelection[1]["selectedByReceiver"] = true;
  }
  if (user2ans3.checked == true) {
    answerSelection[2]["selectedByReceiver"] = true;
  }

  console.log(answerSelection);

  url1 =
    "http://localhost:8989/questions/" + id + "/action/selectreceiver";

  raw = JSON.stringify({
    receiverResponse: answerSelection,
  });

  fetch(url1, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: raw,
    redirect: "follow",
  })
    .then((response) => response.text())
    .then((data) => {
      result = data.replace("[", "");
      resultlist = result.replace("]", "").split(",");
      console.log(resultlist);
      if (
        resultlist[0] == "1" &&
        resultlist[1] == " 1" &&
        resultlist[2] == " 1"
      ) {
        window.location.replace("correct.html#" + id);
      } else {
        window.location.replace("incorrect.html#" + id);
      }
    })
    .catch((error) => {
      alert(error);
      console.log("error", error);
    });
};
