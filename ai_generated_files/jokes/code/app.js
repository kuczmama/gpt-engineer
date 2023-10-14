import { generateJoke } from './joke.js';

// Event listener for the "Generate Joke" button
document.addEventListener('DOMContentLoaded', () => {
  const generateJokeButton = document.getElementById('generateJokeButton');
  const jokeDisplay = document.getElementById('jokeDisplay');

  generateJokeButton.addEventListener('click', () => {
    const joke = generateJoke();
    jokeDisplay.textContent = joke;
  });
});