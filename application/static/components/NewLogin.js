export default {
    template: `<div
    class="container-sm d-flex justify-content-center align-items-center"
    style="height: 90vh"
  >
    <div
      style="margin-top: 5em; margin-bottom: auto; margin-bottom: auto"
      class="w-50"
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
  
      <div><button class="btn btn-primary mt-3" @click='login' > Login </button></div>
    </div>
  </div>
  `,

  data(){
    return {
        credentials: {
            username: null,
            password: null
        },
        error: null
    }
  },

  methods: {
    async login() {
      const res = await fetch('http://127.0.0.1:5000/api/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.credentials),
      })
      const data = await res.json()
      if (res.ok) {
        console.log("OKAYYYY")
        localStorage.setItem('access-token', data.access_token)
        console.log("token saved")
        // localStorage.setItem('role', data.role)
        this.$router.push({ path: '/home' })
      } else {
        this.error = data.message
      }
    },
  }
}