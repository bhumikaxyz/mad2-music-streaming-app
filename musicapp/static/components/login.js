const Login = Vue.component("Login", {
  template: `<div
    class="container-sm d-flex justify-content-center align-items-center"
    style="height: 90vh"
  >
    <form
      method="post"
      action=""
      style="margin-top: 5em; margin-bottom: auto; margin-bottom: auto"
      class="form-outline w-50"
    >
      <img
        class="mb-4"
        src="static/images/musical-note.png"
        alt="Logo"
        width="90"
        height="90"
        style="display: block; margin-left: auto; margin-right: auto"
      />
      <h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>
  
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input
          type="text"
          id="username"
          name="username"
          class="form-control"
          v-model="credentials.username"
          required
        />
      </div>
  
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          id="password"
          name="password"
          class="form-control"
          v-model="credentials.password"
          required
        />
      </div>
  
      <div class="form-check">
        <input
          type="checkbox"
          id="remember"
          name="remember"
          class="form-check-input"
          v-model="credentials.remember_token"
        />
        <label class="form-check-label" for="remember">Remember me</label>
      </div>
  
      <div><button class="btn btn-primary mt-2" @click='login' > Login </button></div>
    </form>
  </div>
  `,
  data() {
    return {
      credentials: {
        username: null,
        password: null,
        remember_token: null,
      },
    };
  },
  methods: {
    async login() {
      console.log("gokul")
      console.log(this.credentials)
      console.log("sdasd")
        // try {
        //   const response = await fetch('http://127.0.0.1:5000/api/signin', {
        //     method: 'POST',
        //     headers: {
        //       'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({
        //       username: this.username,
        //       password: this.password,
        //     }),
        //   });
  
        //   if (!response.ok) {
        //     const errorData = await response.json();
        //     throw new Error(errorData.message);
        //   }
  
        //   const { access_token, username } = await response.json();s
        //   localStorage.setItem('access_token', access_token);
  
        //   this.$router.push('/home');
        // } catch (error) {

        //   console.error('Login failed:', error.message);
        //   this.$notify.error('Login failed. Please check your credentials.');
        // }
      },
    }
  })

export default Login;