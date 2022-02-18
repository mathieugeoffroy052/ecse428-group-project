<template>
  <el-container>
    <el-main>
      <el-row>
        <div class="card">
          <h1>Taskit</h1>
          <el-row>
            <el-divider style="margin: 0px; padding: 0px; padding-bottom: 20px"
              >Log In</el-divider
            >
          </el-row>
          <el-form label-position="top" :model="logInForm">
            <el-form-item label="Email:" required>
              <el-input placeholder="Email" v-model="logInForm.email" />
            </el-form-item>
            <el-form-item label="Password:" required>
              <el-input
                type="password"
                placeholder="Password"
                show-password
                v-model="logInForm.password"
              />
            </el-form-item>
          </el-form>
          <el-row justify="space-between">
            <el-button
              color="#9277FF"
              plain
              class="main-button"
              @submit="onLogIn()"
              >Log In</el-button
            >
            <el-button color="#9277FF" style="color: white" class="main-button"
              >Sign Up</el-button
            >
          </el-row>
        </div>
      </el-row>
        <div style="width:395px; margin:auto; padding:20px">
          <el-alert
          v-if="showError"
          title="Invalid log in attempt"
          type="error"
          show-icon
        >{{error}}</el-alert>
        </div>
    </el-main>
  </el-container>
</template>

<script>
import axios from "axios";

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
      axios ({
          method: 'post',
          url: 'http://127.0.0.1:8000/login/',
          data: {
              'username': this.logInForm.email,
              'password': this.logInForm.password
          }
      }).catch( e => {
          this.error = e.response.data.message;
          this.showError = true;
      })
    },
  },
};
</script>

<style>
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
  width: 165px;
  padding-bottom: 0px;
}
</style>
