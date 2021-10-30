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

$(document).ready(function() {
	var sessionTime;
	var breakTime;
	var timerID;

	var pomodoro = {
		setTimes: function(action) {
			switch (action) {
				case "subtract-session":
					// set one minute as minimum session length
					if (sessionTime > 1) {
						sessionTime--;
					}
					break;
				case "add-session":
					sessionTime++;
					break;
				case "subtract-break":
					// set one minute as minimum break time
					if (breakTime > 1) {
						breakTime--;
					}
					break;
				case "add-break":
					breakTime++;
					break;
			}

			pomodoro.displayTimes(sessionTime);
		},
		displayTimes: function(currentTime) {
			$("#set-session .time").text(sessionTime);
			$("#set-break .time").text(breakTime);
			$("#timer .time").text(currentTime + ':00');

			// update progress bar to set data total to session value
			pomodoro.updateProgress(currentTime * 60);
		},
		runTimer: function() {
		 	var displayTime = $("#timer .time").text().split(':');
		 	pomodoro.timer(displayTime[0], displayTime[1]);
		},
		pauseTimer: function() {
			clearTimeout(timerID);
		},
		timer: function(minutes, seconds) {
			if (seconds > 0) {
				timerID = setTimeout(function () {
					seconds--;
					$(".progress").progress('increment');
					$("#timer .time").text(minutes + ':' + (seconds < 10 ? '0' + seconds : seconds));
					pomodoro.timer(minutes, seconds);
				}, 1000);
			} else {
				if (minutes > 0) {
					pomodoro.timer(--minutes, 60);
				} else {

					pomodoro.isBreak = !pomodoro.isBreak;
					pomodoro.changeSession();
				}
			}
		},
		changeSession: function() {
			// play audio when changing lesson
			var audio = new Audio('https://dl.dropboxusercontent.com/s/02y8d8zetwdz6rn/Ding%20-%20Sound%20Effects%20YouTube.wav');
			audio.play();
			
			$(".progress").progress('reset');
			if (pomodoro.isBreak) {
				pomodoro.displayTimes(breakTime);
				$(".label").text("Break " + pomodoro.count++);
			} else {
				pomodoro.displayTimes(sessionTime);
				$(".label").text("Session " + pomodoro.count);
			}

			pomodoro.runTimer();
		},
		reset: function() {
			$(".progress").progress('reset');
			pomodoro.displayTimes(sessionTime);
			pomodoro.isBreak = false;
			pomodoro.count = 1;
			$(".label").text("Session " + pomodoro.count);
		},
		updateProgress: function(total) {

			$(".progress").attr("data-value", 0);
			$(".progress").attr("data-total", total);
		},
		isBreak: false,
		count: 1,
	};

	init();

	function init() {
		// set initial length for break and session
		sessionTime = 25;
		breakTime = 5;
		pomodoro.displayTimes(sessionTime);
	}

	$(".switch").click(function() {
		if ($(this).hasClass("play")) {
			pomodoro.runTimer();
			$(this).html('<i class="pause icon"></i> Stop');
			$(".reset").attr("disabled", true);
		} else if ($(this).hasClass("pause")) {
			pomodoro.pauseTimer();
			$(this).html('<i class="play icon"></i> Play');
			$(".reset").attr("disabled", false);
		}

		$(".plus, .minus").attr("disabled", true);
		$(".reset").attr("hidden", false);
		$(this).toggleClass("play");
		$(this).toggleClass("pause");
	});

	$(".plus, .minus").click(function() {
		pomodoro.setTimes($(this).val());
	});

	$(".reset").click(function() {
		pomodoro.reset();
		$(".plus, .minus").attr("disabled", false);
		$(this).attr("hidden", true);
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


