<template>
  <el-container class="viewtasks" style="height: 100vh">
    <el-container>
      <el-header>
        <div class="logo">
          <el-button class="logobutton" type="text">TaskIt</el-button>
        </div>
        <div class="options">
          <el-button class="logout" color="#ccbfff" @click="onLogOut()">
            Logout
          </el-button>
        </div>
        <div class="avatar"></div>
        <div class="username"></div>
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
            <el-button
              class="addtaskbutton"
              circle
              @click="add_task_drawer = true"
            >
              +
            </el-button>
            <el-table
              :data="tableData"
              height="55vh"
              stripe
              border
              style="color: black"
            >
              <el-table-column prop="description" label="Description" />
              <el-table-column prop="due_datetime" sortable label="Due Date" />
              <el-table-column
                prop="estimated_duration"
                sortable
                label="Duration"
              />
              <el-table-column prop="weight" sortable label="Weight" />\
              <el-table-column prop="notes" sortable label="Task Notes" />
              <el-table-column prop="state" fixed="right" label="State" />
              <el-table-column fixed="right" label="">
                <el-row justify="center">
                  <template #default="scope">
                    <el-button
                      color="#FF8989"
                      size="small"
                      circle
                      @click="onEditState(scope.$index, 'NS')"
                    >
                    </el-button>
                    <el-button
                      color="#FCFF89"
                      size="small"
                      circle
                      @click="onEditState(scope.$index, 'IP')"
                    >
                    </el-button>
                    <el-button
                      color="#9CFF89"
                      size="small"
                      circle
                      @click="onEditState(scope.$index, 'C')"
                    >
                    </el-button>
                  </template>
                </el-row>
              </el-table-column>
              <el-table-column fixed="right" label="Operations">
                <template #default="scope">
                  <el-button
                    size="small"
                    @click="
                      edit_drawer = true;
                      onEditTask();
                    "
                  >
                    Edit
                  </el-button>
                  <el-popconfirm
                    confirm-button-text="OK"
                    cancel-button-text="No, Thanks"
                    @confirm="onDeleteTask(scope.$index)"
                    icon-color="red"
                    title="Are you sure to delete this task?"
                    font-family="Noteworthy Light"
                  >
                    <template #reference>
                      <el-button size="small" type="danger"> Delete </el-button>
                    </template>
                  </el-popconfirm>
                </template>
              </el-table-column>
            </el-table>

            <el-drawer
              v-model="add_task_drawer"
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
                  <b>Task Description</b>
                </el-row>
                <el-row>
                  <input
                    type="taskName"
                    v-model="task_params.description"
                    placeholder="Enter Task Description"
                    required
                  />
                </el-row>
                <el-row>
                  <label class="required" for="pswd"
                    ><b>Task Due Date</b></label
                  >
                </el-row>
                <el-row style="padding-top: 15px">
                  <el-date-picker
                    v-model="task_params.due_datetime"
                    type="datetime"
                    placeholder="Select date and time"
                    style="
                      height: 45px;
                      width: 600px;
                      background-color: #eeeeee;
                      padding-top: 7px;
                    "
                    value-format="YYYY-MM-DDThh:mm"
                  >
                  </el-date-picker>
                </el-row>

                <el-row style="padding-top: 15px">
                  <label class="required" for="pswd"
                    ><b>Task Duration</b></label
                  >
                </el-row>
                <el-row style="padding-bottom: 15px">
                  <el-time-picker
                    arrow-control
                    v-model="task_params.estimated_duration"
                    placeholder="Enter Task Duration"
                    value-format="hh:mm:ss"
                    style="
                      height: 45px;
                      width: 600px;
                      background-color: #eeeeee;
                      padding-top: 7px;
                    "
                  >
                  </el-time-picker>
                </el-row>

                <el-row>
                  <label class="required" for="pswd-repeat"
                    ><b>Task Weight</b></label
                  >
                </el-row>
                <el-row>
                  <el-input-number v-model="task_params.weight" :min="1" />
                </el-row>
                <el-row style="padding-top: 15px">
                  <b>Task Notes</b>
                </el-row>
                <el-row>
                  <input
                    type="taskNotes"
                    v-model="task_params.notes"
                    placeholder="Enter Task Notes/Details"
                    maxlength="200"
                  />
                </el-row>
                <hr />
                <div>
                  <el-button
                    type="submit"
                    class="submit"
                    style="border-radius: 10px; width: 30%"
                    @click="onAddTask()"
                  >
                    Add Task
                  </el-button>
                </div>
                <div style="width: 395px; margin: auto; padding: 20px">
                  <el-alert
                    v-if="showError"
                    type="error"
                    @close="this.showError = false"
                    >{{ error }}</el-alert
                  >
                </div>
              </el-form>
            </el-drawer>
            <el-drawer
              v-model="edit_drawer"
              title="I am the title2"
              :with-header="false"
            >
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

