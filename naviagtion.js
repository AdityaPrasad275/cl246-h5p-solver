//document.querySelectorAll('.video-stream')[0].duration

let totalTime = 1106.661
let percentage = [0.22802299999999998, 0.530777, 0.63402, 0.964188]
let i = 0;
document.querySelectorAll('.video-stream')[0].currentTime = totalTime*percentage[i] - 2
