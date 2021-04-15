@app.route('/tags_click', methods=["POST"])
def tagclick():
    req = request.get_json() #convert json object into python dict
    print(req)

    res = make_response(jsonify({"message": "JSON received"}), 200)
    return res

fetch(`${window.origin}/tags_click`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(object),
    cache: "no-cache",
    headers: new Headers({
        "content-type": "application/json"
    })
})
.then(function (response) {
    if (response.status !== 200) {
        console.log('Response status was not 200: ${response.status}');
        return ;
    }
    response.json().then(function (data) {
        console.log(data)
    })
})

https://www.youtube.com/watch?v=QKcVjdLEX_s&t=27s
