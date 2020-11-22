var APISettings = (function () {
    function parseCSRFToken() {
        return $('#csrftoken > input').val();
    }
    
    return {
        apiBaseUrl: 'http://localhost:8000/api/'
        , csrf_token: parseCSRFToken()
    }
})();

var ClassificationApi = (function () {
    async function spamTest(emailText) {
        if (!emailText) {
            //alert('No emailText name in spamTest');
            return;
        }
        
        var jqXHR = $.ajax({
            type: 'POST'
            , async: true
            , url: APISettings.apiBaseUrl + 'spamtest'
            , headers: { "X-CSRFToken": APISettings.csrf_token }
            , xhrFields: {}
            , data: JSON.stringify({
                emailText: emailText
            })
            , contentType: 'application/json; charset=utf-8'
        });
    
        var promise = new Promise(function (resolve, reject) {
            jqXHR.done(function (data, textStatus, jqXHR) {
                resolve(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                // if (['abort', 'canceled'].indexOf(jqXHR.statusText || textStatus) === -1) {
                // }
                alert(jqXHR.responseJSON || jqXHR.responseText);
                reject(jqXHR);
            });
        });
    
        return promise;
    }

    async function spamOrHam(emailText) {
        if (!emailText) {
            alert('No emailText name in spamTest');
            return;
        }
        
        var jqXHR = $.ajax({
            type: 'POST'
            , async: true
            , url: APISettings.apiBaseUrl + 'spamorham'
            , headers: { "X-CSRFToken": APISettings.csrf_token }
            , xhrFields: {}
            , data: JSON.stringify({
                emailText: emailText
            })
            , contentType: 'application/json; charset=utf-8'
        });
    
        var promise = new Promise(function (resolve, reject) {
            jqXHR.done(function (data, textStatus, jqXHR) {
                resolve(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                // if (['abort', 'canceled'].indexOf(jqXHR.statusText || textStatus) === -1) {
                // }
                alert(jqXHR.responseJSON || jqXHR.responseText);
                reject(jqXHR);
            });
        });
    
        return promise;
    }

    return {
        spamTest: spamTest
        , spamOrHam: spamOrHam
    }
})();