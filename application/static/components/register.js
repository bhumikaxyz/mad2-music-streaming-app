const Register = Vue.component('Register', {
  
    template: `
    <div
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
        <h1 class="h3 mb-3 font-weight-normal">Register Today!</h1>
    
        <div class="mb-3">
          <label for="name" class="form-label">Name</label>
          <input type="text" id="name" name="name" class="form-control" required />
        </div>
    
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            class="form-control"
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
            required
          />
        </div>
    
        <div class="mb-3">
          <label for="confirm_password" class="form-label">Confirm Password</label>
          <input
            type="password"
            id="confirm_password"
            name="confirm_password"
            class="form-control"
            required
          />
        </div>
        <div>
          <button type="submit" class="btn btn-primary my-3">Register</button>
        </div>
      </form>
    </div>
    
    `,
    
    
});

export default Register;