<script>
import axios from "axios";

const axios_instance = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL,
});
export default {
  name: "Tasks",
  data() {
    return {
      task_params: {
        description: "",
        due_datetime: "",
        estimated_duration: "",
        weight: "",
        notes: "",
        state: "NS",
      },
      task_state: {
        state: "",
      },
      delete_task: {
        id: "",
      },
      state: "",
      username: "",
      add_task_drawer: false,
      edit_drawer: false,
      error: "",
      showError: false,
      options: [
        {
          value: "NS",
          label: "Not Started",
        },
        {
          value: "IP",
          label: "In Progress",
        },
        {
          value: "CP",
          label: "Complete",
        },
      ],
      tableData: [],
    };
  },
  created: function () {
    this.username = localStorage.getItem("token");
    axios_instance
      .get("/api/tasks/", {
        headers: {
          Authorization: "Token " + localStorage.getItem("token"),
        },
      })
      .then((response) => {
        this.tableData = response.data.sort((a, b) =>
          a.priority < b.priority ? 1 : -1
        );
      })
      .catch(() => {
        alert("You are not logged in!");
        window.location.href = "../login";
      });
  },
  methods: {
    onLogOut() {
      axios_instance
        .post(
          "/accounts/logout/",
          {},
          {
            headers: {
              Authorization: "Token " + localStorage.getItem("token"),
            },
          }
        )
        .then(() => {
          localStorage.removeItem("token");
          window.location.href = "../login";
        });
    },
    onAddTask() {
      if (this.task_params.task_description != "") {
        axios_instance
          .post("/api/tasks/", this.task_params, {
            headers: {
              Authorization: "Token " + localStorage.getItem("token"),
            },
          })
          .then((response) => {
            (this.error = response), location.reload(true);
          })
          .catch(() => {
            this.error = "Error creating task";
            this.showError = true;
          });
      } else {
        this.error = "Tasks must have a description!";
        this.showError = true;
      }
    },
    onDeleteTask: function (id) {
      var new_id = this.tableData[id]["id"];
      this.delete_task.id = new_id;
      axios_instance
        .delete("/api/tasks/", {
          headers: {
            Authorization: "Token " + localStorage.getItem("token"),
          },
          data: this.delete_task,
        })
        .then(alert("Deleted Successfully!"));
      location.reload(true);
    },
    onEditTask() {
      this.test = "";
    },
    onEditState: function (id, state) {
      this.task_state.state = state;
      var new_id = this.tableData[id]["id"];
      axios_instance
        .put("/api/update-state/" + new_id, this.task_state, {
          headers: {
            Authorization: "Token " + localStorage.getItem("token"),
          },
        })
        .then(alert("Edited Successfully!"));
      location.reload(true);
    },
  },
};
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
input[type="taskName"],
input[type="taskLength"],
input[type="taskCategory"],
input[type="taskNotes"] {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  display: inline-block;
  border: none;
  background: #f1f1f1;
}
</style>
