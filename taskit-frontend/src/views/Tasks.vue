<template>
  <el-container>
    <el-main>
      <div>
        hi
      </div>
      
    </el-main>
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
              task_params : {
                description: "",
                due_datetime: "",
                estimated_duration: "",
                weight: "",
                state: "NS"
              },
              task_state : {
                state: ""
              },
              delete_task : {
                id: ""
              },
              state: '',
              username: '',
              add_task_drawer: false,
              edit_drawer: false,
              error: "",
              showError: false,
              options: [{
                value: 'NS',
                label: 'Not Started',
              },
              {
                value: 'IP',
                label: 'In Progress',
              },
              {
                value: 'CP',
                label: 'Complete',
              }
              ],
              tableData: [],
          }
      },
      created: function () {
        this.username = localStorage.getItem("token")
        axios_instance
          .get("/api/tasks/", {
              headers: {
                'Authorization': 'Token ' + localStorage.getItem("token")
                }})
          .then(response => {
            this.tableData = response.data.sort((a,b) => (a.priority < b.priority) ? 1 : -1)
          })
          .catch(() => {
              alert("You are not logged in!")
              window.location.href = "../login"
            })
      },
      methods: {
        onLogOut() {
          axios_instance
            .post('/accounts/logout/', {}, {
              headers: {
                'Authorization': 'Token ' + localStorage.getItem("token")
                }})
            .then(() => {
              localStorage.removeItem("token");
              window.location.href = "../login";
            })
        },
        onAddTask() {
          if(this.task_params.task_description != ""){
            axios_instance
              .post('/api/tasks/', this.task_params, {
                headers: {
                  'Authorization': 'Token ' + localStorage.getItem("token")
                  }})
              .then(response => {
                this.error = response,
                location.reload(true)
                })
              .catch(() => {
                this.error = "Error creating task";
                this.showError = true;
              })
          } else {
            this.error = "Tasks must have a description!";
            this.showError = true;
          }
        },
        onDeleteTask: function(id) {
          var new_id = this.tableData[id]["id"]
          this.delete_task.id = new_id;
          axios_instance
          .delete('/api/tasks//', {
            headers: {
            'Authorization': 'Token ' + localStorage.getItem("token")
            },
            data: this.delete_task
          })
            .then(alert("Deleted Successfully!"))
          location.reload(true)
        },
        onEditTask() {
          this.test = ''
        },
        onEditState: function (id, state) {
          this.task_state.state = state
          var new_id = this.tableData[id]["id"]
          axios_instance
          .put('/api/update-state/' + new_id, this.task_state, 
          {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem("token")
            }})
            .then(alert("Edited Successfully!"))
          location.reload(true)
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
