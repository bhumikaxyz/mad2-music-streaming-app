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
  
      <div><button type="submit" class="btn btn-primary my-3">Sign In</button></div>
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
    login() {
      fetch("/login?include_auth_token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.credentials),
      }).then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Invalid username or password");
        }
      }).then((data) => {
        localStorage.setItem('auth-token', data.response.user.authentication_token)
        window.location.href='/';
      });
    },
  },
})


export default Login;