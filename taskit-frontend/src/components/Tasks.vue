<template>
  <el-container class="viewtasks" style="height: 100vh">
    <el-container>
      <el-header>
        <div class="logo">
          <el-button class="logobutton" type="text">TaskIt</el-button>
        </div>
        <div>
          <el-button class="logout" @click="(disable1 = true), (visibility1 = false), (tutorial_four = true), (tutorial_three = false)" v-if="tutorial_three"
            >Next Step
          </el-button>
          <el-dialog
            v-model="tutorial_one"
            title="Welcome!"
            width="30%"
          >
            <span>Welcome to TaskIt! Would you like to view a quick tutorial?</span>
            <template #footer>
              <span class="dialog-footer">
                <el-popconfirm
                            confirm-button-text="OK"
                            cancel-button-text="No, Thanks"
                            @confirm="hasSeen()"
                            icon-color="red"
                            title="Are you sure want to skip the tutorial?"
                            font-family="Noteworthy Light"
                          >
                <template #reference>
                  <el-button>Skip Tutorial</el-button>
                </template>
                </el-popconfirm>
                <el-button type="primary" @click="(tutorial_one = false), (tutorial_two = true)"
                  >Yes</el-button
                >
              </span>
            </template>
          </el-dialog>
          <el-dialog
            v-model="tutorial_two"
            title="Let's Get Started!"
            width="30%"
          >
            <span>Here are a few things to know before we start. Click the 'Next Step' button when you are ready to move forward.</span>
            <template #footer>
              <span class="dialog-footer">
                <el-button type="primary" @click="(tutorial_two = false), (disable1 = false), (visibility1 = true), (tutorial_three = true)"
                  >Confirm</el-button
                >
              </span>
            </template>
          </el-dialog>
          <el-dialog
            v-model="tutorial_four"
            title="Creating a task"
            width="30%"
          >
            <span>You can create a new task by clicking the '+' at the bottom right of your screen.</span>
            <template #footer>
              <span class="dialog-footer">
                <el-button type="primary" @click="(tutorial_four = false), (tutorial_five = true)"
                  >Confirm</el-button
                >
              </span>
            </template>
          </el-dialog>
          <el-dialog
            v-model="tutorial_five"
            title="Creating a task list"
            width="30%"
          >
            <span>You can create a new list by clicking the 'New Task List' botton on the left side of your screen.</span>
            <template #footer>
              <span class="dialog-footer">
                <el-button type="primary" @click="(tutorial_five = false), (tutorial_six = true)"
                  >Confirm</el-button
                >
              </span>
            </template>
          </el-dialog>
          <el-dialog
            v-model="tutorial_six"
            title="Editing ad Deleting a Task"
            width="30%"
          >
            <span>Once a task is created, you can edit and delete it.</span>
            <template #footer>
              <span class="dialog-footer">
                <el-button type="primary" @click="(tutorial_six = false), (tutorial_seven = true)"
                  >Confirm</el-button
                >
              </span>
            </template>
          </el-dialog>
          <el-dialog
            v-model="tutorial_seven"
            title="Editing and Deleting a List"
            width="30%"
          >
            <span>Once a list is created, you can edit and delete it. You can change the name of a list by double clicking on it. To delete, click the delete button in the task </span>
            <template #footer>
              <span class="dialog-footer">
                <el-button type="primary" @click="(tutorial_seven = false), (tutorial_eight = true)"
                  >Confirm</el-button
                >
              </span>
            </template>
          </el-dialog>
          <el-dialog
            v-model="tutorial_eight"
            title="The End"
            width="30%"
          >
            <span>The tutorial is now over! You can now proceed to tasking! </span>
            <template #footer>
              <span class="dialog-footer">
                <el-button type="primary" @click="(tutorial_eight = false), hasSeen()"
                  >Confirm</el-button
                >
              </span>
            </template>
          </el-dialog>
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
            <el-tooltip
              class="box-item"
              :disabled="disable1"
              effect="dark"
              content="All of your lists"
              placement="right"
              :visible="visibility1"
            >
              <span>Lists</span>
            </el-tooltip>
            <el-divider content-position="center">o</el-divider>
              <el-table :data="listData" stripe border>
                <el-table-column prop="list_name" label="List Name">
                  <template v-slot="scope">
                    <el-row>
                      <el-space wrap>
                        <div v-on:dblclick="editTaskList(scope.row.id)" v-if="scope?.row && currentTasklist != scope?.row.id">
                          {{ scope.row.list_name }}
                        </div>
                        <div>
                          <el-input
                            v-if="scope?.row && currentTasklist === scope?.row.id"
                            v-model="scope.row.list_name"
                            v-on:keyup.enter="edit_task_list_name(scope.row)"
                          ></el-input>
                        </div>
                        <div>
                          <el-popconfirm
                            confirm-button-text="OK"
                            cancel-button-text="No, Thanks"
                            @confirm="onDeleteList(scope.$index)"
                            icon-color="red"
                            title="Are you sure to delete this list?"
                            font-family="Noteworthy Light"
                          >
                            <template #reference>
                              <el-button type="danger" circle>
                                <el-icon >
                                  <delete/>
                                </el-icon>
                              </el-button>
                            </template>
                          </el-popconfirm>
                        </div>
                      </el-space>
                    </el-row>
                  </template>
                </el-table-column>
              </el-table>
            <el-button
              round
              class="addtasklistbutton"
              @click="add_task_list_drawer = true"
            >
              New Task List
            </el-button>
            <el-drawer
              v-model= "add_task_list_drawer"
              :direction= "direction"
              :with-header="false"
            >
              <span>Create New Task List</span>
              <el-form>
                <h1>TaskIt</h1>
                <el-row>
                  <el-divider style="margin: 0px; padding: 0px"
                    >New Task List
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
                    Please fill in this form to create a new task list.
                  </p>
                </el-row>

                <el-row>
                  <b>Task List Name</b>
                </el-row>
                <el-row>
                  <input
                    type="taskName"
                    v-model="task_list_params.list_name"
                    placeholder="Enter Task List Name"
                    required
                  />
                </el-row>
                <div>
                  <el-button
                    type="submit"
                    class="submit"
                    style="border-radius: 10px; width: 30%"
                    @click="onAddTaskList()"
                  >
                    Add Task List
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
          </div>
        </el-aside>
        <el-main>
          <div class="maincard">
            <el-tooltip
              :disabled="disable1"
              class="box-item"
              effect="dark"
              content="All of your current tasks"
              placement="right"
              :visible="visibility1"
            >
              <span>Current Task List</span>
            </el-tooltip>
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
              border
              style="color: black"
            >
              <el-table-column type="expand" width=40>
                <template #default="props">
                  <p>Duration: {{ props.row.estimated_duration }}</p>
                  <p>Weight: {{ props.row.weight }}</p>
                  <p>Notes: {{ props.row.notes }}</p>
                </template>
              </el-table-column>
              <el-table-column prop="description" label="Description" />
              <el-table-column prop="due_datetime" sortable label="Due Date" width=230 />
              <el-table-column label="" width=150>
                <template #default="scope">
                  <el-row justify="center">
                    <el-dropdown
                      trigger="click"
                      @command="(option) => onEditState(scope.$index, option)"
                    >
                      <el-button type="default">
                        {{ taskStateOptions[scope.row.state] }}
                        <el-icon class="el-icon--right">
                          <arrow-down />
                        </el-icon>
                      </el-button>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item command="NS">
                            {{ taskStateOptions["NS"] }}
                          </el-dropdown-item>
                          <el-dropdown-item command="IP">
                            {{ taskStateOptions["IP"] }}
                          </el-dropdown-item>
                          <el-dropdown-item command="C">
                            {{ taskStateOptions["C"] }}
                          </el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </el-row>
                </template>
              </el-table-column>
              <el-table-column label="Operations" width=150>
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
                    v-model="task_params.estimated_duration"
                    placeholder="Enter Task Duration"
                    value-format="HH:mm:ss"
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
import { ArrowDown, Delete } from "@element-plus/icons-vue";

