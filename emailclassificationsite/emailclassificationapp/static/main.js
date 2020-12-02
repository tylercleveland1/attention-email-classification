/*
 *
 * THIS FILE IS NOT INCLUDED ON THE WEBPAGE
 * Transpile this file to js as main.js before running
 *
 * */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
function classifier() {
    return __awaiter(this, void 0, void 0, function* () {
        // Show the loading spinner
        document.getElementById("loading").className = "fas fa-circle-notch fa-spin fa-3x ml-auto";
        // Get the email text given in the textbox
        var unformattedEmail = document.getElementById("input").value;
        if (unformattedEmail.length == 0) {
            return;
        }
        // Remove punctuation and other random characters from the email
        var email = unformattedEmail.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");
        email = email.replace(/\s{2,}/g, " ");
        // @ts-ignore
        var emailList = yield ClassificationApi.spamOrHam(email);
        var attentionScores = emailList.keywords;
        var keywords = [];
        // get the words that have high attention scores
        attentionScores.forEach(element => {
            keywords.push(element[0].toLowerCase());
        });
        // get the Spam or Ham prediction
        var prediction = emailList.prediction[0];
        // format the highlighted text to the webpage
        var output = "";
        if (prediction == "spam") {
            document.getElementById("spamOrHam").innerHTML = "Spam";
            document.getElementById("spamOrHam").className = "text-danger";
            unformattedEmail.split(" ").forEach(unformattedWord => {
                var word = unformattedWord.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").replace(/\s{2,}/g, " ");
                if (keywords.indexOf(word.toLowerCase()) !== -1) {
                    var score = getAttentionScore(word, attentionScores);
                    if (score == 0) {
                        output += "<span>" + unformattedWord + "</span> ";
                    }
                    else if (score < 0.2) {
                        output += "<span class='highlight-red-1'>" + unformattedWord + "</span> ";
                    }
                    else if (score < 0.4) {
                        output += "<span class='highlight-red-2'>" + unformattedWord + "</span> ";
                    }
                    else if (score < 0.6) {
                        output += "<span class='highlight-red-3'>" + unformattedWord + "</span> ";
                    }
                    else if (score < 0.8) {
                        output += "<span class='highlight-red-4'>" + unformattedWord + "</span> ";
                    }
                    else {
                        output += "<span class='highlight-red-5'>" + unformattedWord + "</span> ";
                    }
                }
                else {
                    output += "<span>" + unformattedWord + "</span> ";
                }
            });
        }
        else {
            document.getElementById("spamOrHam").innerHTML = "Ham";
            document.getElementById("spamOrHam").className = "text-success";
            unformattedEmail.split(" ").forEach(unformattedWord => {
                var word = unformattedWord.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").replace(/\s{2,}/g, " ");
                if (keywords.indexOf(word.toLowerCase()) !== -1) {
                    var score = getAttentionScore(word, attentionScores);
                    if (score == 0) {
                        output += "<span>" + unformattedWord + "</span> ";
                    }
                    else if (score < 0.2) {
                        output += "<span class='highlight-green-1'>" + unformattedWord + "</span> ";
                    }
                    else if (score < 0.4) {
                        output += "<span class='highlight-green-2'>" + unformattedWord + "</span> ";
                    }
                    else if (score < 0.6) {
                        output += "<span class='highlight-green-3'>" + unformattedWord + "</span> ";
                    }
                    else if (score < 0.8) {
                        output += "<span class='highlight-green-4'>" + unformattedWord + "</span> ";
                    }
                    else {
                        output += "<span class='highlight-green-5'>" + unformattedWord + "</span> ";
                    }
                }
                else {
                    output += "<span>" + unformattedWord + "</span> ";
                }
            });
        }
        // print the highlighted text to the webpage
        document.getElementById("output").innerHTML = output;
        // Display the output row
        document.getElementById("output_row").className = "row bg-light p-3 rounded mt-2";
        // Hide the loading spinner
        document.getElementById("loading").className = "d-none";
    });
}
// searches through a list of words and attention scores and returns the attention score associated with the word
function getAttentionScore(word, attentionScores) {
    for (let index = 0; index < attentionScores.length; index++) {
        const element = attentionScores[index];
        if (word.toLowerCase() == element[0]) {
            return element[1];
        }
    }
    return 0;
}
