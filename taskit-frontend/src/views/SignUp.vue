<template>
<el-container>
    <el-main>
      <el-row>
        <div class="card">
        <el-form  label-position="top"  
                  @submit.prevent="handleSubmit" 
                  :model="signUpForm">
          <h1 style="padding: 5px; padding-bottom: 5px">
            TaskIt
          </h1>
            <el-row>
              <el-divider style="margin: 0px; padding: 0px; padding-bottom: 20px"
                >Sign Up
                </el-divider>
            </el-row>

           <el-form-item label="Email:" required> 
             <input type="email" 
                    v-model="email" 
                    pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$" 
                    oninvalid="this.setCustomValidity('Please enter a valid email address')"
                    oninput="this.setCustomValidity('')" 
                    placeholder="Enter Email" 
                    name="email" 
                    id="email" 
                    required> 
           </el-form-item>

           <el-form-item label="Password:" required> 
            <input  type="password" 
                    v-model="password" 
                    placeholder="Enter Password" 
                    name="pswd" 
                    id="pswd" 
                    required>
           </el-form-item>

           <el-form-item label="Re-type password:" required> 
             <input type="password" 
                    v-model="pswdRepeat" 
                    placeholder="Repeat Password" 
                    name="pswd-repeat" 
                    id="pswd-repeat" 
                    required>
           </el-form-item>
              
            <div v-if="passwordError" class="error">{{ passwordError }} </div>

            <button  type="submit" 
                        class="submit" 
                        style="border-radius: 4px;">
                        Sign Up
            </button>

          <el-row justify="center">
            <p>Already have an account? Head back to <a href="#" onclick="location.href='../login'"> login</a>.</p>
          </el-row>
        </el-form>
        </div>
      </el-row>
    </el-main>
</el-container>
</template>

<script>
import axios from "axios";
const axios_instance = axios.create({
    baseURL: process.env.VUE_APP_BACKEND_URL,
});

export default{
    data() {
        return {
        signUpForm: {},
        email: "",
        password: "",
        pswdRepeat: "",
        error: "",
        passwordError: false,
      };
    },
    methods: {
        handleSubmit() {
          if(this.password === this.pswdRepeat){
            this.signUpForm.email = this.email
            this.signUpForm.password = this.password
            this.passwordError = '';
            console.log("Sending email: " + this.signUpForm.email + " and password: " + this.signUpForm.password);

            axios_instance.post("/accounts/signup", this.signUpForm)
              .then(resp => console.log(resp.data))
              .catch(errors => console.log(errors))
            
            axios_instance.post("/accounts/login/", {
              "username": this.signUpForm.email,
              "password": this.signUpForm.password,
            })
              .then(response => {
                localStorage.setItem("token", response.data.token)
                if (response.data.expiry != "") {
                  window.location.href = "../tasks"
                }
              })
              .catch(() => {
                this.error = "Invalid log in attempt";
                this.showError = true;
              })
          } 
          else{
            this.passwordError = 'Passwords don\'t match'
            console.log("Form not submitted due to password mismatch");
          }
        }
    } 
}
</script>


<style>
  @import 'generalStyle.css';
  * {box-sizing: border-box; }

  h1 {
    font-family: var(--titleFont);
    font-size: 50px;
    padding: 0px;
    margin: 0px;
    font-style: normal;
  }
  .card {
    border-style: solid;
    border-radius: 5px;
    border-color: var(--lavender);
    background-color: white;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    padding-left: 20px;
    padding-right: 20px;
    padding-bottom: 10px;
    margin: 20px;
    width: 400px;
    margin: auto;
  }

  input[type=text], input[type=password], input[type=email] {
    width: 100%;
    padding: 15px;
    display: inline-block;
    border: none;
    background: var(--lightGray);
    border-radius:3px;
  }

  input[type=text]:focus, input[type=password]:focus, input[type=email]:focus {
    background-color: var(--darkGray);
    outline: none;
  }

  .submit {
    background-color: var(--lavender);
    font-size: 16px;
    color: white;
    padding: 12px 16px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    opacity: 0.9;
    width: 100px;
  }

  .submit:hover {
    opacity:1;
  }

  a {
    color: dodgerblue;
  }

  .error {
    color: red;
    font-size: 14px;
    font-weight: bold;
  }
</style>