<template>
  <el-container>
    <el-main>
      <el-row>
        <div class="card">
          <div style="display: flex; justify-content: center;">
            <h1 style="padding: 5px; padding-bottom: 5px" >TaskIt</h1>
            <div>
              <img style="margin-top: 35px" src="../assets/icon-dark.png" alt="checkbox icon"  width="32" height="32"/>
            </div>
          </div>
          <el-row>
            <el-divider style="margin: 0px; padding: 0px; padding-bottom: 20px"
              >Log In</el-divider
            >
          </el-row>
          <el-form
            label-position="top"
            :model="logInForm"
            @submit.prevent="onLogIn"
          >
            <el-form-item label="Email:" required>
              <input
                placeholder="Enter Email"
                type="email"
                v-model="logInForm.email"
                pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$"
                oninvalid="this.setCustomValidity('Please enter a valid email address')"
                oninput="this.setCustomValidity('')"
              />
            </el-form-item>
            <el-form-item label="Password:" required>
              <input
                type="password"
                placeholder="Enter Password"
                v-model="logInForm.password"
              />
            </el-form-item>
            <el-row justify="center">
              <button
                style="border-radius: 4px"
                type="submit"
                class="main-button"
                @submit="onLogIn()"
              >
                Log In
              </button>
            </el-row>
            <el-row justify="center">
              <p>
                Don't have an account? Head to
                <a href="#" onclick="location.href='../signup'"> sign up</a>.
              </p>
            </el-row>
          </el-form>
        </div>
      </el-row>
      <div style="width: 395px; margin: auto; padding: 20px">
        <el-alert
          v-if="showError"
          type="error"
          @close="this.showError = false"
          >{{ error }}</el-alert
        >
      </div>
    </el-main>
  </el-container>
</template>

<script>
import axios from "axios";

const axios_instance = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL,
});

export default {
  data() {
    return {
      logInForm: {
        email: "",
        password: "",
      },
      error: "",
      showError: false,
    };
  },
  methods: {
    onLogIn() {
      if (this.logInForm.email != "" && this.logInForm.password != "") {
        axios_instance
          .post("/accounts/login/", {
            username: this.logInForm.email,
            password: this.logInForm.password,
          })
          .then((response) => {
            localStorage.setItem("token", response.data.token);
            this.logInForm.email = "";
            this.logInForm.password = "";
            if (response.data.expiry != "") {
              window.location.href = "../tasks";
            }
          })
          .catch(() => {
            this.error = "Invalid log in attempt";
            this.showError = true;
          });
      } else {
        this.error = "Please fill in all input fields to login.";
        this.showError = true;
      }
    },
    onSignUpClick() {
      window.location.href = "../signup";
    },
  },
};
</script>

<style>
@import "../assets/generalStyle.css";
.card {
  border-style: solid;
  border-radius: 5px;
  border-color: #9277ff;
  background-color: white;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  padding-left: 20px;
  padding-right: 20px;
  padding-bottom: 10px;
  margin: 20px;
  width: 350px;
  margin: auto;
}
h1 {
  font-family: "Noteworthy Light";
  font-size: 50px;
  padding: 0px;
  margin: 0px;
  font-style: normal;
}
body {
  background-color: #9277ff47;
}
.main-button {
  background-color: #9277ff;
  padding: 12px 16px;
  width: 100px; /* was 165 */
  font-size: 16px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  opacity: 0.9;
  color: white;
}
.main-button:hover {
  opacity: 1;
}
a {
  color: dodgerblue;
}
input[type="text"],
input[type="password"],
input[type="email"] {
  width: 100%;
  padding: 15px;
  display: inline-block;
  border: none;
  background: #f1f1f1;
  border-radius: 3px;
}
input[type="text"]:focus,
input[type="password"]:focus,
input[type="email"]:focus {
  background-color: var(--darkGray);
  outline: none;
}
</style>
