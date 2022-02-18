<template>
<el-container>
    <el-main>
      <el-row>
        <div class="card">
        <el-form @submit.prevent="handleSubmit" :model="signUpForm">
          <h1>TaskIt</h1>
            <el-row>
              <el-divider style="margin: 0px; padding: 0px"
                >Sign Up
                </el-divider>
            </el-row>
            <el-row justify="center">
              <p style="font-family: 'Noteworthy Light'; font-style: italic;  padding-bottom: 10px">
                Please fill in this form to create an account.</p>
            </el-row>

            <el-row>
              <el-label class="required" for="email"><b>Email</b></el-label> </el-row>
            <el-row>
              <input type="email" placeholder="Enter Email" name="email" id="email" required> </el-row>

            <el-row>
              <label class="required" for="pswd"><b>Password</b></label> </el-row>
            <el-row>
            <input type="password" placeholder="Enter Password" name="pswd" id="pswd" required> </el-row>

            <el-row>
              <label class="required" for="pswd-repeat"><b>Re-type Password</b></label> </el-row>    
            <el-row>
              <input type="password" placeholder="Repeat Password" name="pswd-repeat" id="pswd-repeat" required> </el-row>
              
            <div v-if="passwordError" class="error">{{ passwordError }} </div>
            <hr>

            <div class="btn-group">
              <button onclick="location.href='../'" type="back" class="backbtn" style="border-radius: 10px; width: 30%">Back</button>
              &ensp;
              <button type="submit" class="submit" style="border-radius: 10px; width: 30%">Sign Up</button>
            </div>

          <div class="signin">
            <p>Already have an account? <a href="#" onclick="location.href='../login'">Log in</a>.</p>
          </div>
        </el-form>
        </div>
      </el-row>
    </el-main>
</el-container>
</template>

<script>
import axios from "axios";
export default{
    data() {
        return {
        signUpForm: {
          email: "",
          password: "",
        },
        error: "",
        passwordError: false,
      };
    },
    methods: {
        handleSubmit() {
            var email = document.getElementById("email").value;
            var pswd = document.getElementById("pswd").value;
            var pswdRepeat = document.getElementById("pswd-repeat").value;
            this.passwordError = pswd === pswdRepeat ? '' : 'Passwords do not match';
            console.log("Password error:" + this.passwordError);
            if(this.passwordError === ''){
              axios ({
                method: 'post',
                url: 'http://127.0.0.1:8000/signup/',
                data: {
                    'email': email,
                    'password': pswd
                }
              }).catch( e => {
                  this.error = e.response.data.message;
              })
              console.log("Sending email: " + email + " and password: " + pswd);
            } else{
              console.log("boooo");
            }
        }
    }
}
</script>


<style>
  * {box-sizing: border-box}

  .required:before {
    content:" *";
    color: red;
  }
  body{
    background-color: rgba(146, 119, 255, 0.28);
    padding-right: 150px;
    padding-left: 150px;
  }

  h1 {
    font-family: "Noteworthy Light";
    font-size: 50px;
    padding: 0px;
    margin: 0px;
    font-style: normal;
  }
  .card {
    border-style: solid;
    border-radius: 5px;
    border-color: #9277ff;
    background-color: white;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    padding-left: 20px;
    padding-right: 20px;
    padding-bottom: 20px;
    margin: 20px;
    width: 400px;
    margin: auto;
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