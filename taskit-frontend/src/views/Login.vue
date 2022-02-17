<template>
    <el-container>
        <el-main>
        <el-row>
            <div class="card">
                <h1>Taskit</h1>
                <el-row>
                    <el-divider style="margin:0px; padding:0px; padding-bottom:20px">Log In</el-divider>
                </el-row>
                <el-form label-position="top">
                    <el-form-item label="Email:">
                        <el-input placeholder="Email"/>
                    </el-form-item>
                    <el-form-item label="Password:">
                        <el-input type="password" placeholder="Password"/>
                    </el-form-item>
                </el-form>
                <el-row justify="space-between">
                    <el-form-item>
                        <el-button color="#9277FF" plain class="main-button">Log In</el-button>
                    </el-form-item>
                    <el-button color="#9277FF" style="color: white" class="main-button">Sign Up</el-button>
                </el-row>
            </div>
        </el-row>
        </el-main>
    </el-container>
</template>

<script >

</script>

<style>
.card {
    border-style: solid;
    border-radius: 5px;
    border-color: #9277FF;
    background-color: white;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    padding-left: 20px;
    padding-right: 20px;
    padding-bottom: 20px;
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
    background-color: #9277FF47;
}
.main-button {
    width: 165px;
}
</style>