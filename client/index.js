quesForm = document.getElementById("quesForm");

quesForm.onsubmit = (element) => {
  element.preventDefault();

  question = document.getElementById("question").value;
  result1 = document.getElementById("result1").value;
  result2 = document.getElementById("result2").value;
  result3 = document.getElementById("result3").value;
  correctRes1 = document.getElementById("check1");
  correctRes2 = document.getElementById("check2");
  correctRes3 = document.getElementById("check3");

  AnswerSelection = [
    { text: result1, selectedBySender: false },
    { text: result2, selectedBySender: false },
    { text: result3, selectedBySender: false },
  ];

  if (correctRes1.checked == true) {
    AnswerSelection[0]["selectedBySender"] = true;
  }
  if (correctRes2.checked == true) {
    AnswerSelection[1]["selectedBySender"] = true;
  }
  if (correctRes3.checked == true) {
    AnswerSelection[2]["selectedBySender"] = true;
  }

  raw = JSON.stringify({
    question: question,
    answer: AnswerSelection,
  });

  fetch("http://localhost:8989/questions", { 
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: raw,
    redirect: "follow",
  })
    .then((response) => response.json())
    .then((data) => {
      receievedAns = data["answer"];
      if (receievedAns == "") {
        alert("Sorry theres a problem in the server, we are working");
      } else {
        receivedId = data.toString()
        window.location.replace("confirmation.html#"+receivedId);
      }
    })
    .catch((error) => {
      alert(error);
      console.log("error", error);
    });
};
