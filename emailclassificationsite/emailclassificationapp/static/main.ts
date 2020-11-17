/*
 *
 * THIS FILE IS NOT INCLUDED ON THE WEBPAGE
 * Transpile this file to js as main.js before running
 * 
 * */

function classifier() {
    // Show the loading spinner
    document.getElementById("loading").className = "fas fa-circle-notch fa-spin fa-3x ml-auto";

    var email = (<HTMLInputElement>document.getElementById("input")).value;

    /*
     * Machine Learning Logic will go here
     */

    document.getElementById("output").innerHTML = email;

    // Display the output row
    document.getElementById("output_row").className = "row bg-light p-3 rounded mt-2"
    // Hide the loading spinner
    document.getElementById("loading").className = "d-none"
}