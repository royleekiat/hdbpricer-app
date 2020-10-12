<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color:azure;
  background-color:rgb(51, 104, 105);
}

#nav {
  text-align: center;
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color:azure;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

.map-container-2 iframe{
left:0;
top:0;
height:100%;
width:100%;
position:absolute;
}
</style>