const axios_instance = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL,
  headers: {
    Authorization: "Token " + localStorage.getItem("token"),
  },
});

export default {
  name: "Tasks",
  components: {
    ArrowDown,
    Delete,
  },
  data() {
    return {
      currentTasklist: "",
      task_params: {
        description: "",
        due_datetime: "",
        estimated_duration: "",
        weight: "",
        notes: "",
        state: "NS",
      },
      task_list_params: {
        list_name: "",
      },
      task_state: {
        state: "",
      },
      delete_task: {
        id: "",
      },
      delete_list:{
        id: "",
      },
      state: "",
      username: "",
      add_task_drawer: false,
      edit_drawer: false,
      add_task_list_drawer: false,
      error: "",
      direction: "ltr",
      showError: false,
      taskStateOptions: {
        NS: "Not Started",
        IP: "In Progress",
        C: "Completed",
      },
      tableData: [],
      tutorial_one: (sessionStorage.getItem("hasSeenTutorial").toLowerCase() === "false"),
      tutorial_two: false,
      tutorial_three:false,
      tutorial_four: false,
      tutorial_five: false,
      tutorial_six: false,
      tutorial_seven: false,
      tutorial_eight: false,
      tutorial_nine: false,
      tutorial_ten: false,
      disable1: true,
      visibility1: false,
      listData: [],
    };
  },
  created: function () {
    this.username = localStorage.getItem("token");
    axios_instance
      .get("/api/tasks/")
      .then((response) => {
        this.tableData = response.data.sort((a, b) =>
          a.priority < b.priority ? 1 : -1
        );
        for (var i = 0; i < this.tableData.length; i++) {
            const date = new Date(this.tableData[i]["due_datetime"]);
            this.tableData[i]["due_datetime"] = date.toLocaleString();
        }
      })
      .catch(() => {
        alert("You are not logged in!");
        window.location.href = "../login";
      });
    axios_instance
      .get("/api/task_list/")
      .then((response) => {
        this.listData = response.data.sort();
      })
      .catch(() => {
        alert("You are not logged in!");
        window.location.href = "../login";
      });
  },
  methods: {
    hasSeen() {
      this.tutorial_one = false;
      sessionStorage.setItem("hasSeenTutorial", true);
    },
    onLogOut() {
      axios_instance.post("/accounts/logout/", {}).then(() => {
        localStorage.removeItem("token");
        window.location.href = "../login";
      });
    },
    onAddTask() {
      if (this.task_params.task_description != "") {
        axios_instance
          .post("/api/tasks/", this.task_params)
          .then((response) => {
            this.error = response;
            location.reload(true);
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
    onAddTaskList() {
      if (this.task_list_params.list_name != "") {
        axios_instance
          .post("/api/task_list/", this.task_list_params)
          .then((response) => {
            this.error = response;
            location.reload(true);
          })
          .catch(() => {
            this.error = "Error creating task list";
            this.showError = true;
          });
      } else {
        this.error = "Task list must have a name!";
        this.showError = true;
      }
    },
    onDeleteList: function (id) {
      var new_id = this.listData[id]["id"];
      this.delete_list.id = new_id;
      axios_instance.delete("/api/task_list/", {data: this.delete_list})
        .then(alert("Deleted Successfully!"));
      location.reload(true);
    },
    onDeleteTask: function (id) {
      var new_id = this.tableData[id]["id"];
      this.delete_task.id = new_id;
      axios_instance
        .delete("/api/tasks/", {data: this.delete_task})
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
        .put("/api/update-state/" + new_id, this.task_state)
        .then(alert("Edited Successfully!"));
      location.reload(true);
    },
    editTaskList(tasklistId) {
      this.currentTasklist = tasklistId
    },
    edit_task_list_name({id, list_name}) {
      axios_instance
        .put("/api/edit-name/" + id, { list_name: list_name })
        .then((response) => {
          console.log(response)
          this.currentTasklist = ""
        });
      }
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

.viewtasks .addtasklistbutton {
  display: inline-flex;
  transform: translateY(+50%);
  font-size: 15px;
  background-color: #ffffff;
  border-color: #9277ff;
  border-width: 2px;
  font-family: Futura, "Trebuchet MS";
  color: #9277ff;
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
