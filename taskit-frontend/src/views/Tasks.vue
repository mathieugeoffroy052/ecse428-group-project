<template>
  <el-container class="viewtasks" style="height: 100vh">
    <el-container>
      <el-header>
        <div class="logo">
          <el-button class="logobutton" type="text">TaskIt</el-button>
        </div>
        <div class="options">
          <el-button class="logout" color="#ccbfff" @change="onLogOut()"
            >Logout</el-button
          >
        </div>
        <div class="avatar">
          <el-avatar :size="40" :src="circleUrl"></el-avatar>
        </div>
        <div class="username">email123@email.email</div>
      </el-header>
      <el-container>
        <el-aside width="300px">
          <div class="card">
            <span>Lists</span>
            <el-divider content-position="center">o</el-divider>
          </div>
        </el-aside>
        <el-main>
          <div class="maincard">
            <span>Current Task List</span>
            <el-divider content-position="center">o</el-divider>

            <el-table
              :data="tableData"
              stripe
              border
              row-style="color:black"
              header-row-style="color:#9277ff"
            >
              <el-table-column prop="taskName" label="Task Name" />
              <el-table-column prop="priority" label="Priority" />
              <el-table-column prop="length" label="Length" />
              <el-table-column prop="category" label="Category" />
              <el-table-column prop="state" label="State" />
              <!-- <el-table-column fixed="right" label="Operations" >
              <template #default>
                <el-button type="text" size="small" @click="handleClick"
                  >Detail</el-button
                >
                <el-button type="text" size="small">Edit</el-button>
              </template>
            </el-table-column> -->
            </el-table>

            <el-button class="addtaskbutton" circle @click="drawer = true"
              >+</el-button
            >
            <el-drawer
              v-model="drawer"
              title="I am the title"
              :with-header="false"
            >
              <span>Create New Task</span>
              <el-form @submit.prevent="handleSubmit" :model="signUpForm">
                <h1>TaskIt</h1>
                <el-row>
                  <el-divider style="margin: 0px; padding: 0px"
                    >New Task
                  </el-divider>
                </el-row>
                <el-row justify="center">
                  <p
                    style="
                      font-family: 'Noteworthy Light';
                      font-style: italic;
                      padding-bottom: 10px;
                    "
                  >
                    Please fill in this form to create a new task.
                  </p>
                </el-row>

                <el-row>
                  <el-label class="required" for="email"
                    ><b>Task Name</b></el-label
                  >
                </el-row>
                <el-row>
                  <input
                    type="email"
                    placeholder="Enter Task Name"
                    name="email"
                    id="email"
                    required
                  />
                </el-row>

                <el-row>
                  <label class="required" for="pswd"><b>Task Length</b></label>
                </el-row>
                <el-row>
                  <input
                    type="password"
                    placeholder="Enter Task Length"
                    name="pswd"
                    id="pswd"
                    required
                  />
                </el-row>
                <el-row>
                  <label class="required" for="pswd"><b>Due Date</b></label>
                </el-row>
                <el-row>
                  <el-date-picker
                    v-model="value1"
                    style="height: 42px"
                    type="date"
                    placeholder="Pick a day"
                  ></el-date-picker>
                </el-row>

                <el-row>
                  <label class="required" for="pswd-repeat"
                    ><b>Task Category</b></label
                  >
                </el-row>
                <el-row>
                  <input
                    type="password"
                    placeholder="Enter Task Category"
                    name="pswd-repeat"
                    id="pswd-repeat"
                    required
                  />
                </el-row>

                <div v-if="passwordError" class="error">
                  {{ passwordError }}
                </div>
                <hr />

                <div class="btn-group">
                  <button
                    type="submit"
                    class="submit"
                    style="border-radius: 10px; width: 30%"
                  >
                    Add Task
                  </button>
                </div>
              </el-form>
            </el-drawer>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script lang="js" setup>
  import axios from 'axios'

  const axios_instance = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL,
  });

  export default {
      name: 'Tasks',
      data () {
          return {
              drawer: false,
              tableData: [
                {taskName: "Reach Masters", priority: "1", length:"2 months", category: "mental health", state: "in progress"},
                {taskName: "Eat Food", priority: "2", length:"1 month", category: "mental health", state: "in progress"},
                {taskName: "School", priority: "3", length:"2 months", category: "!mentalhealth", state: "in progress"},
                {taskName: "Sleep", priority: "no", length:"2 months", category: "mental health", state: "in progress"}
                ],
              value1: ''
          }
      },
      methods: {
        onLogOut() {
          axios_instance
          .post("/logout")
          .then(
            window.location.href = '../login'
          )
        }
      }

  }
