document.addEventListener("DOMContentLoaded", function () {
  var modeSwitch = document.querySelector(".mode-switch");

  modeSwitch.addEventListener("click", function () {
    document.documentElement.classList.toggle("dark");
    // modeSwitch.classList.toggle("active");
  });

  var listView = document.querySelector(".list-view");
  var gridView = document.querySelector(".grid-view");
  var projectsList = document.querySelector(".project-boxes");

  listView.addEventListener("click", function () {
    gridView.classList.remove("active");
    listView.classList.add("active");
    projectsList.classList.remove("jsGridView");
    projectsList.classList.add("jsListView");
  });

  gridView.addEventListener("click", function () {
    gridView.classList.add("active");
    listView.classList.remove("active");
    projectsList.classList.remove("jsListView");
    projectsList.classList.add("jsGridView");
  });

  document
    .querySelector(".messages-btn")
    .addEventListener("click", function () {
      document.querySelector(".messages-section").classList.add("show");
    });

  document
    .querySelector(".messages-close")
    .addEventListener("click", function () {
      document.querySelector(".messages-section").classList.remove("show");
    });
});

//Setup
var fsmActual = document.createElement("div");
fsmActual.setAttribute("id", "fsm_actual");
document.body.appendChild(fsmActual);
var $fsm = document.querySelectorAll(".fsm");
var $fsmActual = document.querySelector("#fsm_actual");
$fsmActual.style.position = "absolute";

var position = {};
var size = {};

//modal action stuffs
var openFSM = function (event) {
	var $this = event.currentTarget;
	position = $this.getBoundingClientRect();
	size = {
		width: window.getComputedStyle($this).width,
		height: window.getComputedStyle($this).height
	};

	$fsmActual.style.position = "absolute";
	$fsmActual.style.top = position.top + "px";
	$fsmActual.style.left = position.left + "px";
	$fsmActual.style.height = size.height;
	$fsmActual.style.width = size.width;
	$fsmActual.style.margin = $this.style.margin;

	setTimeout(function () {
		$fsmActual.innerHTML = $this.innerHTML;
		var classes = $this.classList.value.split(" ");
		for (var i = 0; i < classes.length; i++) {
			$fsmActual.classList.add(classes[i]);
		}
		$fsmActual.classList.add("growing");
		$fsmActual.style.height = "100vh";
		$fsmActual.style.width = "100vw";
		$fsmActual.style.top = "0";
		$fsmActual.style.left = "0";
		$fsmActual.style.margin = "0";
	}, 1);

	setTimeout(function () {
		$fsmActual.classList.remove("growing");
		$fsmActual.classList.add("full-screen");
	}, 1000);
};

var closeFSM = function (event) {
	var $this = event.currentTarget;

	$this.style.height = size.height;
	$this.style.width = size.width;
	$this.style.top = position.top + "px";
	$this.style.left = position.left + "px";
	$this.style.margin = "0";
	$this.classList.remove("full-screen");
	$this.classList.add("shrinking");

	setTimeout(function () {
		while ($this.firstChild) $this.removeChild($this.firstChild);
		var classList = $this.classList;
		while (classList.length > 0) {
			classList.remove(classList.item(0));
		}
		$this.style = "";
	}, 1000);
};

for (var i = 0; i < $fsm.length; i++) {
	$fsm[i].addEventListener("click", openFSM);
}
$fsmActual.addEventListener("click", closeFSM);


  