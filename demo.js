fetch("http://127.0.0.1:5000/api/login",
{
    method: "POST", 
    headers: {
        "Content-Type": "application/json",
      }
}).then((response) => { return response.json()
    // if (response.ok) {
    //   return response.json();
    // } else {
    //   // return response;
    //   throw new Error("Invalid username or password");
    // }
}
)