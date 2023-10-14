function getRandomIdea() {
    const keywords = ["technology", "food", "travel", "health", "education"];
    const products = ["app", "website", "platform", "service", "product"];
    
    if (keywords.length === 0 || products.length === 0 || keywords.length !== products.length) {
        return "Sorry, unable to generate idea at the moment.";
    }
    
    const randomKeyword = keywords[Math.floor(Math.random() * keywords.length)];
    const randomProduct = products[Math.floor(Math.random() * products.length)];
    
    const idea = "Create a " + randomKeyword + " " + randomProduct + ".";
    
    return idea;
}