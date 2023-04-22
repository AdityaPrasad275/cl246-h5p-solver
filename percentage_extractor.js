// Get the container div element
const container = document.querySelector('.h5p-interactions-container');

// Get an array of all the child div elements with the class name 'h5p-seekbar-interaction'
const seekbarInteractions = container.querySelectorAll('.h5p-seekbar-interaction');

// Create an empty array to store the 'left' values
const leftValues = [];

// Loop through the seekbar interactions and extract the 'left' value from each element
seekbarInteractions.forEach((interaction) => {
  leftValues.push(interaction.style.left);
});

// Now the left values are stored in the 'leftValues' array
console.log(leftValues);
// Assume the array of left values is stored in a variable called 'leftValues'

// Map over the array and convert each left value to a number
const leftNumbers = leftValues.map(leftValue => {
    // Remove the percentage sign and convert to number
    const valueWithoutPercentage = parseFloat(leftValue.replace('%', ''));
    // Divide by 100 and return the resulting number
    return valueWithoutPercentage / 100;
  });
  
// Now 'leftNumbers' contains an array of numbers instead of strings with percentages
return leftNumbers;
  