<template>
 <form @submit.prevent="handleSubmit">
  <h1>TaskIt</h1>
  <div class="container">
    <h2>Sign Up</h2>
    <p>Please fill in this form to create an account.</p>
    <hr>

    <label for="firstname"><b>First Name</b></label>
    <input type="text" placeholder="Enter First Name" name="fName" id="fName" required>

    <label for="lastName"><b>Last Name</b></label>
    <input type="text" placeholder="Enter Last Name" name="lName" id="lName" required>

    <label for="email"><b>Email</b></label>
    <input type="email" placeholder="Enter Email" name="email" id="email" required>

    <label for="pswd"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="pswd" id="pswd" required>

    <label for="pswd-repeat"><b>Re-type Password</b></label>
    <input type="password" placeholder="Repeat Password" name="pswd-repeat" id="pswd-repeat" required>
    <div v-if="passwordError" class="error">{{ passwordError }} </div>
    <hr>

    <div class="btn-group">
      <button onclick="location.href='../'" type="back" class="backbtn" style="border-radius: 10px; width: 20%">Back</button>
      &ensp;
      <button type="submit" class="submit" style="border-radius: 10px; width: 20%">Sign Up</button>
    </div>
  </div>

  <div class="signin">
    <p>Already have an account? <a href="#">Log in</a>.</p>
  </div>
</form>
</template>

<script>
export default{
    data() {
        return {
            email: '',
            password: '',
            firstName: '',
            lastName: '',
            passwordError: ''
        }
    },
    methods: {
        handleSubmit() {
            var pswd = document.getElementById("pswd").value;
            var pswdRepeat = document.getElementById("pswd-repeat").value;
            console.log(pswd);
            console.log(pswdRepeat);
            this.passwordError = pswd === pswdRepeat ? '' : 'Passwords do not match';
        }
    }
}
</script>


<style>
  * {box-sizing: border-box}
  body{
    background-color: rgba(146, 119, 255, 0.28);
    padding-right: 150px;
    padding-left: 150px;
  }

  .container {
    border: 5px solid rgba(146, 119, 255, 1);
    padding-right: 16px;
    padding-left: 16px;
    border-radius: 10px;
  }

  input[type=text], input[type=password], input[type=email] {
    width: 100%;
    padding: 15px;
    margin: 5px 0 22px 0;
    display: inline-block;
    border: none;
    background: #f1f1f1;
  }

  input[type=text]:focus, input[type=password]:focus {
    background-color: #ddd;
    outline: none;
  }

  hr {
    border: 1px solid #f1f1f1;
    margin-bottom: 25px;
  }

  .backbtn {
    background-color: rgba(146, 119, 255, 0.5);
    color: white;
    padding: 16px 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    opacity: 0.9;
  }

  .submit {
    background-color:rgba(146, 119, 255, 1);
    color: white;
    padding: 16px 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    opacity: 0.9;
  }

  .submit:hover {
    opacity:1;
  }

  a {
    color: dodgerblue;
  }

  .error {
    color: #ff0000;
    font-size: 14px;
    font-weight: bold;
}
</style>