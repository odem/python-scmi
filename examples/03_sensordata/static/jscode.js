var isEnabled = false;
var iterations = 0;

function start() {
  isEnabled = true;
  iterations = 0;
  var sensordiv = document.getElementById("sensordata");
  sensordiv.innerHTML = "";
  loop();
}

function stop() {
  isEnabled = false;
}

function loop() {
  if (isEnabled === true) {
    setTimeout(function () {
      doSomething();
      loop();
    }, 1000);
  }
}

function doSomething() {
  var data = getData();
}

function getData() {
  var requestor = new Requestor();

  var url = "/sensordata";
  var args = { paramname: 42 };
  var onmysuccess = gut;
  var onmyerror = boese;

  requestor.fetch_sensordata(url, args, onmysuccess, onmyerror);
}

function gut(value) {
  // console.log(
  //   "gut: " +
  //     value.then(function (text) {
  //       console.log("TEXT: " + text);
  //       const sensordiv = document.getElementById("sensordata");
  //       sensordiv.innerHTML = text;
  //     }),
  // );
  console.log("TEXT: " + value);
  const sensordiv = document.getElementById("sensordata");
  sensordiv.innerHTML = value;
}
function boese() {
  console.log("boese");
}
class Requestor {
  constructor() {}

  fetch_sensordata(url, args, onsuccess, onerror) {
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(args),
    };
    this.post(url, options, onsuccess, onerror);
  }

  post(url, options, onsuccess, onerror) {
    fetch(url, options)
      .then(function (response) {
        return response.json();
      })
      .then(function (value) {
        if (onsuccess !== null) {
          onsuccess(value);
        }
      })
      .catch((error) => {
        if (onerror !== null) {
          onerror(error);
        }
      });
  }
}
