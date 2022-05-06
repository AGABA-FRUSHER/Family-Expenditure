const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

const handleToggleInput = (e)=>{
    if(showPasswordToggle.textContent==="SHOW-PASSWORD"){
        showPasswordToggle.textContent="HIDE-PASSWORD";
        passwordField.setAttribute("type","text");
    }else {
        showPasswordToggle.textContent="SHOW-PASSWORD";
        passwordField.setAttribute("type","password");
        }

    };



showPasswordToggle.addEventListener("click", handleToggleInput);


emailField.addEventListener("keyup",(e)=>{
console.log("777",777);
const emailVal = e.target.value;

emailSuccessOutput.textContent = "checking email";
emailSuccessOutput.style.display = "block"

emailField.classList.remove("is-invalid");
emailFeedBackArea.style.display="none";

    if(emailVal.length > 0){
        fetch("/authentication/validate-email",{
        body:JSON.stringify({email:emailVal}),method:"POST",
        })
         .then((res)=> res.json())
         .then((data)=> {
         console.log("data",data);
         emailSuccessOutput.style.display = "none"
      if(data.email_error){
        submitBtn.disabled=true;
        emailField.classList.add("is-invalid");
        emailFeedBackArea.style.display="block";
        emailFeedBackArea.innerHTML = '<p>email is invalid</p>'
      }else submitBtn.removeAttribute("disabled");

    });

  }

});


usernameField.addEventListener("keyup",(e)=>{
console.log("777",777);
const usernameVal = e.target.value;

usernameSuccessOutput.textContent = "checking username";
 usernameSuccessOutput.style.display = "block"

usernameField.classList.remove("is-invalid");
feedBackArea.style.display="none";

    if(usernameVal.length > 0){
        fetch("/authentication/validate-username",{
        body:JSON.stringify({username:usernameVal}),method:"POST",
        })
         .then((res)=> res.json())
         .then((data)=> {
         console.log("data",data);
         usernameSuccessOutput.style.display = "none"
      if(data.username_error){
        submitBtn.disabled=true;
        usernameField.classList.add("is-invalid");
        feedBackArea.style.display="block";
        feedBackArea.innerHTML = '<p>username should only contain alphanumeric characters</p>'
      }else submitBtn.removeAttribute("disabled");

    });

  }

});