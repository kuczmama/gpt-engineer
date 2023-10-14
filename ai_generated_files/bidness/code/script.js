(function() {
    function generateIdea() {
        const idea = getRandomIdea();
        
        document.getElementById("idea").textContent = idea;
    }

    window.generateIdea = generateIdea;
})();