// Function to generate a random joke
function generateJoke() {
  const jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "Did you hear about the mathematician who is afraid of negative numbers? He will stop at nothing to avoid them!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I used to be a baker, but I couldn't make enough dough.",
    "What do you call someone with no body and no nose? Nobody knows!"
  ];

  const randomIndex = Math.floor(Math.random() * jokes.length);
  return jokes[randomIndex];
}

// Event listener for the "Generate Joke" button
document.addEventListener('DOMContentLoaded', () => {
  const generateJokeButton = document.getElementById('generateJokeButton');
  const jokeDisplay = document.getElementById('jokeDisplay');

  generateJokeButton.addEventListener('click', () => {
    const joke = generateJoke();
    jokeDisplay.textContent = joke;
  });
});