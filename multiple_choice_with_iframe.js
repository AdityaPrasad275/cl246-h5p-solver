
const iframe = document.querySelector('iframe'); // select the iframe element
const innerDoc = iframe.contentDocument || iframe.contentWindow.document; // get the document object inside the iframe
const options = innerDoc.querySelectorAll('.h5p-answer'); // select the answer options inside the iframe

for (let i = 0; i < options.length; i++) {
    options[i].click(); // click on each answer option
}

innerDoc.querySelectorAll('.h5p-question-check-answer')[0].click(); // click the "Check" button

const correctOptions = [];
const options_1 = innerDoc.querySelectorAll('.h5p-answer');
for (let i = 0; i < options_1.length; i++) {
    if (options_1[i].classList.contains("h5p-correct")) {
    correctOptions.push(options_1[i].textContent.split('\n')[0]);
    }
}

innerDoc.querySelectorAll('.h5p-question-try-again')[0].click(); // click the "Try Again" button

const options_2 = [...innerDoc.querySelectorAll('.h5p-answer')];
for (let i = 0; i < options_2.length; i++) {
    if (correctOptions.includes(options_2[i].textContent.split('\n')[0])) {
    options_2[i].click(); // click on each correct answer option
    }
}
await new Promise(resolve => setTimeout(resolve, 500));
innerDoc.querySelectorAll('.h5p-question-check-answer')[0].click(); // click the "Check" button again
await new Promise(resolve => setTimeout(resolve, 500));
innerDoc.querySelectorAll('.h5p-question-iv-continue')[0].click(); // click the "Continue" button
