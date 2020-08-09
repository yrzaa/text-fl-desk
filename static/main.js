
var element=document.getElementById("demo");


//Main events
function sub()
{
  var x = document.getElementById("frm").elements[0].value;
  prediction(x);
}
hide(element);

function clean()
{
  document.getElementById("frm").reset();
  hide(element)
}


//========================================================================
// Helper functions
//========================================================================

function prediction(inp) {
  const data={input:inp}
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          displayResult(data);
        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
    });
}

function displayResult(inp) {
  inp=inp.result;
  show(element)
  if(inp === 0)
  {
  console.log("Negative");
  
  element.innerHTML="Negative";
  }
  else
  {
  console.log("Positive");
  element.innerHTML="Positive";
  }
}

function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}