</script>
<style scoped>
  body {
    background-color: #ded5ff;
  }
  .viewtasks .el-header {
    position: relative;
    background-color: #9277ff;
    height: 10vh;
    color: var(--el-text-color-primary);
  }

  .viewtasks .card {
    border-style: solid;
    border-radius: 5px;
    border-color: #9277ff;
    background-color: white;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 20px;
    width: 280px;
    height: 88vh;
    font-size: 20px;
    font-family: Futura, "Trebuchet MS";
    font-weight: bold;
    color: black;
  }

  .viewtasks .maincard {
    border-style: solid;
    border-radius: 5px;
    border-color: #9277ff;
    background-color: white;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 20px;
    height: 85vh;
    font-size: 20px;
    font-family: Futura, "Trebuchet MS";
    font-weight: bold;
    color: black;
  }

  .viewtasks .addtaskbutton {
    position: absolute;
    display: inline-flex;
    transform: translateY(-50%);
    font-size: 50px;
    background-color: #ffffff;
    border-color: #9277ff;
    border-width: 6px;
    color: #9277ff;
    height: 80px;
    width: 80px;
    font-style: normal;
    left: 90%;
    top: 85%;
  }

  .viewtasks .el-main {
    position: relative;
    background-color: #ffffff;
    height: 90vh;
  }

  .viewtasks .el-aside {
    position: relative;
    display: inline-flex;
    background-color: #ded5ff;
    height: 90vh;
    top: 10px;
    color: var(--el-text-color-primary);
  }

  .viewtasks .lists {
    position: relative;
    top: 20px;
    font-size: 20px;
    font-family: Futura, "Trebuchet MS";
    font-weight: bold;
    color: black;
  }
  .viewtasks .logo {
    position: absolute;
    display: inline-flex;
    left: 20px;
    top: 55%;
    transform: translateY(-50%);
    font-size: 50px;
    font-family: "Noteworthy Light";
    font-style: normal;
    color: white;
  }
  .viewtasks .logobutton {
    position: absolute;
    display: inline-flex;
    display: inline-flex;
    transform: translateY(-50%);
    font-size: 50px;
    font-family: "Noteworthy Light";
    font-style: normal;
    font-weight: bold;
    color: white;
  }
  .viewtasks .options {
    position: absolute;
    display: inline-flex;
    display: inline-flex;
    right: 110px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 50px;
    font-family: "Noteworthy Light";
    font-style: normal;
  }
  .viewtasks .logout {
    position: absolute;
    display: inline-flex;
    display: inline-flex;
    top: 50%;
    transform: translateY(-50%);
    font-size: 20px;
    font-family: Futura, "Trebuchet MS";
    font-weight: bold;
    color: black;
  }
  .viewtasks .avatar {
    position: absolute;
    display: inline-flex;
    display: inline-flex;
    top: 50%;
    transform: translateY(-50%);
    font-size: 20px;
    font-family: Futura, "Trebuchet MS";
    font-weight: bold;
    color: black;
    right: 130px;
  }
  .viewtasks .username {
    position: absolute;
    display: inline-flex;
    display: inline-flex;
    top: 50%;
    right: 190px;
    transform: translateY(-50%);
    font-size: 20px;
    font-family: Futura, "Trebuchet MS";
    font-weight: bold;
    color: rgb(255, 255, 255);
  }
</style>
