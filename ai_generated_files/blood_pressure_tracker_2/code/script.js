document.getElementById("trackerForm").addEventListener("submit", function(e) {
    e.preventDefault();
    var systolic = document.getElementById("systolic").value;
    var diastolic = document.getElementById("diastolic").value;
    addEntry(systolic, diastolic);
    document.getElementById("systolic").value = "";
    document.getElementById("diastolic").value = "";
});

function addEntry(systolic, diastolic) {
    var entryElement = document.createElement("p");
    entryElement.textContent = "Systolic: " + systolic + " Diastolic: " + diastolic;
    document.getElementById("entriesContainer").appendChild(entryElement);
}