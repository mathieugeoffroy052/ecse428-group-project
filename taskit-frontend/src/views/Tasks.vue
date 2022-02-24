<template>
  <el-container class="viewtasks" style="height: 100vh">
    <el-container>
      <el-header>
        <div class="logo">
          <el-button class="logobutton" type="text">TaskIt</el-button>
        </div>
        <div class="options">
          <el-button class="logout" color="#ccbfff" @click="onLogOut()"
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
            <el-button class="addtaskbutton" circle @click="drawer = true"
              >+</el-button
            >
            <el-table
              :data="tableData"
              height= "55vh"
              stripe
              border
              row-style="color:black"
              header-row-style="color:#9277ff"
              
            >
              <el-table-column prop="taskName" label="Task Name" />
              <el-table-column prop="priority" sortable label="Priority" />
              <el-table-column prop="length" sortable label="Length" />
              <el-table-column prop="category" label="Category" />
              <el-table-column prop="state" label="State">
                
              </el-table-column>
              <el-table-column fixed="right" label="Operations" >
              <template #default = "scope">
                <el-button size="small" @click="drawer2 = true; onEditTask()"
                  >Edit</el-button
                >
                <el-popconfirm
                  confirm-button-text="OK"
                  cancel-button-text="No, Thanks"
                  @confirm="onDeleteTask(scope.$index, scope.row.taskName)"
                  :icon="InfoFilled"
                  icon-color="red"
                  title="Are you sure to delete this task?"
                  font-family = "Noteworthy Light"
                >
                <template #reference>
                  <el-button
                    size="small"
                    type="danger"
                    @click="handleDelete(scope.$index, scope.row)"
                    >Delete</el-button
                  >
                </template>
                </el-popconfirm>
                
              </template>
            </el-table-column>
            </el-table>
            
            
            <el-drawer
              v-model="drawer"
              title="I am the title"
              :with-header="false"
            >
              <span>Create New Task</span>
              <el-form @submit.prevent="handleSubmit" :model="addTaskForm">
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
                  <el-label class="required" for="taskName"
                    ><b>Task Name</b></el-label
                  >
                </el-row>
                <el-row>
                  <input
                    type="taskName"
                    v-model="taskName"
                    placeholder="Enter Task Name"
                    required
                  />
                </el-row>
                <el-row>
                  <label class="required" for="pswd"><b>Task Priority</b></label>
                </el-row>
                <el-row>
                  <input
                    type="taskName"
                    v-model="priority"
                    placeholder="Enter Task Priority"
                    required
                  />
                </el-row>


                <el-row>
                  <label class="required" for="pswd"><b>Task Length</b></label>
                </el-row>
                <el-row>
                  <input
                    type="taskLength"
                    v-model="length"
                    placeholder="Enter Task Length"
                    required
                  />
                </el-row>

                <el-row>
                  <label class="required" for="pswd-repeat"
                    ><b>Task Category</b></label
                  >
                </el-row>
                <el-row>
                  <input
                    type="taskCategory"
                    v-model="category"
                    placeholder="Enter Task Category"
                    required
                  />
                </el-row>

                <div v-if="passwordError" class="error">
                  {{ passwordError }}
                </div>
                <hr />

                <div>
                  <el-button
                    type="submit"
                    class="submit"
                    style="border-radius: 10px; width: 30%"
                    @click = "onAddTask(taskName,priority,length,category)"
                  >
                    Add Task
                  </el-button>
                </div>
              </el-form>
            </el-drawer>
            <el-drawer
              v-model="drawer2"
              title="I am the title2"
              :with-header="false"
            >
            <el-row justify="center">
              <span>Edit State</span>
              <el-divider content-position="center">o</el-divider>
              
                <el-select v-model="state" class="m-2" placeholder="Select" size="large">
                    <el-option
                      v-for="item in options"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
                  </el-row>
                  <el-row justify="center">
                  <el-button
                    type="submit"
                    class="submit"
                    style="border-radius: 10px; width: 30%; height: 30px"
                    @click = "onEditState(state)"
                    
                  >
                    Edit State
                  </el-button>
                  </el-row>
              
            
            
            <el-row justify="center">
              <span>Edit Task</span>
              <el-divider content-position="center">o</el-divider>
              </el-row>
                
               
              <el-divider content-position="center">o</el-divider>
           
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
              taskName: '',
              priority: '',
              length: '',
              category: '',
              state: '',
              value: '',
              test: '',
              drawer: false,
              drawer2: false,
              options: [{
                value: 'toDo',
                label: 'To Do',
              },
              {
                value: 'inProgress',
                label: 'In Progress',
              },
              {
                value: 'finished',
                label: 'Finished',
              }
              
              ],
              tableData: [
                {taskName: "Reach Masters", priority: "1", length:"2 months", category: "mental health", state: "in progress"},
                {taskName: "Eat Food", priority: "2", length:"1 month", category: "mental health", state: "in progress"},
                {taskName: "School", priority: "3", length:"2 months", category: "!mentalhealth", state: "in progress"},
                {taskName: "Sleep", priority: "no", length:"2 months", category: "mental health", state: "in progress"},
                {taskName: "Reach Masters", priority: "1", length:"2 months", category: "mental health", state: "in progress"},
                {taskName: "Eat Food", priority: "2", length:"1 month", category: "mental health", state: "in progress"},
                {taskName: "School", priority: "3", length:"2 months", category: "!mentalhealth", state: "in progress"},
                {taskName: "Sleep", priority: "no", length:"2 months", category: "mental health", state: "in progress"},
                {taskName: "Reach Masters", priority: "1", length:"2 months", category: "mental health", state: "in progress"},
                {taskName: "Eat Food", priority: "2", length:"1 month", category: "mental health", state: "in progress"},
                {taskName: "School", priority: "3", length:"2 months", category: "!mentalhealth", state: "in progress"},
                {taskName: "Sleep", priority: "no", length:"2 months", category: "mental health", state: "in progress"}
                ],
              value1: '',
              tableDataReal: []
          }
      },
      created: function () {
        // axios.get('/view_all_tasks/')
        // .then(response => {
        //   this.tableData = response.data
        // })
        // .catch(e => {
        //   alert(e + " bruh")

        // })
      },
      methods: {
        onLogOut() {
          axios_instance
          .post("/logout")
          .then(
            window.location.href = '../test'
          )
        },
        onAddTask(name,prio,length,cate) {
          this.tableData.push({taskName: name, priority: prio, length: length, category: cate, state: "To Do"})
          axios.post('/addTask/')
            .then(alert("Task Added Successfully"))
        },
        onDeleteTask: function(id, name) {
          this.test = name
          this.tableData.splice(id,1)
          axios.post('/addTask/')
            .then(alert(this.test + " Deleted Successfully!"))
        },
        onEditTask() {
          this.test = ''
        },
        onEditState: function (state) {
          this.state = state
          alert("Edited Successfully!")
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
    height: 10vh;
    width: 10vh;
    font-style: normal;
    right: 8vh;
    bottom: 1vh;
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
  input[type=taskName], input[type=taskLength], input[type=taskCategory]{
    width: 100%;
    padding: 15px;
    margin: 5px 0 22px 0;
    display: inline-block;
    border: none;
    background: #f1f1f1;
  }

</style>
